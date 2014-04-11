

import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;

import java.net.UnknownHostException;
import java.util.List;
import java.util.Set;

public class LoadCollection {

	public static void main(String[] args) throws UnknownHostException{
		 MongoClient mongoClient = new MongoClient();

	        // get handle to "mydb"
	        DB db = mongoClient.getDB("jobaly");

	        // Authenticate - optional
	        // boolean auth = db.authenticate("foo", "bar");
	       
	        // get a collection object to work with
	        DBCollection jobInfoCollection = db.getCollection("jobinfo_se_top_corps");
    
	       
	        // lets get all the documents in the collection and print them out
	        DBCursor cursor = jobInfoCollection.find();
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
	      
	        // release resources
	        mongoClient.close();

	}

}
