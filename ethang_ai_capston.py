from flask import Flask, render_template, url_for, request
import os
from groq import Groq

api_key = "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"
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""@app.route('/')
def index():
    return render_template('index.html')"""

@app.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Get the API key from the request
        submitted_api_key = request.form.get('api_key')
        
        # Verify the API key
        if submitted_api_key == api_key:
            # Check if a file was uploaded
            if 'file' not in request.files:
                return 'No file uploaded', 400
            
            file = request.files['file']
            
            # Check if a file was selected
            if file.filename == '':
                return 'No file selected', 400
            
            # Check if it's a text file
            if not file.filename.endswith('.txt'):
                return 'Only .txt files are allowed', 400
            
            # Save the file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Read the file content
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Initialize Groq client
            client = Groq(api_key=api_key)
            
            # Create the prompt for summarization
            prompt = f"Please summarize the following text:\n\n{content}"
            
            # Get completion from Groq
            completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.3,
                max_tokens=1000
            )
            
            # Get the summary
            summary = completion.choices[0].message.content
            
            # Clean up - delete the uploaded file
            os.remove(filepath)
            
            return render_template('result.html', summary=summary)
        else:
            return 'Invalid API key', 401
    
    # Handle GET request
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)
