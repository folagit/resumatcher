import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
import ConfigParser

gConfig = {}
config = ConfigParser.ConfigParser()
config.optionxform=str
config.read('app.cfg')
for key, value in config.items("all Section"):
    #print key, value
    gConfig[key] = value

print "common.py executed..."
