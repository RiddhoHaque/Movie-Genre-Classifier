real = open("Actual_Genre")
predict = open("Genre_Predictions_1")
result = open("Result_1","w")
order = list()
orderPredict = list()
cnt = 0
res = list()
total_count = 0
count = [0.0 for count in range(11)]
for lineReal in real:
	
	if lineReal == "\n":
		cnt = 0
		cnt2 = 0
		for linePredict in predict:	
			if cnt2 == 12:
				cnt2 = 0
				res = [0 for res in range(11)]
				for i in range(11):
					for j in range(0,i+1):
						for k in range(len(order)):
							if(order[k] == orderPredict[j]):
								res[i]  = 1.0
				orderPredict = [] 
				break
			cnt2 += 1
			if cnt2==1:
				continue
			orderPredict.append(linePredict)
			
		order = []
		total_count += 1.0
		for i in range(len(res)):
			count[i] += res[i]
			sentence = "For " + str(i+1) + ": " + str(res[i]) + "\n"
#			result.write(sentence)
#		result.write("\n")
		continue
	cnt +=1	
	if cnt != 0:
		order.append(lineReal)
total_count += 1.0
for i in range(len(res)):
	count[i] += res[i]
for i in range(len(res)):
	count[i] /= total_count
	sentence = "For " + str(i+1) + ": " + str(count[i]*100) + "\n"
	result.write(sentence)
result.write("\n")
