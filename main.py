from flask import Flask, render_template, request, send_from_directory
import os
import docx2txt
import PyPDF2

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

@app.route("/")
def matchresume():
    return render_template('matchresume.html')


@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form['job_description']
        resume_files = request.files.getlist('resumes')

        resumes = []
        matching_keywords = []  
        missing_keywords = {}  
        job_words = set(job_description.lower().split()) 
        analysis = {}  
        comparative_summaries = []  

        for resume_file in resume_files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)
            resume_text = extract_text(filename).lower()
            resumes.append(resume_text)

          
            resume_words = set(resume_text.split())
            matching = job_words & resume_words  
            matching_keywords.append(matching)

            missing = job_words - resume_words 
            missing_keywords[resume_file.filename] = missing

            total_job_words = len(job_words)
            total_resume_words = len(resume_words)
            matching_count = len(matching)
            percentage_matching = (matching_count / total_job_words) * 100 if total_job_words else 0

            analysis[resume_file.filename] = {
                "Total Job Description Words": total_job_words,
                "Total Resume Words": total_resume_words,
                "Matching Words": matching_count,
                "Percentage of Matching": f"{percentage_matching:.2f}%"
            }

            summary = generate_comparative_summary(job_description, resume_text)
            comparative_summaries.append({
                "filename": resume_file.filename,
                "summary": summary
            })

        if not resumes or not job_description:
            return render_template('matchresume.html', message="Please upload resumes and enter a job description.")

        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()

        job_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_vector], resume_vectors)[0]

        top_indices = similarities.argsort()[-5:][::-1]
        top_resumes = [resume_files[i].filename for i in top_indices]
        similarity_scores = [round(similarities[i], 2) for i in top_indices]

        if not top_resumes or not similarity_scores:
            return render_template('matchresume.html', message="No matching resumes found.")

        return render_template('matchresume.html', 
                               message="Top matching resumes:", 
                               top_resumes=top_resumes, 
                               similarity_scores=similarity_scores,
                               top_matching_keywords=matching_keywords,
                               analysis=analysis,
                               missing_keywords=missing_keywords,
                               comparative_summaries=comparative_summaries,
                               zip=zip)

    return render_template('matchresume.html')


def generate_comparative_summary(job_description, resume_text):
    """Generates a comparative summary between job description and resume text"""
    
    job_words = set(job_description.lower().split())
    resume_words = set(resume_text.lower().split())

    
    matching_words = job_words & resume_words
    missing_words = job_words - resume_words

  
    summary = f"Matching skills: {', '.join(matching_words)}\n"
    summary += f"Missing skills: {', '.join(missing_words)}\n"
    summary += f"Total matching: {len(matching_words)} out of {len(job_words)}\n"
    return summary


@app.route('/download_resume/<filename>')
def download_resume(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/help')
def help():
    return render_template('help.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/logout')
def logout():
    return render_template('login.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
