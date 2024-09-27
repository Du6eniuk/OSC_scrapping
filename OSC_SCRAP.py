import requests 
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to scrape the website and extract only the URL
def get_url(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.find_all('p')[0].text.strip()
            
            # Use regex to find URLs in the text
            url_pattern = r'www\.[a-zA-Z0-9-]+\.[a-zA-Z0-9./-]+'  # Adjust the pattern as needed
            found_urls = re.findall(url_pattern, text)
            return found_urls[0] if found_urls else "URL not found"
        else:
            return "Request failed"
    except requests.RequestException:
        return "Invalid URL or request failed"

# Function to process a list of URLs and save the results in a DataFrame
def process_urls_from_csv(input_csv, output_csv):
    # Read the CSV file into a DataFrame
    input_df = pd.read_csv(input_csv)

    # Assuming the column containing URLs is named 'URL'
    data = []
    for url in input_df['URL']:
        address = get_url(url)
        data.append({'URL': url, 'Address': address})
    
    # Creating a DataFrame
    output_df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    output_df.to_csv(output_csv, index=False)

    return output_df

# Example usage
input_csv = 'OSC_input.csv'  
output_csv = 'OSC_output.csv' 

result_df = process_urls_from_csv(input_csv, output_csv)