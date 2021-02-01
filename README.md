# IA - Análise de Discurso

## Sistema

​	O sistema será desenvolvido usando uma combinação de softwares em Java e em Python, fazendo uso da biblioteca de processamento de linguagem natural NLTK e do pacote de manipulação de grafos *networkx*, entre outras tecnologias.

​	A maior parte do sistema roda automaticamente, o usuário não interage com os softwares em Java, e somente com três scripts em Python. Através desses scripts, podemos dividir o manuseio de dados em fases:

![image](https://user-images.githubusercontent.com/68669255/106465305-8e3abf80-6478-11eb-94dd-7900dfdc62f1.png)

## Objetivo

![image](https://user-images.githubusercontent.com/68669255/106465769-305aa780-6479-11eb-995a-f8ff135a1c48.png)



## Preparação dos dados

​	Ao receber o discurso do paciente em formato “.txt” o programa faz um pré-processamento para remoção de *stopwords*, e depois realiza *stemming*:



- Tokenização do texto: remoção de pontos, vírgulas, quebra de linhas, o, a, os, as;
- Stemming: redução do termo ao seu radical.



## Análise Emocional

​	Na análise de sentimentos, o programa tokeniza o texto por frases conforme o padrão do NLTK. Depois tokeniza cada uma das frases individualmente, gerando assim uma matriz de frases e palavras.

​	Após isso, estas frases são comparadas com o léxico para extrair o cunho emocional de palavras no texto em vetores de oito dimensões, uma para cada emoção: *anger**,* *anticipation**,* *disgust**,* *fear**,* *joy,sadness**,* *surprise**,* *trust*.



## Parâmetros de IA

​	Para a análise, oito classificadores foram utilizados:

- K- neighbors;
- Support Vector Classifier (SVC);
- Árvore de Decisão;
- Random Forest;
- MLP;
- Gaussian NB;
- QDA



## Resultados

​	Todos devem dar um valor entre 0 (zero) e 1 (um) para cada frase que analisarem. Zero indica 100% de certeza que o paciente está doente, e um indica 100% de certeza que ele está saudável.