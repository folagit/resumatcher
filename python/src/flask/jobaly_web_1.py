from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
     
from data_handler import DataHandler

app = Flask(__name__)     
dataHandler = DataHandler()
     
     
@app.route('/layout.html')
def handle_layout():
    return render_template('layout.html')
     
@app.route('/')
@app.route('/index.html')
def handle_index():     
    
    resumes = dataHandler.get_resumes()    
    return render_template('index.html', resumes=resumes)

@app.route('/add_resume',  methods=['POST', 'GET'])     
def add_resume():    
    error = None
    if request.method == 'POST':
         resume_text = request.form['resume_txt'].strip()
    #     print "resume_text:", resume_text
         if len(resume_text) > 0 :
             dataHandler.save_resume(resume_text)
         
    return handle_index()
    
@app.route('/resume.html')     
def  handle_resume():    
	
	re_id = request.args.get('reid', '').strip()
	print " handle_resume re_id=", re_id
	resumes = dataHandler.get_resumes()   
	resume =  dataHandler.get_resume(re_id)
	if resume is None:
		resume = { "_id":re_id , "content":"no_content"}
	
	return render_template('resume.html', resumes=resumes, resume=resume)

if __name__ == '__main__':
    
    app.run( host='0.0.0.0',  debug=True)
