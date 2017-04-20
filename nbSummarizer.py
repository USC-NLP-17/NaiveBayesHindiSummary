import nltk
import codecs
import re
import operator
import math
from tf_idf import tf_idf
from tf_isf import tf_isf
from tokenizer import *
from collections import OrderedDict
#1. Get Sentence list with Sentid
sentenceDict = {}
sentenceDictLen = {}
#sentenceDictLenTest = {}
featureVec = {}
#featureVecTest = {}
sentenceDictLabel = {}
#sentenceDictTest = {}

def print_summary(fileName,contentList):
    fileName = 'complete_corpus\\candidate_summary\\'+fileName
    f = open(fileName, "w+", encoding="utf8")

    for sentence in contentList:
        if (len(sentence.strip()) > 0):
            f.write(sentence.strip() + " " + u"\u0964" + " ")
    f.close()

def read_from_file(filename):
    f = codecs.open(filename, encoding='utf-8')
    data = f.read()
    f.close()
    return data
def merge(dict,res_idf_v,res_isf_v,sentenceDictLen_v,id):
    LocalfeatureVec = {}
    for key in dict.keys():
        #d = {"tfIsf": 0}
        d = {"tfIdf":0, "tfIsf": 0, "length": 0}  # , "label":'N'}

        if key in res_idf_v.keys():
            d["tfIdf"] = res_idf_v[key]
        if key in res_isf_v.keys():
            d["tfIsf"] = res_isf_v[key]
        if key in sentenceDictLen_v.keys():
            d["length"] = sentenceDictLen_v[key]

        LocalfeatureVec[key] = d
    return LocalfeatureVec

if __name__ == "__main__":
    no_of_inputs = 20          #No. of training files
    no_of_testSet = 20         #No. of Test files
    for x in range(1, no_of_inputs+1):
        fileContent = ''
        sentenceList = ''
        sentenceListSum = ''
        fileName = 'complete_corpus\\machine_output\\tokenized' + str(x) + ".txt"
        fileNameSummary = 'complete_corpus\\machine_output\\tokenizedSummary' + str(x) + ".txt"
        fileContent = read_from_file(fileName)
        fileContentSummary = read_from_file(fileNameSummary)
        #print("\n"+str(x) +":"+str(len(fileContent)))
        sentenceList = fileContent.split((u"।"))
        sentenceList = sentenceList[0:-1]
        sentenceListSum = fileContentSummary.split((u"।"))
        sentenceListSum = sentenceListSum[0:-1]
        no_of_sentence = len(sentenceList)
        for y in range(0,no_of_sentence):
            #multi = math.pow(10,len(str(y)))
            #sentId = str(((x * multi) + y ) / multi)
            sentId = str(x)+'.'+str(y)
            sentenceDict[sentId] = sentenceList[y]
            #sentenceDict[((x * multi) + y ) / multi] = sentenceList[y]
            if (sentenceDict[sentId] in sentenceListSum):
                sentenceDictLabel[sentId] = 'Y'
            else:
                sentenceDictLabel[sentId] = 'N'
            sentenceDictLen[sentId] = len(sentenceDict[sentId].split())
    #call for tf-idf
    res_idf = tf_idf(sentenceDict,no_of_inputs)
    #call for tf-isf
    res_isf = tf_isf(sentenceDict,no_of_inputs)
    #merge into one dictionary
    featureVec = merge(sentenceDict,res_idf,res_isf,sentenceDictLen,0)
    train = []
    for w in featureVec.keys():
        # print (featureVec[w])
        train.append((featureVec[w], sentenceDictLabel[w]))
    classifier = nltk.classify.NaiveBayesClassifier.train(train)


    #--**--TestData Set-------------------------------------
    #---**-read test data ------------------------------
    for i in range(1,no_of_testSet+1):
        testIter = 0
        count = 0
        ans = []
        test = []
        ansWithSent = {}
        sentenceDictTest = {}
        no_of_sentence_test = 0
        sentenceDictLenTest = {}
        featureVecTest = {}
        totalCountofSum = 0
        sorted_ans = []
        summary_list_sentids = []
        summary_list = []
        summaryFn = ''

        fileNameTest = 'complete_corpus\\testFile\\input' + str(i) + ".txt"
        originalTestFileList, fileContentTest = tokenize_testFile(fileNameTest)
        #originalTestFileList = read_from_file(fileNameTest)
        originalTestFileList = originalTestFileList[0:-1]

        no_of_sentence_test = len(fileContentTest)
        for y in range(0, no_of_sentence_test):
            multi = str(i)+'.'+str(y)
            sentenceDictTest[multi] = fileContentTest[y]

    # call for tf-idf
        res_idf_test = tf_idf(sentenceDictTest,1)
    # call for tf-isf
        res_isf_test = tf_isf(sentenceDictTest,1)
        for k in sentenceDictTest.keys():
            sentenceDictLenTest[k] = len(sentenceDictTest[k].split())

        featureVecTest = merge(sentenceDictTest,res_idf_test,res_isf_test,sentenceDictLenTest,1)

        for w in featureVecTest.keys():
            test.append((featureVecTest[w]))
#-----------------------------------------

        result = classifier.prob_classify_many(test)
        #result = classifier.classify_many(test)

        for res in result:
            val = 'N' if (res._prob_dict['N'])>(res._prob_dict['Y']) else 'Y'
            # print(val+'  N:'+str(i._prob_dict['N']) +'     Y:'+str(i._prob_dict['Y']))
            #if val =='Y':
            #    ansWithSent[testIter] = res._prob_dict['Y']
            ansWithSent[testIter] = res._prob_dict['Y']
            #if(val=='Y'):
            #    ans.append(originalTestFileList[testIter])
            testIter+=1
        totalCountofSum =  math.ceil(len(ansWithSent)*0.3)
        sorted_ans = sorted(ansWithSent.items(),key=operator.itemgetter(1),reverse=True)

        for sr in sorted_ans:
            #print(originalTestFileList[i[0]])
            #summary_list.append(originalTestFileList[sr[0]])
            summary_list_sentids.append(sr[0])
            count+=1
            if count >= int(totalCountofSum):
                break
        summary_list_sentids.sort()
        summaryFn = 'candidate_summary'+str(i)+'.txt'
        for sentidSorted in summary_list_sentids:
            summary_list.append(originalTestFileList[sentidSorted])
        print_summary(summaryFn,summary_list)
