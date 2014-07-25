package nlplibs.opennlp;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

import opennlp.tools.cmdline.parser.ParserTool;
import opennlp.tools.parser.Parse;
import opennlp.tools.parser.Parser;
import opennlp.tools.parser.ParserFactory;
import opennlp.tools.parser.ParserModel;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;

public class TryParser {

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub
		String modelFilePath = "java//opennlpmodels//en-parser-chunking.bin";
		InputStream modelIn = new FileInputStream(modelFilePath);
		try {
			ParserModel model = new ParserModel(modelIn);
			Parser parser = ParserFactory.create(model);
			
			String sentence = "The quick brown fox jumps over the lazy dog .";
			Parse topParses[] = ParserTool.parseLine(sentence, parser, 1);
			for (Parse item : topParses) {
				item.show();
			}

		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (modelIn != null) {
				try {
					modelIn.close();
				} catch (IOException e) {
				}
			}
		}
	}

}

