
import re
import math
import decimal
from collections import OrderedDict

tf_isf_feature = []

def tf_isf(m_d,total_files):
	tfFinalList = []
	df_dictionary = {}
	idf_dictionary = {}
	doc_sent_count = []
	doc_count = 0
	sent_ids=[]
	number = 0
	main_dict=OrderedDict()
    for k,v in m_d.items():
       main_dict[k]=v.split()
	while number < total_files:
            number = number + 1
	    tf_per_sent_list = []
	    n_sentences = 0
	    idlst=[]
	    for k, v in main_dict.items():
		if str(k).startswith(str(number)):
					idlst.append(k)
					n_sentences = n_sentences + 1
					tf_sent_dict = {}
					for keyword in v:
						if keyword in tf_sent_dict:
							tf_sent_dict[keyword] = tf_sent_dict[keyword] + 1
						else:
							tf_sent_dict.update({keyword:1})
					tf_per_sent_list.append(tf_sent_dict)
	   sent_ids.append(idlst)#sentence ids
	   tfFinalList.append(tf_per_sent_list)
	   doc_sent_count.append(n_sentences)

	for sent_list in tfFinalList:
		for dicts in sent_list:
			maxtf = 0
			for w in dicts:
				if dicts[w] > maxtf:
					maxtf = dicts[w]
			for w in dicts:
				dicts[w] = (dicts[w] / float(maxtf))

	sf_list = []

	for sent_list in tfFinalList:
		sf = {}
		for dicts in sent_list:
			for w in dicts:
				if w in sf:
					sf[w] = sf[w] + 1
				else:
					sf.update({w:1})
		sf_list.append(sf)

	isf_list = []

	id = 0
	for dict1 in  sf_list:
		isf_dict = {}
		for w in dict1:
			isf = 0.0
			val1 =0.0
			val1 = float(doc_sent_count[id] / float(1 + dict1[w]))
			if val1 > 0:
				isf = math.log(val1 , 10)

			isf_dict.update({w:isf})
		id = id + 1
		isf_list.append(isf_dict)


	#print isf_list[0]

	id = 0
	for doc in tfFinalList:
		for sentdic in doc:
			for w in sentdic:
				isf_dict = isf_list[id]
				if w in isf_dict:
					sentdic[w] = sentdic[w] * isf_dict[w]
				else:
					sentdic[w] = 0
	id = id + 1
        ans=OrderedDict()
	#tf_isf_feature
	#[[{},{},{}..],[],[],..]
	#list which contains list of dictionaries.
	# the list represents a whole chunk
	# the sublist represent a doc
	# the dictionaries have (word:tf-isf) key-pair
	for i,doc in enumerate(tfFinalList):
		for j,sent in enumerate(doc):
			score=0.0
			l=len(sent)+1
			for key in sent.iterkeys():
				score+=sent[key] # add tf_isf of words
			score/=(l*1.0)
			ans[sent_ids[i][j]]=round(decimal.Decimal(score),4)

	return ans #sent-id : noralized total tf_isf score
