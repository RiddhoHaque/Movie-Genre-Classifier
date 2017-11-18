import gensim, logging
#import kmeans
from sklearn.cluster import KMeans
from spherecluster import SphericalKMeans
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
    def __init__(self, filename):
        self.filename = filename
 
    def __iter__(self):
    	for line in open(self.filename):
            yield line.split()

sentences = MySentences('PlotoutputFile.tsv')
'''
model = gensim.models.Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
model.save('/home/sdp/Downloads/Movie/mymodel')
'''
new_model = gensim.models.Word2Vec.load('/home/sdp/Downloads/Movie/mymodel')


word_vectors = new_model.wv.syn0

num_clusters = 10

# Initalize a k-means object and use it to extract centroids
#print(len(word_vectors))
#kmeans_clustering = sphericalKMeans(word_vectors, vectorSize = 20, numberOfVectors = len(word_vectors), numberOfClusters = 10)
kmeans_clustering = SphericalKMeans( n_clusters = 10 )
idx = kmeans_clustering.fit( word_vectors )
idx2 = kmeans_clustering.fit_predict( word_vectors )

##########################Save the word2vec centroids in a file#############################
centroid_file=open("wordCentroids.txt", "w")
word_centroids=idx.cluster_centers_
centroid_file.write(str(len(word_centroids))+"\n")
centroid_file.write(str(len(word_centroids[0]))+"\n")
for cen in word_centroids:
	for i in range(len(cen)):
		centroid_file.write(str(cen[i])+"\n")
centroid_file.close()
############################################################################################


file = open("vecSummary.txt","w") 
word_centroid_map = dict(zip( new_model.wv.index2word, idx2 ))
document_vectors = list()
lineNo = 0
# Go through each document

for line in open('PlotoutputFile.tsv'):	
	lineNo += 1
	total_count = 0
	context_count = [0]*10
# Go through each word                                                                              
	for word in line.split():
		total_count = total_count + 1;
		index = [ind for ind, x in enumerate(word_centroid_map.keys()) if x == word]
		if(len(index) > 0):
			context_count[word_centroid_map.values()[index[0]] ] += 1
	doc_vec=list()		
	sentence =  str(lineNo) + "\n" + str(total_count) +"\n"
	for cluster in xrange(0,10):
		doc_vec.append(100*context_count[cluster]/total_count)		
		sentence = sentence + str(100*context_count[cluster]/total_count) + "\n"
	sentence +="\n" 		
	print(sentence)		
	file.write(sentence)
	document_vectors.append(doc_vec)
file.close()


##########################Cluster the document vectors#####################################
number_of_clusters=20
kmeans_clustering = SphericalKMeans(number_of_clusters)
idx = kmeans_clustering.fit( document_vectors)
doc_centroids=idx.cluster_centers_
genreCount=[[0 for x in range(11)] for y in range(number_of_clusters)]
count=0
clusterVgenres=[[0 for x in range(11)] for y in range(number_of_clusters)]
for line in open('output.csv'):	
	parts=line.split(',')
	found = 0
	for i in range(len(parts[1])):
		if parts[1][i]=='1':
			genreCount[idx.labels_[count]][i]+=1
			if i != 3:
				found = 1
	if found :
		genreCount[idx.labels_[count]][3]-=1
	count+=1
for cluster in range(number_of_clusters):
	max_count=0
	for genres in range(11):
		max_count=max(max_count, genreCount[cluster][genres])
	for genres in range(11):
		if(genreCount[cluster][genres]==max_count): 
			clusterVgenres[cluster][genres]=1	

###########################################################################################




##########################Save the doc2vec centroids in a file#############################
centroid_file=open("docCentroids.txt", "w")
centroid_file.write(str(len(doc_centroids))+"\n")
centroid_file.write(str(len(doc_centroids[0]))+"\n")
for cen in doc_centroids:
	for i in range(len(cen)):
		centroid_file.write(str(cen[i])+"\n")
centroid_file.close()
############################################################################################


##########################Save the clusterVgenres matrix in a file#############################
centroid_file=open("clusterVsGenres.txt", "w")
toWrite=""
for i in range(number_of_clusters):
	for j in range(11):
		toWrite=toWrite+str(clusterVgenres[i][j])+" "
	toWrite+="\n"
centroid_file.write(toWrite)
centroid_file.close()
############################################################################################

