from flask import Flask, jsonify, redirect, render_template, request, url_for
import pandas as pd
import sys
sys.path.append('C:\\Users\\Keertisuryawanshi\\Desktop\\Python\\database')
from connection import engine

sys.path.append('C:\\Users\\Keertisuryawanshi\\Desktop\\Python\\notification_system')
from notification_system.hushushmail import send_email

sys.path.append('C:\\Users\\Keertisuryawanshi\\Desktop\\Python\\evaluation_system')
from algopickle import process_and_save_candidates
# from .notification import shortlist_mail

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_role = request.form['job_role']
        # Construct the table name based on the selected job role
        process_and_save_candidates(job_role)
        table_name = f'candidates_{job_role.replace(" ", "_").lower()}'
        # Fetch data from the database for the selected job role
        query = f"SELECT * FROM {table_name} LIMIT 10;"
        candidates_df = pd.read_sql(query, engine)
        candidates = candidates_df.to_dict(orient='records')
        
        return render_template('index.html', job_role=job_role, candidates=candidates)
    
    return render_template('index.html')

@app.route('/send_emails', methods=['POST'])
def send_emails():
    # Get the selected job role from the request data
    job_role = request.args.get('job_role')

    # Construct the table name based on the selected job role
    table_name = f'candidates_for_{job_role.replace(" ", "_").lower()}'

    # Fetch data from the database for the selected job role
    query = f"SELECT * FROM {table_name} LIMIT 10;"
    candidates_df = pd.read_sql(query, engine)
    candidates = candidates_df.to_dict(orient='records')

    # Send emails to each candidate
    subject = "'Congratulations! You've been Selected for the Doodle Hiring Process'"
    body = """
    <!-- Your HTML email body here -->
    """

    for candidate in candidates:
        receiver_email = candidate['owner_email_address']
        send_email(receiver_email, subject, body)

    return jsonify({'message': 'Emails sent successfully.'})

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Process the form data (e.g., save to a database, send an email, etc.)
        # For now, let's just print it to the console
        print(f"Received feedback from {name} ({email}): {message}")
        
        # Redirect to a new page or back to the form with a success message
        return redirect(url_for('index'))  # Assuming 'index' is a route that exists
    else:
        # If someone navigates to /feedback directly, just show the form
        return render_template('feedback.html')
    
if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         selected_job_role = request.form['job_role']
#         # Fetch data from the database based on the selected job role
#         table_name = selected_job_role.replace(' ', '_').lower() + '_top_candidates'
#         query = f"SELECT * FROM {table_name};"
#         candidates_df = pd.read_sql(query, engine)
#         candidates = candidates_df[['Owner Display Name', 'Owner User ID', 'Owner Reputation']].to_dict(orient='records')
#         return render_template('index.html', selected_job_role=selected_job_role, candidates=candidates)
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

# Getting results from directly reading CSV file 

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         selected_job_role = request.form['job_role']
#         candidates_df = pd.read_csv(f'candidates_for_{selected_job_role}.csv')
#         candidates = candidates_df.to_dict(orient='records')
#         return render_template('index.html', selected_job_role=selected_job_role, candidates=candidates)
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

























# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
        
#         pass
#     return render_template('index.html')

# @app.route('/Feedback', methods=['GET', 'POST'])
# def Feedback():
#     if request.method == 'POST':
#         # Process the form 
#         pass
#     return render_template('Feedback.html')


