# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 13:52:04 2014

@author: dlmu__000
"""
import codecs
import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient
import jobaly.utils 

prehtml = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	<title>untitled</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta name="generator" content="Geany 1.24" />

<style type="text/css">
.detail_jobtitle {
height:50px;
font-size:22px;
color:#764293;
}

.detail_div {
padding-top: 30px;  
padding-right: 0px;  
padding-bottom: 20px;  
padding-left: 50px;  
width:580px;
}
</style>

</head>

<body>'''

posthtml = ''' 
</body>

</html>'''

def loadJobs(dbname, collName, ids):
     dbClient = DbClient('localhost', 27017, dbname)
     jobCollection = dbClient.getCollection(collName)
     jobs = []
     for jobid in ids:
        result=list(jobCollection.find({'_id': jobid }))
        if len(result) > 0:
            job = result[0]
         #   print type(job)
         #   print job
            print job["_id"], job["location"]
            jobs.append(job)
     return jobs
     
def createPage(jobs, name):
    filename = "pages\\" + name+".html"
     
    page = prehtml.replace("untitled",name)
    gray = True
    n = 0
    for job in jobs:
     #   print job
        n += 1
        gray = not gray
        bg = '  style="background-color:' + ('#eeeeee' if gray else '#FFFFFF') + ';"'       
        
        div = '\n<div  class="detail_div"' +bg  + ' >\n' 
        div = div + '\n<div style="font-size:24px;"> No:&nbsp;&nbsp;' + str(n) + '&nbsp;&nbsp;&nbsp;&nbsp' + 'Job Id:&nbsp;&nbsp;' + job["_id"] +  '</div>\n'
        div = div +   '<div class="detail_jobtitle" >' +  job["jobtitle"] +  '</div>\n'
        div = div +   '<div>' +  job["summary"] +  '\n</div>\n'
        div = div + '\n</div>\n\n\n'
        page = page + div 
    page = page +   posthtml      
    
    f = codecs.open(filename, "w", "utf-8")
    f.write(page)
    f.close()
         
def main():
     dbname = "jobaly" 
     keyword = "web developer"
     keyword = "java"
     keyword = "python"
     keyword = "javascript"
     keyword = "PHP"
     keyword = "HTML"
     
     name = keyword.split()[0]
     jobCollectionName = "keyword_info_"+name
     idsfile = "pages\\"+name+".txt"
  
     ids = jobaly.utils.loadArrayFromFile(idsfile)  
  
     jobs = loadJobs(dbname, jobCollectionName, ids)
     createPage(jobs, name)
      
if __name__ == "__main__": 
    main()