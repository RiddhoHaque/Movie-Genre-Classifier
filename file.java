import java.util.*;
import java.net.*;
import java.io.*;


public class file{
	static boolean isAllZero(String mask){
		for(int i=0; i<mask.length(); i++){
			if(mask.charAt(i)!='0')return false; 
		}
		return true;
		//~ }

   public static void main(String args[]) throws IOException,FileNotFoundException {  
      BufferedReader indata = null;
      BufferedReader inplot = null;
      BufferedWriter out = null;
      int dataPoints=0;
      try {
		 indata = new BufferedReader(new InputStreamReader(new FileInputStream("sorted_movie_metadata.tsv"))); 
		 inplot = new BufferedReader(new InputStreamReader(new FileInputStream("sorted_summery_plot.txt"))); 
		 out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("output.csv"))); 
		 String c=null,plot=null; 
		 String arr[]; 
		 String id = null,idPlot = null; 
		 String mask; 
		 while ((plot = inplot.readLine())!=null)
		 {
				arr = plot.split("\t",2);
				idPlot=arr[0];
				plot=arr[1];
				 while ((c = indata.readLine())!=null) {
					
					arr=c.split("\t",2);
					id=arr[0];
					c=arr[1];
					if(idPlot.equals(id))break;
				}
				if(c==null)
				{
					System.out.println(id+" - "+idPlot);
					break;
				}
				System.out.println(id+" "+idPlot);
				c=c.toLowerCase(); 
				mask=""; 
				if(c.matches("(.*)history(.*)") || c.matches("(.*)documentary(.*)") || c.matches("(.*)war film(.*)") || c.matches("(.*)biograph(.*)")) mask+="1"; 
				else mask+="0"; 
				if(c.matches("(.*)comedy(.*)") || c.matches("(.*)parody(.*)") || c.matches("(.*)satire(.*)")) mask+="1"; 
				else mask+="0"; 
				if(c.matches("(.*)horror(.*)") || c.matches("(.*)supernatural(.*)")) mask+="1"; 
				else mask+="0"; 
				if(c.matches("(.*)drama(.*)") || c.matches("(.*)teen(.*)") || c.matches("(.*)romantic(.*)") || c.matches("(.*)romance(.*)") || c.matches("(.*)musical(.*)")) mask+="1"; 
				else mask+="0"; 
				if(c.matches("(.*)fantasy(.*)")) mask+="1"; 
				else mask+="0"; 
				if(c.matches("(.*)family(.*)") || c.matches("(.*)children(.*)")) mask+="1"; 
				else mask+="0"; 
				if(c.matches("(.*)action(.*)") || c.matches("(.*)sports(.*)") || c.matches("(.*)superhero(.*)")) mask+="1"; 
				else mask+="0"; 
				if(c.matches("(.*)thriller(.*)") || c.matches("(.*)crime(.*)") || c.matches("(.*)mystery(.*)")) mask+="1"; 
				else mask+="0"; 
				if(c.matches("(.*)adult(.*)") || c.matches("(.*)erotic(.*)") || c.matches("(.*)sexploitation(.*)") || c.matches("(.*)gay(.*)") || c.matches("(.*)lesbian(.*)")) mask+="1"; 
				else mask+="0"; 
				if(c.matches("(.*)science fiction(.*)") || c.matches("(.*)alien film(.*)")) mask+="1"; 
				else mask+="0"; 
				if(c.matches("(.*)adventure(.*)")) mask+="1"; 
				else mask+="0"; 
				if(isAllZero(mask)) continue; 
				out.write(id+","+mask+","+plot+"\n"); 
				out.flush(); 
				dataPoints++;
         }
      }finally {
         if (indata != null) {
            indata.close();
            inplot.close();
         }
         if (out != null) {
            out.close();
         }
         System.out.println(dataPoints);
      }
   }
}
