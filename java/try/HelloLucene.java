import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.FieldType;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Terms;
import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.Version;

import java.io.IOException;

public class HelloLucene {

	public static void main(String[] args) throws IOException, ParseException {
		// 0. Specify the analyzer for tokenizing text.
		// The same analyzer should be used for indexing and searching
		StandardAnalyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);

		// 1. create the index
		Directory index = new RAMDirectory();

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_40,
				analyzer);

		IndexWriter w = new IndexWriter(index, config);
		
		FieldType type = new FieldType();
		type.setIndexed(true);
		type.setStored(true);
		type.setStoreTermVectors(true);
		
		addDoc(w, type,  "Lucene in Action", "193398817");
		addDoc(w, type,  "Lucene for Dummies", "55320055Z");
		addDoc(w, type,  "Managing Gigabytes", "55063554A");
		addDoc(w, type,  "The Art of Computer Science", "9900333X");
		w.close();

		IndexReader reader = DirectoryReader.open(index);
		// query(reader);
		getTF(reader);
		reader.close();
	}

	private static void addDoc(IndexWriter w, FieldType type, String title, String isbn)
			throws IOException {
		Document doc = new Document();
		Field field = new Field("title", title, type);
		doc.add(field);
		
		// use a string field for isbn because we don't want it tokenized
		doc.add(new StringField("isbn", isbn, Field.Store.YES));
		w.addDocument(doc);
	}

	public static void getTF(IndexReader reader) throws IOException {
		for (int i = 0; i < reader.maxDoc(); i++) {
			Document doc = reader.document(i);
			String title = doc.get("title");
			System.out.println("----- docId=" + title+"-----");
			Terms terms = reader.getTermVector(i, "title");
			TermsEnum termEnum = terms.iterator(null);
			BytesRef bytesRef;

			while ((bytesRef = termEnum.next()) != null) {
				 String term = bytesRef.utf8ToString();
                 System.out.println("term: " + term );
			}

		}
	}

	public static void query(IndexReader reader) throws ParseException,
			IOException {
		// the "title" arg specifies the default field to use
		// when no field is explicitly specified in the query.
		StandardAnalyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
		// 2. query
		String querystr = "lucene";

		Query q = new QueryParser(Version.LUCENE_40, "title", analyzer)
				.parse(querystr);

		int hitsPerPage = 10;
		IndexSearcher searcher = new IndexSearcher(reader);
		TopScoreDocCollector collector = TopScoreDocCollector.create(
				hitsPerPage, true);
		searcher.search(q, collector);
		ScoreDoc[] hits = collector.topDocs().scoreDocs;

		// 4. display results
		System.out.println("Found " + hits.length + " hits.");
		for (int i = 0; i < hits.length; ++i) {
			int docId = hits[i].doc;
			Document d = searcher.doc(docId);
			System.out.println((i + 1) + ". " + d.get("isbn") + "\t"
					+ d.get("title"));
		}
	}
}
