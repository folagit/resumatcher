from common import  * 
from bson.objectid import ObjectId
import datetime

class DataHandler:
    
    def __init__(self , dbclient=None ):
        if ( dbclient is None):
          self.dbClient = DbClient('localhost', 27017, "jobaly")               
        else: 
          self.dbClient = dbclient
          
        self.resumeCollection = self.dbClient.getCollection(gConfig["webResumeColName"]) 
        self.jobCollection = self.dbClient.getCollection(gConfig["webJobInfoCollName"])  

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
        return self.jobCollection.find_one({'_id': _id })

def main(): 

   dataHandler = DataHandler()
  # dataHandler.save_resume("dfasdfw dsfwedf")
  # item = dataHandler.get_resume('537178f841a0a20860278df4')
   item = dataHandler.get_job('3eb8caa5add2996b')
    
   print item 
    
if __name__ == "__main__": 
    main()
