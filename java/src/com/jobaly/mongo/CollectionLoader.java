package com.jobaly.mongo;

import java.net.UnknownHostException;

import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.MongoClient;

public class CollectionLoader {
	
	private  MongoClient mongoClient;
	private  DB db;
	private  DBCollection collection;
	
	public CollectionLoader(String dbName, String CollName) throws UnknownHostException {
		    mongoClient = new MongoClient();
            db = mongoClient.getDB("jobaly");	         
            collection= db.getCollection("jobinfo_se_top_corps"); 
	}
	
	public DBCursor loadPage(int pageNo, int pageSize) {
		DBCursor cursor = collection.find();
		cursor.skip(pageSize * pageNo );
		cursor.limit(pageSize);
		return cursor;
	}

	public static void main(String[] args) throws UnknownHostException {
		// TODO Auto-generated method stub
		CollectionLoader loader = new CollectionLoader("jobaly", "jobinfo_se_top_corps");
		DBCursor cursor  = loader.loadPage(3,10);
		
		try {
        	int i = 0;
            while (cursor.hasNext()) {
                System.out.println(cursor.next());
                i++;
            }
            System.out.println("i=" + i);
        } finally {
            cursor.close();
            
        }
      
	}

}
