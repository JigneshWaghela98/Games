import pdfplumber
import os
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Function to extract text from a PDF file using pdfplumber
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

# Data Preparation
data_directory = r'C:\Users\PC\Desktop\DataResume'  # Ensure this is the correct path

resume_texts = []
job_categories = []

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

            # Basic text preprocessing (removes non-alphanumeric characters)
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()

            resume_texts.append(text)

            # Extract job category from the filename (e.g., software_engineer.pdf -> software_engineer)
            job_category = filename.split('.')[0]
            job_categories.append(job_category)

    # Check if any resumes were processed
    print(f"Number of resumes processed: {len(resume_texts)}")
    print(f"Number of job categories: {len(job_categories)}")

    if len(resume_texts) == 0:
        print("Error: No valid resumes to process. Please check the data directory and ensure there are PDF files with extractable text.")
    else:
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            resume_texts, job_categories, test_size=0.2, random_state=42
        )

        # Feature extraction using TF-IDF Vectorizer
        vectorizer = TfidfVectorizer()
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        # Model training using Logistic Regression
        model = LogisticRegression(max_iter=1000)  # Increased max_iter for convergence
        model.fit(X_train_vec, y_train)

        # Model Evaluation: Print classification report
        y_pred = model.predict(X_test_vec)
        print("Model Evaluation (Classification Report):")
        print(classification_report(y_test, y_pred))

        # Function to predict the job category of a new resume
        def predict_job_category(new_resume_path):
            new_resume_text = extract_text_from_pdf(new_resume_path)
            new_resume_text = re.sub(r'[^a-zA-Z0-9\s]', '', new_resume_text).lower()
            new_resume_vec = vectorizer.transform([new_resume_text])
            predicted_category = model.predict(new_resume_vec)[0]
            return predicted_category

        # Example usage:
        new_resume_path = r'C:\Users\PC\Downloads\archive\data\data\APPAREL'  # Replace with the actual path to the new resume
        predicted_category = predict_job_category(new_resume_path)
        print(f"Predicted Job Category for the new resume: {predicted_category}")
