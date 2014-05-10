
from dbclient import DbClient 
import operator

def main(): 
    collectionName = "job_lang_top_corps"
    dbClient = DbClient('localhost', 27017, "jobaly")
    collection = dbClient.getCollection(collectionName)
    
    title_dict = {}
    for job in collection.find():
        # print job["_id"], job["jobtitle"]
        title =  job["jobtitle"]
        if title_dict.has_key(title): 
            title_dict[title] += 1
        else :
            title_dict[title] = 1
    
    stat_file_name =  "jobtitle_stat.txt"  
    with open( stat_file_name , "w") as text_file:   
        i = 0 
        for (key, value) in sorted(title_dict.iteritems(), key=operator.itemgetter(1), reverse = True):
        #     print key, ":", value 
             text_file.write("%s : %s \n" % (key.encode('utf8'),value)) 
             i+=1
        print i, " lines had been writen into file:", stat_file_name
    
if __name__ == "__main__": 
    main()
