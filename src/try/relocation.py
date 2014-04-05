# -*- coding: utf-8 -*-
"""
Created on Thu Apr 03 19:10:51 2014

@author: dlmu__000
"""

import urllib2

old_url = "http://www.ined.com/viewjob?jk=98a50788f8655e4d&qd=gJB6JX2hr2MB71avps3d3FWMZnGk-Xl6XWa2tn7OOd99gDZ2l1G_91taeGAyEmNCMABZ7Em3y32eygLv4Y3Fa5uHOgM4Q02BKbIOelzapB2kpj-pIiHq1WDAT_yQ0Zhf&indpubnum=3139916985086815&atk=18kl141s819ri2s6"
new_url = "http://www.indeed.com/viewjob?jk=98a50788f8655e4d&qd=gJB6JX2hr2MB71avps3d3FWMZnGk-Xl6XWa2tn7OOd99gDZ2l1G_91taeGAyEmNCMABZ7Em3y32eygLv4Y3Fa5uHOgM4Q02BKbIOelzapB2kpj-pIiHq1WDAT_yQ0Zhf&indpubnum=3139916985086815&atk=18kl141s819ri2s6"
#print url
try:
    response = urllib2.urlopen(old_url)
    #print urllib2.geturl() 
    #print response.info()
    print response.info().getheader('Location')
    the_page = response.read()
    print the_page
except urllib2.HTTPError as e:
    print e 
except urllib2.URLError as e:
    print e
except  Exception as e:
     print "Unexpected error:"