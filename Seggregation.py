import pdfplumber
import os
import re
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold  # StratifiedKFold for stratified CV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier  # Trying Random Forest Classifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder  # For encoding job categories

import joblib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Ensure you have NLTK stopwords and WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')

# Function to extract text  from a PDF file using pdfplumber
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # If text extraction was successful
                    text += page_text
            return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

# Improved text preprocessing
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    
    # Lemmatization (Reduce words to their base form)
    lemmatizer = WordNetLemmatizer()
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
    
    return text

# Data Preparation
data_directory = r'C:\Users\PC\Desktop\DataResume'  # Ensure this is the correct path

resume_texts = []
job_categories = []

# Dictionary to map short job categories to full department names
category_to_full_name = {
    "hr": "HR Department",
    "engineering": "Engineering Department",
    "marketing": "Marketing Department",
    "finance": "Finance Department",
    "sales": "Sales Department",
    # Add more mappings as needed
}

# Check if there are PDF files in the directory
if not any(filename.endswith('.pdf') for filename in os.listdir(data_directory)):
    print("No PDF files found in the specified directory.")
else:
    # Iterate through the directory and process each PDF resume
    for filename in os.listdir(data_directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(data_directory, filename)
            text = extract_text_from_pdf(filepath)

            # Check if text extraction was successful
            if not text:
                print(f"Warning: No text extracted from {filename}")
                continue

            # Preprocess the text
            text = preprocess_text(text)

            resume_texts.append(text)

            # Extract job category from the filename (e.g., software_engineer.pdf -> software_engineer)
            job_category = filename.split('.')[0].lower()
            job_categories.append(job_category)

    # Check if any resumes were processed
    print(f"Number of resumes processed: {len(resume_texts)}")
    print(f"Number of job categories: {len(job_categories)}")

    if len(resume_texts) == 0:
        print("Error: No valid resumes to process. Please check the data directory and ensure there are PDF files with extractable text.")
    else:
        # Encode job categories using LabelEncoder
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(job_categories)

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            resume_texts, y_encoded, test_size=0.2, random_state=42
        )

        # Check class distribution
        class_distribution = {category: list(y_train).count(i) for i, category in enumerate(label_encoder.classes_)}
        print(f"Class distribution: {class_distribution}")

        # Determine the number of splits based on the class distribution
        # If any class has fewer than 2 samples, set n_splits=2
        min_samples_in_class = min(class_distribution.values())
        n_splits = 3 if min_samples_in_class >= 3 else 2

        # Ensure n_splits is always at least 2
        if n_splits < 2:
            print("Warning: Some classes have too few samples. Skipping cross-validation.")
            n_splits = 2

        print(f"Using n_splits = {n_splits}")

        # Feature extraction using TF-IDF Vectorizer (with n-grams)
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_df=0.9, min_df=5)
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        # Trying Random Forest Classifier
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_vec, y_train)

        # Save the trained model using joblib
        model_file_path = r'C:\Users\PC\Desktop\resume_classifier_model.joblib'  # Choose a path to save the model
        joblib.dump(model, model_file_path)  # Save the model
        joblib.dump(vectorizer, r'C:\Users\PC\Desktop\vectorizer.joblib')  # Save the vectorizer
        joblib.dump(label_encoder, r'C:\Users\PC\Desktop\label_encoder.joblib')  # Save the label encoder
        print(f"Model, vectorizer, and label encoder saved.")

        # Model Evaluation: Print classification report
        y_pred = model.predict(X_test_vec)
        print("Model Evaluation (Classification Report):")
        print(classification_report(y_test, y_pred))

        # If there are enough samples for cross-validation, proceed with it
        if n_splits >= 2:
            # Stratified Cross-validation to check model performance
            stratified_kfold = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
            cross_val_scores = cross_val_score(model, X_train_vec, y_train, cv=stratified_kfold, scoring='accuracy')
            print(f"Cross-validation scores: {cross_val_scores}")
            print(f"Mean cross-validation score: {cross_val_scores.mean()}")
        else:
            print("Skipping cross-validation due to insufficient data for stratified splitting.")

        # Function to predict the job category of a new resume
        def predict_job_category(new_resume_path):
            # Extract text from the new resume
            new_resume_text = extract_text_from_pdf(new_resume_path)
            if not new_resume_text:
                print(f"Error: No text extracted from {new_resume_path}")
                return None

            # Preprocess the new resume text
            new_resume_text = preprocess_text(new_resume_text)

            # Transform the new resume text into the same feature space as the training data
            new_resume_vec = vectorizer.transform([new_resume_text])

            # Predict the job category (encoded)
            predicted_encoded = model.predict(new_resume_vec)[0]

            # Decode the predicted label back to the original category name
            predicted_category = label_encoder.inverse_transform([predicted_encoded])[0]

            # Map the predicted category to its full department name
            full_department_name = category_to_full_name.get(predicted_category, "Unknown Department")
            return full_department_name

        # Example usage
        new_resume = r"D:/TestResume/29091445.pdf"  # Replace with the path to your new resume
        predicted_category = predict_job_category(new_resume)
        print(f"Predicted job category: {predicted_category}")
