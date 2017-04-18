import math
import decimal

def tf_idf(m_d): # main dictionary with key: sentId and value is a list of words ( Eg: key = 1.1 , value = ['hi,'hello'])
    #main_dict={ '1.1': [ 'hi','hello'], '2.1': [ 'hirrrr','hellrrrrro']}
    main_dict={}
    tfList = []
    tf_dictionary = {}
    df_dictionary = {}
    doc_count = 0
    score = 0.0
    for k, v in m_d.items():
        main_dict[k] = v.split()

    idf_dictionary = {}

    iteration = 0

    compare_list = ['1.1','2.1','3.1','4.1','5.1','6.1','7.1','8.1','9.1','10.1','11.1','12.1','13.1','14.1','15.1','16.1','17.1','18.1','19.1','20.1']#,'22.1','23.1','24.1','25.1']
    for k, v in main_dict.items():
        if k == '1.1':
            doc_count = doc_count + 1
            iteration = iteration + 1
            tf_dictionary = {}
        elif k == compare_list[iteration+1]: # a new article is encountered
            doc_count = doc_count + 1
            iteration = iteration + 1
            tfList.append(tf_dictionary)
            tf_dictionary = {}

        for keyword in v:
            if keyword in tf_dictionary:
                tf_dictionary[keyword] = tf_dictionary[keyword] + 1
            else:
                tf_dictionary.update({keyword:1})


    tfList.append(tf_dictionary) # for the last set of documents
    print (tfList)
    for dct in tfList:
        maxtf = 0
        for word in dct:
            if dct[word] > maxtf:
                maxtf = dct[word]
        for word in dct:
            dct[word] = dct[word] / float(maxtf)

    #print (tfList)
    print (df_dictionary)
    for dict1 in tfList:
        #print (str(dict1)+"\n")
        for j in dict1:
            #print (j)
            if j in df_dictionary:
                print ("kkkkkkk")
                df_dictionary[j] = df_dictionary[j] + 1
            else:
                df_dictionary.update({j:1})

    #print (df_dictionary)
    #print "========================"

    #print doc_count
    for word in df_dictionary:
        idf_score = 0
        val1 = (doc_count / (1 + df_dictionary[word]))
        if val1 > 0:
            idf_score = math.log(val1 , 10)

        idf_dictionary.update({word:idf_score})

    #print (idf_dictionary)

    for dict1 in tfList:
        for word in dict1:
            idf_score = idf_dictionary[word]
            val1 = dict1[word]
            val1 = val1 * idf_score
            dict1.update({word:val1})
    #return tfList
    #------------------------ tf-idf score for sentence
    #tfList	 : [{},{},{}..] each dictionary is for a doc and has (word:tf_idf)
    ans={}
    iteration = 0
    for k, v in main_dict.items():
        if k == '1.1':
            score = 0.0
            iteration = iteration + 1
        elif k == compare_list[iteration+1]: # a new article is encountered
            score = 0.0
            iteration = iteration + 1
        length = len(v)
        if length == 0:
            continue
        for keyword in v:
            if keyword in tfList[iteration - 1 ]:
                score+=tfList[iteration - 1][keyword]#add tf-idf of words of sentence
        #print (length)
        score = (score*1.0) / length #normalized
        #ans[k]=round(decimal.Decimal(score),4)
        ans[k] = round(score, 4)

    return ans #has sentId:totalTF-idfScore key-val pair
