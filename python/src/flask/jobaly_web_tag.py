from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,  send_from_directory
from werkzeug import secure_filename  
from data_handler import DataHandler
import json
import math
import os
from jobanalysis.jobdescparser import JobDescParser 
from filetotxt import fileToTxt
from jobanalysis.resume import  resumeparser  
from jobanalysis.similarity.modelsimilarity import ModelSimilarity


dbinfo = {}
dbinfo["pagesize"] = 20
dbinfo['dbname'] = "jobaly_daily_test"  
dbinfo['collname'] = "daily_job_webdev"
dbinfo['modelcollname'] = dbinfo['collname']+"_model"

app = Flask(__name__)     
dataHandler = DataHandler()     
dataHandler.connectJobColl(dbinfo['dbname'] , dbinfo['collname'])
  
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['resume'] = ""   
app.config['resume_name'] = ""
     
@app.route('/layout.html')
def handle_layout():
    return render_template('layout.html')
     
@app.route('/')
@app.route('/index.html')
def handle_index():        
    pageno = request.args.get("pageno")
    print "pageno = ", pageno
    if pageno is None:
        pageno = 1
    else :
         pageno = int( pageno.strip() )
    jobs = list( dataHandler.getJobsByPage(dbinfo["pagesize"], pageno))
  #  for item in jobs:
  #      print item["_id"]
        
    dbinfo["pageno"] = pageno
    dbinfo['collsize'] =  dataHandler.collSize  
    pagerInfo=getPagerInfo(pageno)
    return render_template('tag_index.html', dbinfo=dbinfo, pagerInfo=pagerInfo,  jobs=jobs)

def getPagerInfo(pageno):
    pagerInfo= {}
    pagerInfo["pageno"] = pageno
    pagenum = int(math.ceil(dbinfo['collsize'] / dbinfo['pagesize']))
    pagerInfo["pagenum"] = pagenum
    if pagenum <= 10 :
        pagerInfo["start"] = 1
        pagerInfo["end"]  =  pagenum   
    elif pageno < 6 : 
        pagerInfo["start"] = 1    
        pagerInfo["end"]  =  10
    elif pageno > pagenum - 5 : 
        pagerInfo["start"] = pagenum - 10    
        pagerInfo["end"]  =  pagenum
    else :
        pagerInfo["start"] = pageno - 5    
        pagerInfo["end"]  =  pageno + 4
    
    return pagerInfo
          
@app.route('/connectcoll.html')      
def connect_coll():
    dbinfo['dbname'] = request.args.get('dbname','').strip()
    dbinfo['collname'] = request.args.get('collname','').strip()    
    print "dbname=", dbinfo['dbname'], "collname=", dbinfo['collname']   
    
    dataHandler.connectJobColl(dbinfo['dbname'],dbinfo['collname']) 
    return handle_index()

@app.route('/jobdetail.html')    
def  jobdetail():    
	
	jobid = request.args.get('jobid', '').strip()
	print " handle_match jobid=", jobid	 
	job =  dataHandler.get_job(jobid)	
	return render_template('jobdetail.html', dbinfo=dbinfo, job=job )

@app.route('/jobparas.html')    
def  jobParagraghs():   	
   jobid = request.args.get('jobid', '').strip()
   print " handle_match jobid=", jobid	 
   job =  dataHandler.get_job(jobid)	 
   jobDesc = JobDescParser.parseJobDesc(job)
   paras = jobDesc.listParagraphs()
   return render_template('jobparas.html', dbinfo=dbinfo, job=job, paras=paras )

@app.route('/jobmodel.html')    
def  jobModel():   	
   jobid = request.args.get('jobid', '').strip()
   print " handle_match jobid=", jobid	 
   job =  dataHandler.get_job(jobid)	 
   model = dataHandler.get_model(jobid)	
   return render_template('jobmodel.html', dbinfo=dbinfo, job=job, model=model )


@app.route('/searchjobs.html')    
def  searchjob():    
   query = request.args.get('query', '').strip()
   qtype = request.args.get('qtype', '').strip()
	 
   jobs, pageno, resultnum =  dataHandler.searchjobs(query,qtype )	
       
   dbinfo["pageno"] = pageno
   dbinfo['collsize'] =  resultnum
   pagerInfo= {}
   pagerInfo["start"] = 1
   pagerInfo["end"]  =  1  
  
   return render_template('tag_index.html', dbinfo=dbinfo, pagerInfo=pagerInfo,  jobs=jobs)

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
	else: 
		content = resume["content"]
		resume["content"] = "<br />".join(content.split("\n"))
	
	return render_template('resume.html', resumes=resumes, resume=resume)
	
@app.route('/search_result.html')    
def  handle_match():    
	
    re_id = request.args.get('reid', '').strip()
    print " handle_match re_id=", re_id	 
    resume =  dataHandler.get_resume(re_id)
    content = "no_content"
    if resume is None:
        resume = { "_id":re_id , "content":"no_content"}
    else: 
        content = resume["content"]
        resume["content"] = "<br />".join(content.split("\n"))
        
    jobs = dataHandler.matchResume(content)

    return render_template('search_result.html', resume=resume, jobs=jobs)
	
@app.route('/getjob.ajax')    
def  ajax_getjob():    
	
	jobid = request.args.get('jobid', '').strip()
	print " handle_match jobid=", jobid	 
	job =  dataHandler.get_job(jobid)	
	return  json.dumps(job) 
 
@app.route('/connectdb.ajax')    
def  ajax_connectColl():    
	
    dbName = request.args.get('dbname', '').strip()	 
    collName =  request.args.get('collname', '').strip()	 
    print " ajax_connectColl dbName=", dbName, " collName =", collName 
    app.logger.debug(" ajax_connectColl dbName=" + dbName +"; collName ="+ collName )

    result = {}
    
@app.route('/set_resume.html')    
def  set_resume():
    content = ""
    filename = ""
    if session.has_key("resume"):    	    
        content = session['resume']   
        filename = session['resume_name']
        print  "session resume name =>>=", session['resume_name']
    return render_template('set_resume.html', resume=content, filename=filename )
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploadresume', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        path = os.path.join(app.config['UPLOAD_FOLDER'] , filename)
        print "path=", path
        file.save( path )
        resume = fileToTxt(path)
        session['resume'] = resume
        session['resume_name'] = filename
        print  "session resume name ===", session['resume_name']
                        
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return render_template('set_resume.html', resume=resume, filename=filename )

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
                               
@app.route('/resume_match')    
def resume_match():         
     resume = session['resume']               
     resumeModel = resumeparser.parseResumeText(resume)                              
     modelColl = dataHandler.modelCollection  
     similarity = ModelSimilarity()    
     result = similarity.match_jobs(resumeModel , modelColl  )
     i = 0
     jobs = []
     for key, value in result:
         i += 1
         print i,key, value
         job = dataHandler.get_job(key)
         job["score"] = value
         jobs.append(job)
         if i == 30 :
             break

     return render_template('job_match.html', jobs=jobs) 

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run( host='0.0.0.0',  debug=True)