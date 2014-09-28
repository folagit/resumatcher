# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 15:42:46 2014

@author: dlmu__000
"
"""
import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient
from jobdescparser import JobDescParser, JobDesc
from nltk.tokenize import sent_tokenize, word_tokenize
import json
from pattern.en import parse, Text, Sentence

def dumpToText(listObj, fileName, lam):
     with open(fileName, "w") as f:
         for item in listObj:              
             line = lam(item) + "\n"
         #    print line.encode("GBK", "ignore")
             f.write(line.encode('utf8'))
         
def dumpToJson(listObj, fileName):
     with open(fileName, "w") as f:
         json.dump(listObj, f)
     
def dumpTwo(listObj, fileName , lam):
    txtFileName = fileName+".txt"
    jsonFileName = fileName+".json"
    dumpToText(listObj, txtFileName , lam)
    dumpToJson(listObj, jsonFileName)
    
def getAllSentsInColl(collection):
    allSents = []
    for job in collection.find(): 
        print "\n\n\n======",job["_id"],"============================\n"
        jobDesc = JobDescParser.parseJobDesc(job)
        sents = [ (  jobDesc._id, sent )  for sent in  jobDesc.listAllSentences() ]
        allSents.extend(sents)  
    return allSents    
    
def termsMatching(allSents,terms):
    matchingSents =[]
    for (jid, sent) in allSents:
        tokens = [ token.lower() for token in word_tokenize(sent)]
        for term in  terms:      
            if term in tokens : 
                matchingSents.append((jid, sent))
                break
    return  matchingSents      
    
def termMatching(allSents,term):    
    matchingSents =[]
    for (jid, sent) in allSents:
        print sent
        tokens = [ token.lower() for token in word_tokenize(sent)]
        if term in tokens : 
            matchingSents.append((jid, sent))
    return  matchingSents  
 
def testGetAllSents():    
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")       
     allSents =  getAllSentsInColl(newCol) 
     dumpTwo(allSents, "sents\web_dev_sents_2" , ( lambda x: x[0] + ":" + x[1] ) )     
  

def testTermMatching():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")       
     allSents =  getAllSentsInColl(newCol) 
     
     term = "experience"
     term = "knowledge"
     term = "skills"
     term = "degree"
     matchingSents = termMatching(allSents,term)     
     dumpTwo(matchingSents, "sents\\matching_"+ term , ( lambda x: x[0] + ":" + x[1] ) )     
    
def testTermsMatching():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")
     newCol = srcBbClient.getCollection("daily_job_info_2014-06-16")
     newCol = srcBbClient.getCollection("daily_job_info_2014-06-10")
      
     print "newCol=" ,newCol
     allSents =  getAllSentsInColl(newCol) 
     
     terms = ["degree", "B.S.", "M.S." ,"BS", "MS", "bachelor", "master", "phd","master's"]
     matchingSents = termsMatching(allSents,terms)     
   #  dumpTwo(matchingSents, "sents\\degree_raw" , ( lambda x: x[0] + ":" + x[1] ) )  
     dumpTwo(matchingSents, "sents\\degree_0610" , ( lambda x: x[0] + ":" + x[1] ) )     
  
import   operator
def wordStat():
    fileName = "sents\\matching_muldegree2.json"
    f = open(fileName, "r") 
    data = json.load(f)
  #  print data 
    tokenStat = {}
    for item in data:
        line = item[1]
        tokens = line.split()
        for token in tokens:
            if tokenStat.has_key(token):
                tokenStat[token]+=1
            else:
                tokenStat[token] = 1
    
    outFileName = "sents\\degreestat_2.txt"
    outifile =  open(outFileName, "w")            
    for (key, value) in sorted(tokenStat.iteritems(), key=operator.itemgetter(1), reverse = True):
        print key.encode("GBK", "ignore"), value
        outifile.write(key.encode('utf8')+" : " + str(value) + "\n")

def findVerb(sent):
    result = parse(sent,tokenize = True, tags = True, )
    sen = Sentence(result) 
    vlist = [ word.string for word in sen if word.type.startswith("V") ]
    print vlist
    vlist = [ word.string for word in sen if word.type.startswith("V") ]
    return vlist

def verbStat():
    fileName = "sents\\matching_muldegree_3.json"
    f = open(fileName, "r") 
    data = json.load(f)
  #  print data 
    tokenStat = {}
    for item in data:
        line = item[1]
        tokens = findVerb(line)
        for token in tokens:
            if tokenStat.has_key(token):
                tokenStat[token]+=1
            else:
                tokenStat[token] = 1
    
    outFileName = "sents\\degree_verb_stat_3.txt"
    outifile =  open(outFileName, "w")            
    for (key, value) in sorted(tokenStat.iteritems(), key=operator.itemgetter(1), reverse = True):
        print key.encode("GBK", "ignore"), value
        outifile.write(key.encode('utf8')+" : " + str(value) + "\n")
  
  
def main(): 
   # testParseAll()
  #  wordStat()
   testTermsMatching()
    
if __name__ == "__main__": 
    main()   