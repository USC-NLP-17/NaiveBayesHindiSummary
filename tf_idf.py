import math
import decimal
from collections import OrderedDict
main_dict= OrderedDict()
# def tf_idf(m_d): # main dictionary with key: sentId and value is a list of words ( Eg: key = 1.1 , value = ['hi,'hello'])
#     #main_dict={ '1.1': [ 'hi','hello'], '2.1': [ 'hirrrr','hellrrrrro']}
#     main_dict={}
# 	 #has sentId:totalTF-idfScore key-val pair
#for k,v in m_d.items():
#    main_dict[k]=v.split()
#main_dict['1.1']=['cat','dog','rat','horse','monkey','cat']
#main_dict['2.1']=['dog','dog','rat','horse','monkey','eagle','cat']
#main_dict['3.1']=['horse','dog','rat','horse','monkey','eagle','cat']
tfList = []
tf_dictionary = {}
df_dictionary = {}
idf_dictionary = {}
doc_count = 0
iteration = 0
number = 0
#compare_list = ['1.1','2.1','3.1','4.1','5.1','6.1','7.1','8.1','9.1','10.1','11.1','12.1','13.1','14.1','15.1','16.1','17.1','18.1','19.1','20.1','22.1','23.1','24.1','25.1']
while number < 3:
        number = number + 1
        tf_dictionary= {}
        for k, v in main_dict.items():
            if k.startswith(str(number)):
                #print k
                for keyword in v:
                    if keyword in tf_dictionary:
                        tf_dictionary[keyword] = tf_dictionary[keyword] + 1
                    else:
                        tf_dictionary.update({keyword:1})
        tfList.append(tf_dictionary)

#print tfList
for dct in tfList:
    maxtf = 0
    for word in dct:
        if dct[word] > maxtf:
            maxtf = dct[word]
    for word in dct:
        #print str(word)+" "+str(dct[word])
        dct[word] = dct[word] / float(maxtf)

for dict1 in tfList:
    for j in dict1:
        if j in df_dictionary:
            df_dictionary[j] = df_dictionary[j] + 1
        else:
            df_dictionary.update({j:1})

print df_dictionary
print "========================"

doc_count = 3

for word in df_dictionary:
    print word+" "+str(df_dictionary[word])
    idf_score = 0.0
    val1=0.0
    val1 = float(doc_count/float(1 + df_dictionary[word]))
    print val1
    if val1 > 0:
        idf_score = math.log(val1 , 10)

    idf_dictionary.update({word:idf_score})

print len(idf_dictionary)

for dict1 in tfList:
    for word in dict1:
        idf_score = idf_dictionary[word]
        val1 = dict1[word]
        val1 = val1 * idf_score
        dict1.update({word:val1})
#return tfList
#------------------------ tf-idf score for sentence
#tfList	 : [{},{},{}..] each dictionary is for a doc and has (word:tf_idf)
ans=OrderedDict()
number = 0
while number < 3:
        number = number + 1
        score = 0.0
        for k, v in main_dict.items():
            if k.startswith(str(number)):
                length = len(v)
                for keyword in v:
                    if keyword in tfList[number- 1]:
        				score+=tfList[number- 1][keyword]#add tf-idf of words of sentence
                score = score*(1.0/length) #normalized
                ans[k]=round(decimal.Decimal(score),4)

print ans
