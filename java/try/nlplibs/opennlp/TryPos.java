package nlplibs.opennlp;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;

public class TryPos {

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub
		String modelFilePath = "java//opennlpmodels//en-pos-maxent.bin";
		InputStream modelIn = new FileInputStream(modelFilePath);
		try {
			POSModel model = new POSModel(modelIn);

			POSTaggerME tagger = new POSTaggerME(model);
			String sent[] = new String[] { "Most", "large", "cities", "in",
					"the", "US", "had", "morning", "and", "afternoon",
					"newspapers", "." };
			String tags[] = tagger.tag(sent);
			for (String item : tags) {
				System.out.println(item);
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
