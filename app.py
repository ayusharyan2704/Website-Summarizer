from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

app = Flask(__name__)

# Function to extract website content
def get_website_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        return content
    except Exception as e:
        return str(e)

# Function to summarize the extracted content
def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=200, min_length=150, do_sample=False)
    return summary[0]['summary_text']

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle URL submission and summarization
@app.route('/summarize', methods=['POST'])
def summarize_website():
    url = request.form['url']
    content = get_website_content(url)
    if len(content) > 2000:
        content = content[:2000]
    summary = summarize_text(content)
    return render_template('result.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
