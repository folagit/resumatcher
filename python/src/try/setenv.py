import os
import datetime
#print os.environ["PATH"]
today = str(datetime.date.today())  
#os.environ["COLL_DATE"] = today
listCollectionName = "daily_job_list_"+str(today)     
infoCollectionName = "daily_job_info_"+str(today)
os.environ["LIST_COLL_NAME"] = listCollectionName
os.environ["INFO_COLL_NAME"] = infoCollectionName

os.system("bash")
