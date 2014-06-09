import sys
sys.path.append("..")
from apiclient import ApiClient
import jobaly.utils
import datetime

def main(): 
    today = datetime.date.today()    
    lang_names = jobaly.utils.loadArrayFromFile("lang_list.txt")  
    loc_list = jobaly.utils.loadArrayFromFile("state_list.txt")  
    lang_names = ['java', 'C++']
    lang_names = ['java']
    
   # lang_names = jobaly.utils.loadArrayFromFile("test_lang_list.txt")  
   # cities = jobaly.utils.loadArrayFromFile("test_loc_list.txt") 
    
    indeedClient= ApiClient(  { "fromage" : "3"    }   )    
    indeedClient.setLocation("")
    for lang in lang_names:
       q = indeedClient.buildQuery(lang) 
       num = indeedClient.getQueryResultNum("q", q ) 
       print "-----the total number language %s is %d -------" % ( lang, num)  
    
    for city in loc_list:
       indeedClient.setLocation(city) 
       for lang in lang_names:
           q = indeedClient.buildQuery(lang) 
           num = indeedClient.getQueryResultNum("q", q ) 
           print "-----the number of state %s with language %s is %d -------" % (city, lang, num) 
    
if __name__ == "__main__": 
    main()
