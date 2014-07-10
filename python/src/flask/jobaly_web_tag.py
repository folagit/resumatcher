from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
     
from data_handler import DataHandler
import json
import math

dbinfo = {}
dbinfo["pagesize"] = 20
dbinfo['dbname'] = "jobaly_daily_test"  
dbinfo['collname']   = "daily_job_2014-06-05"

app = Flask(__name__)     
dataHandler = DataHandler()     
dataHandler.connectJobColl(dbinfo['dbname'] , dbinfo['collname'])
dbinfo['collsize'] =  dataHandler.collSize    
     
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
    for item in jobs:
        print item["_id"]
        
    dbinfo["pageno"] = pageno
    pagerInfo=getPagerInfo(pageno)
    return render_template('tag_index.html', dbinfo=dbinfo, pagerInfo=pagerInfo,  jobs=jobs)

def getPagerInfo(pageno):
    pagerInfo= {}
    pagerInfo["pageno"] = pageno
    pagenum = math.ceil(dbinfo['collsize'] / dbinfo['pagesize'])
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
    dbinfo['dbname'] = request.form['dbname'].strip()
    dbinfo['collname'] = request.form['collname'].strip()    
    print "dbname=", dbinfo['dbname'], "collname=", dbinfo['collname']   
    
    dataHandler.connectJobColl(dbname,collname) 
    return handle_index()

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

if __name__ == '__main__':
    
    app.run( host='0.0.0.0',  debug=True)
