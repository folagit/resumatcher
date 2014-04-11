package test;

import java.io.IOException;
import java.net.UnknownHostException;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.util.Version;

import com.jobaly.mongo.CollectionLoader;
import com.jobaly.mongo.JobIndexBuilder;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;

public class TestBuildIndex {

	private static Document makeDoc(DBObject job) {
		Document doc = new Document();
		if (job.get("content") != null) {
			doc.add(new StringField("job_id", job.get("_id").toString(),
					Field.Store.YES));

			// use a string field for isbn because we don't want it tokenized
			doc.add(new TextField("job_title", job.get("job_title").toString(),
					Field.Store.YES));
			doc.add(new TextField("job_content", job.get("content").toString(),
					Field.Store.NO));
			return doc;
		} else
			return null;
	}
	
	public static void query(  StandardAnalyzer analyzer, Directory index , String querystr) throws ParseException, IOException {
	
	    // the "title" arg specifies the default field to use
	    // when no field is explicitly specified in the query.
	    Query q = new QueryParser(Version.LUCENE_40, "job_content", analyzer).parse(querystr);

	    // 3. search
	    int hitsPerPage = 10;
	    IndexReader reader = DirectoryReader.open(index);
	    IndexSearcher searcher = new IndexSearcher(reader);
	    TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage, true);
	    searcher.search(q, collector);
	    ScoreDoc[] hits = collector.topDocs().scoreDocs;
	    
	    // 4. display results
	    System.out.println("Found " + hits.length + " hits.");
	    for(int i=0;i<hits.length;++i) {
	      int docId = hits[i].doc;
	      Document d = searcher.doc(docId);
	      System.out.println((i + 1) + ". " + d.get("job_id") + "\t" + d.get("job_title"));
	    }

	    // reader can only be closed when there
	    // is no need to access the documents any more.
	    reader.close();
	}

	public static void main(String[] args) throws IOException, ParseException {
		// TODO Auto-generated method stub
		// TODO Auto-generated method stub
		CollectionLoader loader = new CollectionLoader("jobaly",
				"jobinfo_se_top_corps");
		DBCursor cursor = loader.loadPage(3, 10);
		JobIndexBuilder builder = new JobIndexBuilder();

		try {
			int i = 0;
			while (cursor.hasNext()) {
				i++;
				DBObject job = cursor.next();
				System.out.println(i + ":" + job.get("_id") + ":"
						+ job.get("job_title"));
				Document doc = makeDoc(job);
				if ( doc != null ) {
					builder.addDoc(doc);
				}
			}
			System.out.println("i=" + i);
		} finally {
			cursor.close();
		}
		builder.closeWriter();
		query(builder.getAnalyzer(), builder.getIndex(), "java");

	}

}
