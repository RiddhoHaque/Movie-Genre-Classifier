import gensim
import math
#########################Loads the word vector centroids########################
cnt=0
number_of_word_centroids=0
number_of_word_dimensions=0
for line in open("wordCentroids.txt"):
	if(cnt==0):
		number_of_word_centroids=int(line)
	elif(cnt==1):
		number_of_word_dimensions=int(line)
		word_centroids=[[0 for x in range(number_of_word_dimensions)] for y in range(number_of_word_centroids)]
		row=0
		col=0
	else:
		word_centroids[row][col]=float(line)
		col+=1
		if(col==number_of_word_dimensions):
			col=0
			row+=1
	cnt+=1
##################################################################################

#########################Loads the doc vector centroids###########################
cnt=0
number_of_centroids=0
number_of_dimensions=0
for line in open("docCentroids.txt"):
	if(cnt==0):
		number_of_centroids=int(line)
	elif(cnt==1):
		number_of_dimensions=int(line)
		doc_centroids=[[0 for x in range(number_of_dimensions)] for y in range(number_of_centroids)]
		row=0
		col=0
	else:
		doc_centroids[row][col]=float(line)
		col+=1
		if(col==number_of_dimensions):
			col=0
			row+=1
	cnt+=1
##################################################################################



######################Loads the cluster vs genre matrix###########################
number_of_clusters=20
cVg=[[0 for x in range(11)] for y in range(number_of_clusters)]
row=0
col=0
for line in open("clusterVsGenres.txt"):
	for ch in line:
		if(ch!='1' and ch!='0'):
			continue
		cVg[row][col]=ch
		col+=1	
	row+=1	
	col=0
##################################################################################

####################Finds the cosine distance between two vectors#################
def cosineDistance(vector1, vector2, vectorSize):
	res=0
	norm1=0
	norm2=0    
	for i in range(vectorSize):
		res+=vector1[i]*vector2[i]
	for i in range(vectorSize):
		norm1+=vector1[i]*vector1[i]
	for i in range(vectorSize):
		norm2+=vector2[i]*vector2[i]
	norm1=math.sqrt(norm1)
	norm2=math.sqrt(norm2)
	res/=norm1
	res/=norm2	
	return math.cos(res)
##################################################################################

####################Converts a document to a vector ##############################
new_model = gensim.models.Word2Vec.load('mymodel')
def doc2vec(text):
	clusterCount = [0 for x in range(number_of_word_centroids)]
	for word in text.split(' '):
		if word not in new_model.wv.vocab:
			continue		
		mind=cosineDistance(word_centroids[0],new_model[word], number_of_word_dimensions)
		min_ind=0
		for i in range(1, number_of_word_centroids):
			temp_dis=cosineDistance(word_centroids[i],new_model[word], number_of_word_dimensions)
			if temp_dis<mind:
				mind=temp_dis
				min_ind=i
		clusterCount[min_ind]+=1
	return clusterCount
##################################################################################




##################Finds nearest centroid of a document vector####################
def getClusterInd(docVec):
	min_ind=0
	min_dis=cosineDistance(doc_centroids[0], docVec, number_of_word_centroids)	
	for i in range(1, number_of_centroids):
		temp_dis=cosineDistance(doc_centroids[i], docVec, number_of_word_centroids)
		if temp_dis<min_dis:
			min_dis=temp_dis
			min_ind=i
	return min_ind

##################################################################################

############################List of genre-names###################################
genre_name=["history/documentary/war-film/biograph", "comedy/parody/satire", "horror/supernatural", "drama/teen/romantic/romance/musical", "fantasy", "family/children", "action/sports/superhero", "thriller/crime/mystery", "adult", "science-fiction/alien", "adventure"]
###################################################################################

#################Reads testing data and predicts genre############################
def readTestData(filename):
	prediction = open("Genre_Predictions_1","w")	
	count=1
	for text in open(filename):
		docVec=doc2vec(text)
		cluster=list()		
		for i in range (number_of_clusters):
			cluster.append(cosineDistance(doc_centroids[i], docVec, number_of_word_centroids))		
		sorted_list=[i[0] for i in sorted(enumerate(cluster), key=lambda x:x[1])]
		ind=[0 for x in range(number_of_clusters)]
		for i in range(len(sorted_list)):
			ind[sorted_list[i]]=i
		priority=[0 for x in range(11)]		
		for i in range(11):
			pp=number_of_clusters+1			
			for j in range(number_of_clusters):
				if(cVg[j][i]<pp):
					pp=cVg[j][i]
			priority[i]=pp
		sorted_list=[i[0] for i in sorted(enumerate(priority), key=lambda x:x[1])]
		prediction.write(str(count)+"\n")		
		for i in sorted_list:
			print genre_name[i]
			prediction.write(genre_name[i]+"\n")		
		#for i in range(11):
		#	print("Text "+str(count)+" might be of type "+ genre_name[i])
		#	prediction.write(genre_name[i]+"\n")
		prediction.write("\n")  
		count+=1
##################################################################################

readTestData("test.txt")
