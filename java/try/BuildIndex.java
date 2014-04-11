import java.io.IOException;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.Version;


public class BuildIndex {
	 private StandardAnalyzer analyzer;
	 private Directory index;
	 private IndexWriterConfig config;
	 private IndexWriter writer;
	 
	 public Directory getIndex() {
		return index;
	}



	private QueryParser queryParser;
	 
	 public BuildIndex() throws IOException{
		 analyzer = new StandardAnalyzer(Version.LUCENE_40);
		 index = new RAMDirectory();
		 config = new IndexWriterConfig(Version.LUCENE_40, analyzer);
		 writer = new IndexWriter(index, config);
		 queryParser = new  QueryParser(Version.LUCENE_40, "title", analyzer);
	 }
	 
	 public void addDoc(Document doc) throws IOException{
		 writer.addDocument(doc);
	 }
	 
	 public void closeWriter() throws IOException {
	// TODO Auto-generated method stub
		  writer.close();
	 }
	  
	 public Query createQuery(String querystr) throws ParseException {
		 return queryParser.parse(querystr);
	 }
	
	 public static void main(String[] args) throws IOException, ParseException {
		   
		 BuildIndex builder = new  BuildIndex();
		  
		 builder.addDoc(makeDoc ( "Lucene in Action", "193398817"));
		 builder.addDoc(makeDoc (  "Lucene for Dummies", "55320055Z"));
		 builder.addDoc(makeDoc (  "Managing Gigabytes", "55063554A"));
		 builder.addDoc(makeDoc ( "The Art of Computer Science", "9900333X"));
		 builder.closeWriter();

		    // 2. query
		    String querystr = args.length > 0 ? args[0] : "lucene";

		    // the "title" arg specifies the default field to use
		    // when no field is explicitly specified in the query.
		    Query q = builder.createQuery(querystr);

		    // 3. search
		    int hitsPerPage = 10;
		    IndexReader reader = DirectoryReader.open(builder.getIndex());
		    IndexSearcher searcher = new IndexSearcher(reader);
		    TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage, true);
		    searcher.search(q, collector);
		    ScoreDoc[] hits = collector.topDocs().scoreDocs;
		    
		    // 4. display results
		    System.out.println("Found " + hits.length + " hits.");
		    for(int i=0;i<hits.length;++i) {
		      int docId = hits[i].doc;
		      Document d = searcher.doc(docId);
		      System.out.println((i + 1) + ". " + d.get("isbn") + "\t" + d.get("title"));
		    }

		    // reader can only be closed when there
		    // is no need to access the documents any more.
		    reader.close();
		  }



		private static Document makeDoc( String title, String isbn)  {
		    Document doc = new Document();
		    doc.add(new TextField("title", title, Field.Store.YES));

		    // use a string field for isbn because we don't want it tokenized
		    doc.add(new StringField("isbn", isbn, Field.Store.YES));
		    return doc;
		  }
}
