from common import  * 
from tfgetter import TfGetter
import re
import datetime
import math
from jobaly.db.dbclient import DbClient 


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    
def clearReturn(txt):
     return re.sub("\\\n\-|\\\n", " ",txt)   
     
def processText(txt):
    txt = striphtml(txt)  
    txt = clearReturn(txt)
    return txt
  
def getwtf(tf):
    wtf={}
    for key, value in tf.iteritems():
        wtf[key] = 1 + math.log10( float(value))
    return wtf
    
            
def dfAddTf(df, tf):
    for key, value in tf.iteritems():
        if df.has_key(key):
            df[key] += 1
        else:
            df[key] = 1
    
def getIdf(df, doc_num):
    idf={}
    for key, value in df.iteritems():
        idf[key] = math.log10( float(doc_num) / value )
    return idf
    
def getWtfIdf(wtf,idf):
    wtfidf = {} 
    sumweight = 0
    for key, value in wtf.iteritems():        
        wtfidf[key]=value*idf[key]
        sumweight += wtfidf[key] * wtfidf[key]
    length = math.sqrt(sumweight)
    return wtfidf, length

    
class TfIdfGetter():
    
    def __init__(self):
        self.tfgetter =  TfGetter()   
        
    def getTf(self, content):
        return self.tfgetter.getTf(content)

    def saveJobTfIdf(self, jobcoll , idfColl):
         
         df = {}    
         doc_num = 0
         for item in jobcoll.find(): 
             content = processText(item["summary"])       
             tf = self.getTf(content)
             item['tf'] = tf
             item['wtf'] =  getwtf(tf)
             jobcoll.save(item)
             dfAddTf(df,tf)
             doc_num+=1
         
         idfitem={}
         idfitem['doc_num'] = doc_num
         idfitem['df'] = df
         idf = getIdf(df,doc_num)
         idfitem['idf'] = idf
         idfitem['coll_name'] = jobcoll.name  
         idfitem['date'] = datetime.datetime.now()
        # print idf
         idfColl.save(idfitem)         
         
         for item in jobcoll.find(): 
            wtf = item['wtf']
            item['wtfidf'] , item['length'] = getWtfIdf(wtf,idf)
            jobcoll.save(item)
            
         return idfitem
         
    def getJobTfIdf(self, jobcoll ):     
         jobs = []
         df = {}    
         doc_num = 0
         for item in jobcoll.find(): 
             content = processText(item["summary"])       
             tf = self.getTf(content)            
             item['wtf'] =  getwtf(tf)
             jobs.append(item)
             dfAddTf(df,tf)
             doc_num+=1       
      
         idf = getIdf(df,doc_num)    
         for item in jobs: 
            wtf = item['wtf']
            item['wtfidf'] , item['length'] = getWtfIdf(wtf,idf)
            
         return idf, jobs

            
def main(): 

  # print gConfig
  dbClient = DbClient('localhost', 27017, "jobaly")  
  jobCollection = dbClient.getCollection(gConfig["webJobInfoCollName"])  
  jobIdfCollection = dbClient.getCollection(gConfig["JobIdfCollName"]) 
  
  tfIdfGetter = TfIdfGetter()
 # tfIdfGetter.saveJobTfIdf(jobCollection,  jobIdfCollection )
  idf, jobs = tfIdfGetter.getJobTfIdf(jobCollection)
  print idf
    
if __name__ == "__main__": 
    main()
