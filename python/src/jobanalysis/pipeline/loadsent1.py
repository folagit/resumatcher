# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 22:49:28 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from jobaly.db.dbclient import DbClient
from jobaly.ontology.ontologylib import OntologyLib
from jobdescparser import JobDescParser
from nltk.tokenize import word_tokenize
from data.datautils import dumpTwo
from  data import datautils
import operator

def getJavaScipt(): 
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")
     
     collection = newCol
     term = "javascript"
     matchingSents = []
     for job in collection.find(): 
      #   print "\n\n\n======",job["_id"],"============================\n"
        jobDesc = JobDescParser.parseJobDesc(job)
        sents = jobDesc.listAllSentences() 
        jid = job["_id"]
        for sent in sents:
            tokens = [ token.lower() for token in word_tokenize(sent)]              
            if term in tokens : 
                matchingSents.append((jid, sent))
                print sent.encode("GBK", "ignore")
                
     sortedsents = sorted(matchingSents, key=lambda x:   len(x[1]) )
     dumpTwo(sortedsents, "..\skill\output\javascript" , ( lambda x: x[0] + ":" + x[1] ) )     
 
def getSentenceByTerm(collection, term, outputPath):
    
     matchingSents = []
     for job in collection.find(): 
      #   print "\n\n\n======",job["_id"],"============================\n"
        jobDesc = JobDescParser.parseJobDesc(job)
        sents = jobDesc.listAllSentences() 
        jid = job["_id"]
        for sent in sents:
            tokens = [ token.lower() for token in word_tokenize(sent)]              
            if term in tokens : 
                matchingSents.append((jid, sent))
                print sent.encode("GBK", "ignore")
                
     sortedsents = sorted(matchingSents, key=lambda x:   len(x[1]) )
     dumpTwo(sortedsents, outputPath , ( lambda x: x[0] + ":" + x[1] ) )     
  
  # term must be low case
def testGetSentenceByTerm(term):
    
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     collection = srcBbClient.getCollection("daily_job_webdev")
     
     outputPath = '..\skill\output\\' + term
     getSentenceByTerm(collection, term, outputPath)
     

def getSentsByOntology():
     owlfile = "..\..\jobaly\ontology\web_dev.owl"
     ontology = OntologyLib(owlfile)
     terms = [ " "+ x.lower()+" " for x in ontology.getLabelList()]
     terms.extend([" "+x.lower()+" " for x in ontology.getAllClassNames()])
     
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")     
     collection = newCol
     
     matchingSents = []
     for job in collection.find(): 
      #   print "\n\n\n======",job["_id"],"============================\n"
        jobDesc = JobDescParser.parseJobDesc(job)
        sents = jobDesc.listAllSentences() 
        jid = job["_id"]
        for sent in sents:
            c = 0
            sent = " "+sent.lower()+" "
            for term in terms:                
                if sent.find(term) != -1:
                   c+=1
                if c==3 : 
                    print sent.encode("GBK", "ignore")
                    matchingSents.append((jid, sent))
                    break
              
     sortedsents = sorted(matchingSents, key=lambda x:   len(x[1]) )
     dumpTwo(sortedsents, "term3" , ( lambda x: x[0] + ":" + x[1] ) )     

