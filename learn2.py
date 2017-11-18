import gensim, logging
import time, math
#import kmeans
from sklearn.cluster import KMeans
from spherecluster import SphericalKMeans
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#######################Read all document vectors###########################################
count = 0
#vector = [[0 for x in range(10)] for y in range(40000)]
vector = list()
for conLine in open("vecSummary.txt"):
	if(count ==  0):
		vec=list()
		index = int(conLine)
	count += 1
	if(count ==13):
		vector.append(vec)
		count = 0
	if(count >= 3):
		vec.append(int(conLine))
###########################################################################################
######################Read all masks and prepare masks for each document###################
documents = [list() for x in range(11)]
linecount = 0
for line in open("output.csv"):
	count = 0
	linecount += 1
	if(linecount >= len(vector)):
		break
	for word in line.split(','):
		count += 1		
		if count == 2 :
			cnt = 0
			for i in word:
				if i == '1':
					documents[cnt].append(vector[linecount])
				cnt += 1
			break
###########################################################################################


##########################Save the doc2vec centroids in a file#############################
def writeDocVectorCentroids(doc_centroids, genreNum):
	filename="docCentroids"+str(genreNum)+".txt"
	centroid_file=open(filename, "w")
	centroid_file.write(str(len(doc_centroids))+"\n")
	centroid_file.write(str(len(doc_centroids[0]))+"\n")
	for cen in doc_centroids:
		for i in range(len(cen)):
			centroid_file.write(str(cen[i])+"\n")
	centroid_file.close()
############################################################################################

centroids = [list() for x in range(11)]
number_of_clusters=20
for i in range(11):
	number_of_clusters=min(number_of_clusters, len(documents[i]))
kmeans_clustering = SphericalKMeans( number_of_clusters )
for i in range(11):
	idx=kmeans_clustering.fit( documents[i])
	centroids[i]=idx.cluster_centers_
	writeDocVectorCentroids(centroids[i], i)
	print str(i) + " clustered"
	
###########################################################################################

###################################Cosine Distance#########################################
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

###########################################################################################

def get_min_dis(vec, vecs, sz):
	min_dis=1000.0
	for v in vecs:
		min_dis=min(min_dis, cosineDistance(vec, v, sz))
	return min_dis

logFile=open("genre_cluster_anaysis.txt", "w")

for i in range(11):
	max_dis=0.0
	dis_sum=0.0
	sq_dis_sum=0.0
	for num in range(len(documents[i])):
		temp_dis=get_min_dis(documents[i][num], centroids[i], len(documents[i][num]))
		max_dis=max(max_dis, temp_dis)
		dis_sum+=temp_dis
	mean_dis=(dis_sum)/len(documents[i])
	logFile.write("For genre "+str(i)+"\n")
	logFile.write("Max. dis="+str(max_dis)+"\n")
	logFile.write("Mean dis=" + str(mean_dis)+"\n")
	for num in range(len(documents[i])):
		temp_dis=get_min_dis(documents[i][num], centroids[i], len(documents[i][num]))		
		sq_dis_sum+=(temp_dis-mean_dis)*(temp_dis-mean_dis)
	sq_dis_sum/=len(documents[i])
	variance=math.sqrt(sq_dis_sum)
	logFile.write("Var. of dis=" + str(variance)+"\n")
for i in range(11):	
	for j in range(i+1, 11):
		dis_sum=0
		min_dis=10000.0
		cnt=0		
		for k in centroids[i]:
			mind=10000.0			
			for l in centroids[j]:
				temp_dis=cosineDistance(k, l, len(k))
				mind=min(mind, temp_dis)
			dis_sum+=mind
			cnt+=1
			min_dis=min(min_dis, mind)
		avg_dis=dis_sum/cnt
		logFile.write("Differentiability of genre " + str(i) +" and genre "+str(j)+":"+"\n")
		logFile.write("Worst case difference=" + str(min_dis)+"\n")
		logFile.write("Avg case difference=" + str(avg_dis)+"\n")
		

