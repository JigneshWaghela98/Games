from googlesearch import search
import requests
from bs4 import BeautifulSoup

def google_search(query, num_results=5):
    try:
        search_results = search(query, lang='en')

        # Counter for tracking results
        result_count = 0

        for url in search_results:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title and content
            title = soup.title.text.strip() if soup.title else 'No title found'
            paragraphs = soup.find_all('p')
            content = '\n'.join([para.text.strip() for para in paragraphs])

            # Print title and content
            print(f"Title: {title}")
            print(f"Content:\n{content}")
            print("------")

            # Increment result count
            result_count += 1

            # Break loop if 2 results have been processed
            if result_count == 2:
                break

    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage:
query = "what is nifty today at?"
google_search(query)
