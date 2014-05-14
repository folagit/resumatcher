from common import  * 

def main(): 

  # print gConfig
   dbClient = DbClient('localhost', 27017, "jobaly")    
   dbClient.copyToCollection(gConfig["srcJobInfoCollName"], gConfig["webJobInfoCollName"],20)
    
if __name__ == "__main__": 
    main()