def buildTerms():
     stopwordsstr = ''' 
     'd, 'll, 'm, 're, 's, 't, n't, 've, a, aboard, about, above, across, after, again, against, all, almost, alone, along, alongside, already, also, although, always, am, amid, amidst, among, amongst, an, and, another, anti, any, anybody, anyone, anything, anywhere, are, area, areas, aren't, around, as, ask, asked, asking, asks, astride, at, aught, away, back, backed, backing, backs, bar, barring, be, became, because, become, becomes, been, before, began, behind, being, beings, below, beneath, beside, besides, best, better, between, beyond, big, both, but, by, came, can, can't, cannot, case, cases, certain, certainly, circa, clear, clearly, come, concerning, considering, could, couldn't, daren't, despite, did, didn't, differ, different, differently, do, does, doesn't, doing, don't, done, down, down, downed, downing, downs, during, each, early, either, end, ended, ending, ends, enough, even, evenly, ever, every, everybody, everyone, everything, everywhere, except, excepting, excluding, face, faces, fact, facts, far, felt, few, fewer, find, finds, first, five, following, for, four, from, full, fully, further, furthered, furthering, furthers, gave, general, generally, get, gets, give, given, gives, go, goes, going, good, goods, got, great, greater, greatest, group, grouped, grouping, groups, had, hadn't, has, hasn't, have, haven't, having, he, he'd, he'll, he's, her, here, here's, hers, herself, high, high, high, higher, highest, him, himself, his, hisself, how, how's, however, i, i'd, i'll, i'm, i've, idem, if, ilk, important, in, including, inside, interest, interested, interesting, interests, into, is, isn't, it, it's, its, itself, just, keep, keeps, kind, knew, know, known, knows, large, largely, last, later, latest, least, less, let, let's, lets, like, likely, long, longer, longest, made, make, making, man, many, may, me, member, members, men, might, mightn't, mine, minus, more, most, mostly, mr, mrs, much, must, mustn't, my, myself, naught, near, necessary, need, needed, needing, needn't, needs, neither, never, new, new, newer, newest, next, no, nobody, non, none, noone, nor, not, nothing, notwithstanding, now, nowhere, number, numbers, of, off, often, old, older, oldest, on, once, one, oneself, only, onto, open, opened, opening, opens, opposite, or, order, ordered, ordering, orders, other, others, otherwise, ought, oughtn't, our, ours, ourself, ourselves, out, outside, over, own, part, parted, parting, parts, past, pending, per, perhaps, place, places, plus, point, pointed, pointing, points, possible, present, presented, presenting, presents, problem, problems, put, puts, quite, rather, really, regarding, right, right, room, rooms, round, said, same, save, saw, say, says, second, seconds, see, seem, seemed, seeming, seems, seen, sees, self, several, shall, shan't, she, she'd, she'll, she's, should, shouldn't, show, showed, showing, shows, side, sides, since, small, smaller, smallest, so, some, somebody, someone, something, somewhat, somewhere, state, states, still, still, such, suchlike, sundry, sure, take, taken, than, that, that's, the, thee, their, theirs, them, themselves, then, there, there's, therefore, these, they, they'd, they'll, they're, they've, thine, thing, things, think, thinks, this, those, thou, though, thought, thoughts, three, through, throughout, thus, thyself, till, to, today, together, too, took, tother, toward, towards, turn, turned, turning, turns, twain, two, under, underneath, unless, unlike, until, up, upon, us, use, used, uses, various, versus, very, via, vis-a-vis, want, wanted, wanting, wants, was, wasn't, way, ways, we, we'd, we'll, we're, we've, well, wells, went, were, weren't, what, what's, whatall, whatever, whatsoever, when, when's, where, where's, whereas, wherewith, wherewithal, whether, which, whichever, whichsoever, while, who, who's, whoever, whole, whom, whomever, whomso, whomsoever, whose, whosoever, why, why's, will, with, within, without, won't, work, worked, working, works, worth, would, wouldn't, ye, year, years, yet, yon, yonder, you, you'd, you'll, you're, you've, you-all, young, younger, youngest, your, yours, yourself, yourselves
     '''
     stopwords = stopwordsstr.split(", ")
     punct = '''
     , . : ' " ? / - & ( ) { } [ ] + ; ! # * & @
     '''.split()     
     digits = "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 ".split()
     # print   stopwords   
     common_nouns = '''
      etc. skills experience description proficiency ability data
      products position fundamentals content business e.g.
     '''.split()
  
     person_nouns ='''
      expert  client candidate user team developer role developers
      candidates
     '''.split()     
     
     tech_nouns = '''
     languages architecture  applications application technologies
     enterprise integration    development    
     front portal  expertise systems  pages  directory connectivity    
     microsoft  solutions   technology  markup  
     environment  scripting platform  libraries  
     
     stack soa informatica  sharepoint  ldap  computer 
     discovery lightweight  practices representational  cycle naming  
     life query portals   script servlets third   opportunity 
     patterns  level ms  management service 
     interfaces environments party  custom code      

     '''.split()
     
     
     common_jjs = '''
     hands-on strong front advanced solid minimum responsive external 
     preferred excellent based maintaining focus experienced structured
     universal extensible related unified similar senior 
     
     '''.split()
     
     common_vbs = '''
     understanding required developing using utilizing apply coding 
     please implementing modeling transfer  develop looking building
     '''.split()
     
     owlfile = "..\..\jobaly\ontology\web_dev.owl"
     ontology = OntologyLib(owlfile)
     terms = [ x.lower() for x in ontology.getLabelList()] 
     terms.extend( [ x.lower() for x in  ontology.getAllClassNames( ) ])
     words = []
     for term in terms:
         words.extend(term.split())
         
     words.extend(stopwords)
     words.extend(punct)
     words.extend(digits)
     words.extend(common_nouns)
     words.extend(common_jjs)
     words.extend(common_vbs) 
     words.extend(tech_nouns) 
     words.extend(person_nouns) 
     
     wordset = set(words)
     # print wordset
     return wordset
    
def filterTerms():    
    wordset =  buildTerms()   
    data = datautils.loadJson("term3")
    worddict = {}
    for item in data:
     #   print item
        sent = item[1]    
        sid = item[0]         
        tokens = sent.lower().split()
        for token in tokens :
            if not token in wordset:
                if worddict.has_key(token) :
                    worddict[token] += 1
                else :
                    worddict[token] = 1
                   
    sorted_x = sorted(worddict.iteritems(), key=operator.itemgetter(1))
    
    f = open("unknowns.txt", "w")
    for key, value in sorted_x:
         print key.encode("GBK", "ignore"), value
     #    f.write(key.encode("GBK", "ignore") + "  " + str( value ) + "\n" )
         f.write(key.encode("GBK", "ignore") + " "  )
  

def test_wordset():
    wordset = buildTerms()
    print wordset
    print 'and' in wordset
     
def main(): 
  #  getJavaScipt()
  #  testGetSentenceByTerm("hadoop")
  # getSentsByOntology()
 #  test_wordset()
  filterTerms()
    
if __name__ == "__main__": 
    main()   