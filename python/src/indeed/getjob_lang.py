

from apiclient import ApiClient
from dbclient import DbClient 

def getByLang():
    
    print " --- get job by language and companies---"
    collectionName = "job_lang_top_corps"
    param = { "q" : "software engineer", 
               "fromage" : "30"    }    
               
    lang_names = ["java", "python", "javascript", "C++", "C", "C#", "ruby", "scala", "lisp" ]
    
    indeedClient= ApiClient( param )
    # client.getPage(0)
    dbClient = DbClient('localhost', 27017, "jobaly")
    collection = dbClient.getCollection(collectionName)
    
    
    for corp in indeedClient.corps:
       for lang in lang_names:
           q = indeedClient.buildQuery(lang, {"company": corp })
           print "-----prcoss corp %s with language %s -------" % (corp, lang) 
           indeedClient.processQuery(collection, "q", q)

def main(): 
    getByLang()  
    
if __name__ == "__main__": 
    main()
