package com.jobaly.mongo;

import java.io.IOException;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.Version;

public class JobIndexBuilder {

	private StandardAnalyzer analyzer;
	private Directory index;
	private IndexWriterConfig config;
	private IndexWriter writer;	

	public StandardAnalyzer getAnalyzer() {
		return analyzer;
	}

	public void setAnalyzer(StandardAnalyzer analyzer) {
		this.analyzer = analyzer;
	}

	public void setIndex(Directory index) {
		this.index = index;
	}

	public Directory getIndex() {
		return index;
	}

	public JobIndexBuilder() throws IOException {
		analyzer = new StandardAnalyzer(Version.LUCENE_40);
		index = new RAMDirectory();
		config = new IndexWriterConfig(Version.LUCENE_40, analyzer);
		writer = new IndexWriter(index, config);
	}

	public void addDoc(Document doc) throws IOException {
		writer.addDocument(doc);
	}

	public void closeWriter() throws IOException {
		// TODO Auto-generated method stub
		writer.close();
	}

}
