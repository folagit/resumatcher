from common import  * 
from jobaly.db.dbclient import DbClient 

def makeJobInfoColl():  
   dbClient = DbClient('localhost', 27017, "jobaly")  
   dbClient.copyToCollection(gConfig["srcJobInfoCollName"], gConfig["webJobInfoCollName"],20)     

def main(): 
 
  makeJobInfoColl()

    
if __name__ == "__main__": 
    main()
