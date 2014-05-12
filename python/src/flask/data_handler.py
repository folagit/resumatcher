

from dbclient import DbClient 
import datetime

class DataHandler:
    
    def __init__(self , dbclient=None ):
        if ( dbclient is None):
          self.dbClient = DbClient('localhost', 27017, "jobaly")               
        else: 
          self.dbClient = dbclient
          
        self.resumeCollection = self.dbClient.getCollection("test_resume")  

    def save_resume(self, resume_text): 
        resume = {"content": resume_text, "date": datetime.datetime.utcnow()}
        resume_id = self.resumeCollection.insert(resume)
        print "add resume id is:", resume_id
        
    def get_resumes(self):
        return self.resumeCollection.find()

def main(): 

   dataHandler = DataHandler()
   dataHandler.save_resume("dfasdfw dsfwedf")
    
if __name__ == "__main__": 
    main()
