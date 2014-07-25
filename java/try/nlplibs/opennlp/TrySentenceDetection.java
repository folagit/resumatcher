package nlplibs.opennlp;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;

public class TrySentenceDetection {

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub
		String modelFilePath = "java//opennlpmodels//en-sent.bin";
		InputStream modelIn = new FileInputStream(modelFilePath);

		try {
		  SentenceModel model = new SentenceModel(modelIn);
		  SentenceDetectorME sentenceDetector = new SentenceDetectorME(model);
		  String sentences[] = sentenceDetector.sentDetect("  First sentence. Second B.S. U.S. sentence. ");
		  
		  for (String sent : sentences ) {
			  System.out.println(sent);
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
