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
number_of_centroids=[0 for x in range(11)]
number_of_dimensions=[0 for x in range(11)]
fg=False
for i in range(11):
	cnt=0
	row=0
	col=0
	fileName="docCentroids"+str(i)+".txt"
	for line in open(fileName):		
		if(cnt==0):
			number_of_centroids[i]=int(line)
		elif(cnt==1):
			number_of_dimensions[i]=int(line)
			row=0
			col=0
			if fg== False:
				fg=True
				doc_centroids=[[[0 for x in range(number_of_dimensions[0])] for y in range(number_of_centroids[0])] for z in range(11)]
		else:
			print str(i) +" " + str(row)+ " "+ str(col) + " "+str(line)			
			doc_centroids[i][row][col]=float(line)
			col+=1
			if(col==number_of_dimensions[i]):
				col=0
				row+=1
		cnt+=1
print doc_centroids
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
	if norm1!=0:
		res/=norm1
	if norm2!=0:
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




##################Finds distance to nearest centroid of a document vector#########
def getClusterInd(docVec, ind):
	min_ind=0
	min_dis=cosineDistance(doc_centroids[ind][0], docVec, number_of_word_centroids)		
	for i in range(1, number_of_centroids[ind]):
		temp_dis=cosineDistance(doc_centroids[ind][i], docVec, number_of_word_centroids)
		if temp_dis<min_dis:
			min_dis=temp_dis
			min_ind=i
	return min_dis

##################################################################################

############################List of genre-names###################################
genre_name=["history/documentary/war-film/biograph", "comedy/parody/satire", "horror/supernatural", "drama/teen/romantic/romance/musical", "fantasy", "family/children", "action/sports/superhero", "thriller/crime/mystery", "adult", "science-fiction/alien", "adventure"]
##################################################################################

#################Reads testing data and predicts genre############################
def readTestData(filename):
	file1=open("Genre_Predictions", "w")
	file2=open("Prediction Analysis", "w")	
	count=0
	for text in open(filename):
		count += 1
		file1.write(str(count)+"\n")
		cluster=list()		
		docVec=doc2vec(text)
		for i in range (11):
			cluster.append(getClusterInd(docVec, i))
		sorted_list=[i[0] for i in sorted(enumerate(cluster), key=lambda x:x[1])]
		for i in range(len(cluster)):
			print genre_name[i]+" "+str(cluster[i])
			file2.write(genre_name[i]+" "+str(cluster[i])+"\n")		
		for i in sorted_list:
			print genre_name[i]
			file1.write(genre_name[i]+"\n")		
		print "\n"
		file1.write("\n")
		file2.write("\n")
##################################################################################

readTestData("test.txt")
