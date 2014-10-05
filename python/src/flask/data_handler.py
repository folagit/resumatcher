from common import  gConfig 
from bson.objectid import ObjectId
import datetime
from jobaly.db.dbclient import DbClient 
from tfidf_match import TfIdfMatch

class DataHandler:
    
    def __init__(self , dbclient=None ):
        self.dbclient = dbclient
   
    def setup_tfidfMatcher(self):
        if ( self.dbclient is None):
          self.dbClient = DbClient('localhost', 27017, "jobaly")               
        else: 
          self.dbClient = dbclient
          
        self.resumeCollection = self.dbClient.getCollection(gConfig["webResumeColName"]) 
        self.jobCollection = self.dbClient.getCollection(gConfig["webJobInfoCollName"])  
        self.jobModelCollection = self.dbClient.getCollection(gConfig["jobModelCollName"])
        self.matcher = TfIdfMatch(self.jobCollection)

    def save_resume(self, resume_text): 
        resume = {"content": resume_text, "date": datetime.datetime.utcnow()}
        resume_id = self.resumeCollection.insert(resume)
        print "add resume id is:", resume_id
        
    def get_resumes(self):
        return self.resumeCollection.find()
        
    def get_resume(self, _id):
        return self.resumeCollection.find_one({'_id': ObjectId(_id)})
        
    def get_jobs(self, page_no=1, page_size=20):
        find_sort = None
        find_spec = None
        return self.dbClient.getPage(self.jobCollection, find_spec,find_sort, page_size, page_no)

    def get_job(self, _id):
        result=list(self.jobCollection.find({'_id': _id }))
        if len(result) > 0:
            return result[0]
        else :
            return None      
            
    def get_job_ids(self, ids):
        result=list(self.jobCollection.find({"_id": {"$in": ids}}))        
        return result  

    def get_jobmodel_ids(self, ids):
        result=list(self.modelCollection.find({"_id": {"$in": ids}}))        
        return result            
    
    def get_model(self, _id):
        result=list(self.modelCollection.find({'_id': _id }))
        if len(result) > 0:
            return result[0]
        else :
            return None
        
    def matchResume(self, resume):
        return self.matcher.matchResume(resume)
        
    def connectJobColl(self, dbName, collName):
        
        self.dbname = dbName 
        self.collname = collName                
        self.dbClient = DbClient('localhost', 27017, dbName)               
        self.jobCollection = self.dbClient.getCollection(collName)  
        self.collSize = self.dbClient.getCollectionSize(collName) 
        self.modelCollection = self.dbClient.getCollection(collName+"_model")
        
    def getJobsByPage(self, page_size ,  page_no ):
        find_sort = None
        find_spec = None        
        return self.dbClient.getPage(self.jobCollection, find_spec,find_sort, page_size, page_no)        
  
    def searchjobs(self,query,qtype )	:        
        if qtype == "jid" :
            result=list(self.jobCollection.find({'_id': query }))
            pageno = 1  
        elif  qtype == "jobtitle" :   
            result=list(self.jobCollection.find({'jobtitle': query }))
            pageno = 1              
            
        resultnum = len(result)
        return (result, pageno, resultnum)
        
        
def main(): 

  
   dataHandler = DataHandler()     
   dataHandler.connectJobColl("jobaly_daily_test","daily_job_2014-06-05")
   print  dataHandler.collSize
   qtype = "jid"
   query = "49d46bcba36a9767"
   
   qtype = "jobtitle"
   query = "Web Developer"
   
   jobs, pageno, resultnum =  dataHandler.searchjobs(query,qtype )	
  # print jobs 
   print pageno, resultnum
 
 
if __name__ == "__main__": 
    main()
