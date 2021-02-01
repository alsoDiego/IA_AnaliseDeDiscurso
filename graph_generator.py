import graph as gr
import networkx as nx

esquizofrenia="fechou as 5 empresas e então a geração de renda e as pessoas que moravam lá eu conheço bem porque eu cresci lá são muito pequenas, são pequenas de personalidade."
control= "aí eu disse pra menina que estava comigo, eu estou vendo tudo pela metade, ela disse oxente, eu disse é... ela me deu a agenda pra eu ligar pro pessoal que ligou pra mim."
esquizofrenia = gr.prepare(esquizofrenia)
control=gr.prepare(control)
Esquigraph = gr.generateGraph(esquizofrenia)
Controlgraph = gr.generateGraph(control)
file = open("graph_visualization.txt",'w')
nodes=[]
for i in Esquigraph.edges:
	string1 = ""
	string2	= ""
	node1 = i[0]
	node2 = i[1]
	if not(node1 in nodes):
		nodes.append(node1)

	string1 = str(nodes.index(node1)+1)

	if not(node2 in nodes):
		nodes.append(node2)

	string2 = str(nodes.index(node2)+1)

	file.write(string1+"-"+string2+",")


file.write(str(len(Esquigraph.edges))+"\n")

nodes=[]
for i in Controlgraph.edges:
	string1 = ""
	string2	= ""
	node1 = i[0]
	node2 = i[1]
	if not(node1 in nodes):
		nodes.append(node1)

	string1 = str(nodes.index(node1)+1)

	if not(node2 in nodes):
		nodes.append(node2)

	string2 = str(nodes.index(node2)+1)

	file.write(string1+"-"+string2+",")


file.write(str(len(Controlgraph.edges))+"\n")

file.close()