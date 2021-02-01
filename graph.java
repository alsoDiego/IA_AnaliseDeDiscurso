import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Vector;





public class Graph {
	
	static int c1=0,c2=0,c3=0,cmaximum=0,ccmaximum=0;
	static int [][] cycles=new int[200][3];
	static int counter=0;
	static boolean [] marcado = new boolean [10000000] 
	public static void searchCycles(int [][]edges, int[] path,int actual,int level){
		boolean repeat=false;
		for(int i=0;i<level;i++){
			if(path[i]!=0&&path[i]==actual){
				repeat=true;
				cmaximum=Math.max(cmaximum, (level-i)+1);
				if(level-i==1){
					boolean see=true;
					for(int j=0;j<counter;j++){
						if(cycles[j][0]==path[i]||cycles[j][0]==actual){
							if(cycles[j][1]==path[i]||cycles[j][1]==actual){
								if(cycles[j][2]==-1){
									see=false;
								}
							}
						}
					}
					if(see){
						cycles[counter][0]=path[i];
						cycles[counter][1]=actual;
						cycles[counter][2]=-1;
						counter++;
						c2++;
					}
				}if(level-i==2){
					boolean see=true;
					for(int j=0;j<counter;j++){
						if(cycles[j][0]==path[i]||cycles[j][0]==actual||cycles[j][0]==path[i+1]){
							if(cycles[j][1]==path[i]||cycles[j][1]==actual||cycles[j][1]==path[i+1]){
								if(cycles[j][1]==path[i]||cycles[j][1]==actual||cycles[j][1]==path[i+1]){
									see=false;
								}
							}
						}
					}
					if(see){
						cycles[counter][0]=path[i];
						cycles[counter][1]=actual;
						cycles[counter][2]=path[i+1];
						counter++;
						c3++;
					}
				}
			}
		}
		for(int i=0;i<edges.length&&!repeat;i++){
			if(edges[i][0]==actual&&!marcado[edges[i][0]]){
				path[level]=actual;
				marcado[edges[i][0]]=true;
				searchCycles(edges,path,edges[i][1],level+1);
			}
		}
	}
	public static void searchBBCycles(int [][]edges, int[] path,int actual,int level){
		boolean repeat=false;
		for(int i=0;i<level;i++){
			if(path[i]!=0&&path[i]==actual){
				repeat=true;
				ccmaximum=Math.max(ccmaximum, (level-i)+1);
				
			}
		}
		for(int i=0;i<edges.length&&!repeat;i++){
			if(edges[i][0]==actual){
				path[level]=actual;
				searchBBCycles(edges,path,edges[i][1],level+1);
			}if(edges[i][1]==actual){
				path[level]=actual;
				searchBBCycles(edges,path,edges[i][0],level+1);
			}
		}
	}
	public static double averageDegree(int [][]edges,int amount){
		int h=10000000;
		double aa=amount *1.0;
		double answer=0.0;
		boolean [] painted=new boolean[h];
		for(int i=0;i<amount;i++){
			if(painted[edges[i][0]]==false){
				painted[edges[i][0]]=true;
				answer++;
			}
			if(painted[edges[i][1]]==false){
				painted[edges[i][0]]=true;
				answer++;
			}
		}
		return aa/answer;
	}
	public static int parallelEdges(int [][]edges, int amount){
		int answer=0;
		for (int i=0;i<amount;i++){
			for(int j=i+1;j<amount;j++){
				if(edges[i][0]==edges[j][0]&&edges[i][1]==edges[j][1]){
					answer++;
				}
			}
		}
		return answer;
	}
	public static List<String> changeToNumbers(List<String> lines){
		List<String> answer= new ArrayList<String>();
		answer.add(lines.size()+"");
		Vector<String> map= new Vector<String>();
		for(int i=0;i<lines.size();i++){
			String[] line=lines.get(i).split(" ");
			if(!map.contains(line[0])){
				map.add(line[0]);
			}
			if(!map.contains(line[1])){
				map.add(line[1]);
			}
			answer.add(map.indexOf(line[0])+" "+map.indexOf(line[1]));
		}
		return answer;
		
	}
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		/*List<String> lines = Files.readAllLines(Paths.get("res/nashorn1.js"));
		lines.add("print('foobar');");
		Files.write(Paths.get("res/nashorn1-modified.js"), lines);*/
		List<String> lines = Files.readAllLines(Paths.get("graph.txt"));
		int index=0;
		//Iterator<String> it =lines.iterator();
		List<String> answer = new ArrayList<String>();
		lines=changeToNumbers(lines);
		while(index<lines.size()){
			
			String jj=lines.get(index);
			index++;
			int amount=Integer.parseInt(jj);
			int edges[][]=new int[amount][2];
			for(int i=0;i<amount;i++){
				String a=lines.get(index);
				index++;
				String split[]=a.split(" ");
				edges[i][0]=Integer.parseInt(split[0]);
				edges[i][1]=Integer.parseInt(split[1]);
			}
			for(int i=0;i<amount;i++){
				if(edges[i][0]==edges[i][1]){
					c1++;
				}
			}
			searchCycles(edges,new int[amount],edges[0][0],0);
			searchBBCycles(edges,new int[amount],edges[0][0],0);
			double degree=averageDegree(edges,amount);
			int parallel=parallelEdges(edges,amount);
		
			answer.add("Grau medio: "+degree*2);
			answer.add("Maximo componente conectado: "+ccmaximum+"");
			answer.add("Maximo componente fortemente conectado: "+cmaximum+"");
			//answer.add("Arestas paralelas"parallel+"");
			answer.add("ciclos de grau 1: "+c1+"");
			answer.add("ciclos de grau 2: "+c2+"");
			answer.add("ciclos de grau 3: "+c3+"");
			answer.add("");
			
			c1=0;c2=0;c3=0;cmaximum=0;ccmaximum=0;
			cycles=new int[200][3];
			counter=0;
			index++;
			
		}
		
		Files.write(Paths.get("cycles.txt"),answer);
	}

}