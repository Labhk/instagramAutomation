import os
import json
import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment variable
my_key = os.getenv('GEMINI_API_KEY')

# Initialize ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro", verbose=True, temperature=0.1, google_api_key=my_key)



class BrowserTools:

    @staticmethod
    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content, just pass a string with
        only the full url, no need for a final slash `/`, eg: https://google.com or https://clearbit.com/about-us"""
        # Get HTML content from the website
        response = requests.get(website)
        if response.status_code != 200:
            return "Failed to retrieve website content."

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all div elements and extract their text
        div_texts = [div.get_text() for div in soup.find_all('div')]

        # Join extracted text into a single string
        content = '\n\n'.join(div_texts)

        # Limit the content to the first 8000 characters
        content_chunks = [content[i:i + 6000] for i in range(0, len(content), 6000)]

        summaries = []
        for chunk in content_chunks:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing researches and summaries based on the content you are working with',
                backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                llm=llm,
                allow_delegation=False)
            task = Task(
                agent=agent,
                description=f'Analyze and make a LONG summary the content below, make sure to include ALL relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
            )
            summary = task.execute()
            summaries.append(summary)

        # Join all summaries into a single string
        final_summary = '\n\n'.join(summaries)

        return f'\nScrapped Content: {final_summary}\n'