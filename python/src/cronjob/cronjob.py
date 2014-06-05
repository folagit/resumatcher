from joblist_daily import *
from jobinfo_daily import *


def main():
     
     today = datetime.date.today()    
     listCollectionName = "daily_job_list_"+str(today)
     print listCollectionName
     infoCollectionName = "daily_job_info_"+str(today)
     print infoCollectionName
     
     getJobList(listCollectionName) 
     getJobInfo(listCollectionName, infoCollectionName)
     
    
if __name__ == "__main__": 
    main()
