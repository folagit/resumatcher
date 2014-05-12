from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
     
from data_handler import DataHandler

app = Flask(__name__)     
dataHandler = DataHandler()
     
@app.route('/')
def handle_index():     
    
    resumes = dataHandler.get_resumes()
    
    return render_template('index.html', resumes=resumes)

@app.route('/add_resume',  methods=['POST', 'GET'])     
def add_resume():    
    error = None
    if request.method == 'POST':
         resume_text = request.form['resume_txt'].strip()
         print "resume_text:", resume_text
         if len(resume_text) > 0 :
             dataHandler.save_resume(resume_text)
         
    return handle_index()

if __name__ == '__main__':
    
    app.run( host='0.0.0.0',  debug=True)
