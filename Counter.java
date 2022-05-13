import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;

public class Counter {
	//需统计的文件
	private static File basefile = new File("nlpcc2016test_ans.dat"); 
	private static File basefile2= new File("nlpcc2016dev.dat");
	private static File basefile3 = new File("nlpcc2016train.dat");
	private static File[] baselist = {basefile3,basefile2,basefile};
	//训练集中单词集合
	private static HashSet<String> wordtrain = new HashSet<String>();
	public static void main(String[] args) {	
		try {
			Counters(baselist);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	
	public static void Counters(File[] trainfile) throws IOException{
		int totsent = 0;  //计算句子数
		int totword = 0; //计算词数
		int totchars = 0; // 计算字符数
		int devmiss = 0;  //计算dev中未出现在train的词数
		int testmiss = 0;	// 计算test中未出现在train的词数
		HashSet<String> wordtotal = new HashSet<String>(); //总词集合
		HashSet<Character> chartotal = new HashSet<Character>(); //总字符集合
		int k = 0;
		for(File files: trainfile){
			BufferedReader bufreader = new BufferedReader(new FileReader(files));
			String line = null;
			int sent = 0;
			int word = 0;
			int chars = 0;
			HashSet<String> wordtmp = new HashSet<String>();
			HashSet<Character> chartmp = new HashSet<Character>();
			while((line = bufreader.readLine())!=null){
				sent ++;
				totsent++;
				String[] words = line.split("\\s");
				word += words.length;
				totword += words.length;
				for(String wd:words){
					int lg = wd.length();
					chars += lg;
					totchars += lg;
					wordtotal.add(wd);
					wordtmp.add(wd);
					if(k==0){
						wordtrain.add(wd);
					}else if(k==1){
						if(wordtrain.contains(wd)==false){
							devmiss++;
						}
					}else if(k==2){
						if(wordtrain.contains(wd)==false){
							testmiss++;
						}
					}
					for(int i=0;i<lg;i++){
						chartotal.add(wd.charAt(i));
						chartmp.add(wd.charAt(i));
					}
				}
			}
			bufreader.close();
			System.out.println(files.getName()+":");
			System.out.println("句子数："+sent);
			System.out.println("词数："+word);
			System.out.println("字符数："+chars);
			System.out.println("词集合："+wordtmp.size());
			System.out.println("字符集合："+chartmp.size());
			if(k==1){
				System.out.println("oov:" + devmiss*1.0/word);
			}else if(k==2){
				System.out.println("oov:" + testmiss*1.0/word);
			}
			k++;
		}
			System.out.println("总和：");
			System.out.println("总体句子数："+totsent);
			System.out.println("总体词数："+totword);
			System.out.println("总体字符数："+totchars);
			System.out.println("总体词集合："+wordtotal.size());
			System.out.println("总体字符集合："+chartotal.size());
	}
}