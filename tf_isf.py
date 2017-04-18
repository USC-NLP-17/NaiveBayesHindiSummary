import math
import decimal

def tf_isf(m_d):
    # main dictionary with key: sentId and value is a list of words ( Eg: key = 1.1 , value = ['hi,'hello'])
    main_dict = {}
    for k,v in m_d.items():
        main_dict[k] = v.split()
    tfFinalList = []
    df_dictionary = {}
    idf_dictionary = {}
    doc_sent_count = []
    doc_count = 0
    sent_ids=[]
    iteration = 0
    n_sentences = 0
    tf_per_sent_list = []
    idlst = []
    compare_list = ['1.1','2.1','3.1','4.1','5.1','6.1','7.1','8.1','9.1','10.1','11.1','12.1','13.1','14.1','15.1','16.1','17.1','18.1','19.1','20.1']#,'22.1','23.1','24.1','25.1']
    for k, v in main_dict.items():
        if k == '1.1':
            tf_per_sent_list = []
            iteration = iteration + 1
            n_sentences = 0
            idlst=[]
        elif k == compare_list[iteration+1]: # a new article is encountered
            sent_ids.append(idlst)#sentence ids
            tfFinalList.append(tf_per_sent_list)
            doc_sent_count.append(n_sentences)
            tf_per_sent_list = []
            iteration = iteration + 1
            n_sentences = 0
            idlst=[]
        idlst.append(k)
        n_sentences = n_sentences + 1
        tf_sent_dict = {}
        for keyword in v:
            if keyword in tf_sent_dict:
                tf_sent_dict[keyword] = tf_sent_dict[keyword] + 1
            else:
                tf_sent_dict.update({keyword:1})
        tf_per_sent_list.append(tf_sent_dict)

    sent_ids.append(idlst)#sentence ids # for the last set of documents
    tfFinalList.append(tf_per_sent_list)# for the last set of documents
    doc_sent_count.append(n_sentences)# for the last set of documents

    for sent_list in tfFinalList:
        for dicts in sent_list:
            maxtf = 0
            for w in dicts:
                if dicts[w] > maxtf:
                    maxtf = dicts[w]
            for w in dicts:
                dicts[w] = dicts[w] / float(maxtf)

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
            val1 = doc_sent_count[id] / float(1 + dict1[w])
            if val1 > 0:
                isf = math.log(val1 , 10)

            isf_dict.update({w:isf})
        id = id + 1
        isf_list.append(isf_dict)


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

    ans={}
    for i,doc in enumerate(tfFinalList):
        for j,sent in enumerate(doc):
            score=0.0
            l=len(sent)+1
            for key in sent.keys():
                score+=sent[key] # add tf_isf of words
            score/=(l*1.0)
            #ans[sent_ids[i][j]]=round(decimal.Decimal(score),4)
            ans[sent_ids[i][j]] = round(score, 4)

    return ans #sent-id : normalized total tf_isf score
