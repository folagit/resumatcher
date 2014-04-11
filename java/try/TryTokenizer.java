import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;

import opennlp.tools.tokenize.Tokenizer;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;

public class TryTokenizer {

	public static String readFile(String path, Charset encoding) throws IOException {
		if ( encoding == null) encoding = Charset.defaultCharset();
		byte[] encoded = Files.readAllBytes(Paths.get(path));
		return encoding.decode(ByteBuffer.wrap(encoded)).toString();
	} 
	
	public static String[] tokenize(String str, Tokenizer tokenizer){
		String tokens[] = tokenizer.tokenize(str);
		for (String token : tokens)
			System.out.println(token);
		return tokens;
	}

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub
		InputStream modelIn = new FileInputStream("en-token.bin");

		try {
			TokenizerModel model = new TokenizerModel(modelIn);
			Tokenizer tokenizer = new TokenizerME(model);
			String txt1 =   readFile("files/job_1.txt", null);
			tokenize(txt1,tokenizer);
			
		//	String txt2 =   readFile("files/job_1.html", null);
		//	tokenize(txt2,tokenizer);

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
