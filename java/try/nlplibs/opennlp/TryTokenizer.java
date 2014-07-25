package nlplibs.opennlp;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.tokenize.Tokenizer;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;

public class TryTokenizer  {

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub
		String modelFilePath = "java//opennlpmodels//en-token.bin";
		InputStream modelIn = new FileInputStream(modelFilePath);

		try {
			TokenizerModel model = new TokenizerModel(modelIn);
			Tokenizer tokenizer = new TokenizerME(model);
			String tokens[] = tokenizer.tokenize("An input sample sentence.");
			
		  for (String item : tokens ) {
			  System.out.println(item);
		  }
		  
		}
		catch (IOException e) {
		  e.printStackTrace();
		}
		finally {
		  if (modelIn != null) {
		    try {
		      modelIn.close();
		    }
		    catch (IOException e) {
		    }
		  }
		}
	}

}
