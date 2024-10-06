from flask import Flask, request, render_template
import os
import PyPDF2
from transformers import pipeline
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

nltk.download('punkt')


summarizer = pipeline("summarization")

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def summarize_text(text):

    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def extract_keywords(text):
   
    words = word_tokenize(text)
    
 
    words = [word.lower() for word in words if word.isalnum()]
    
    
    freq_dist = FreqDist(words)

    keywords = freq_dist.most_common(10) 
    return [word for word, freq in keywords]

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        if pdf_file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(filename)
            text = extract_text_from_pdf(filename)

            summary = summarize_text(text)
            keywords = extract_keywords(text)

            return render_template('result.html', summary=summary, keywords=keywords)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
