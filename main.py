import graph as gr
esqui=[]
esqui=list(gr.getcsv("D:/Documents/Neuro/AnaliseDeDiscurso/PLN/Esquizofrenia - Analise de discurso/Entrevistas transcritas/",0,1,0))
control=list(gr.getcsv("D:/Documents/Neuro/AnaliseDeDiscurso/PLN/Estresse - Cuidadores de pacientes com parkinson - Analise de discurso/respostas/",1,0,0))
esqui.extend(control)
file = open("patient_data.txt",'w')
for line in esqui:
	file.write(str(line)+"\n")
file.close()
