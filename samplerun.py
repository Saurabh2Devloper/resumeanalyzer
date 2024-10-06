@app.route('/download_resume/<filename>')
def download_resume(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404
    
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


# Download Buttn
#  <td><a href="{{ url_for('download_resume', filename=resume) }}" class="download-btn">Download</a></td>


# Comparative summary DIV
# <div>
#     <h3>Comparative Summary</h3>
#     {% for summary in comparative_summaries %}
#         <div class="resume-card">
#             <div><strong>Resume: {{ summary.filename }}</strong></div>
#             <div>{{ summary.summary }}</div>
#         </div>
#     {% endfor %}
# </div>


# Improvement Section 

#  <div class="improvements-section">
#             <h3>Improvements</h3>
#             {% if missing_keywords %}
#                 <ul class="improvements-list">
#                     {% for resume, missing in missing_keywords.items() %}
#                         <li>
#                             <strong>{{ resume }}:</strong> {{ missing | join(', ') }}
#                         </li>
#                     {% endfor %}
#                 </ul>
#             {% else %}
#                 <p>No missing keywords found.</p>
#             {% endif %}
#         </div>


# <div>
#                                 <strong>Matching Words:</strong> {{ details['Matching Words'] }}
#                             </div>
#                             <div>
#                                 <strong>Percentage of Matching:</strong> {{ details['Percentage of Matching'] }}
#                             </div>



#  <table>
#                     <tr>
#                         <th>Resume</th>
#                         <th>Similarity Score</th>
#                         <th>Download</th>
#                     </tr>
#                     {% for resume, score in zip(top_resumes, similarity_scores) %}
#                     <tr>
#                         <td>{{ resume }}</td>
#                         <td>{{ score }}</td>
#                        <!-- btn -->
#                     </tr>
#                     {% endfor %}
#                 </table>