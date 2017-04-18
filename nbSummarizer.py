import nltk
import codecs
import re
import math
from tf_idf import tf_idf
from tf_isf import tf_isf
from tokenizer import *
from collections import OrderedDict
#1. Get Sentence list with Sentid
sentenceDict = {}
sentenceDictLen = {}
sentenceDictLenTest = {}
featureVec = {}
featureVecTest = {}
sentenceDictLabel = {}
sentenceDictTest = {}

def read_from_file(filename):
    f = codecs.open(filename, encoding='utf-8')
    data = f.read()
    f.close()
    return data
def merge(dict):
    LocalfeatureVec = {}
    for key in dict.keys():
        # d1 = {"length": 0}
        d = {"tfIsf": 0, "tfIdf": 0, "length": 0}  # , "label":'N'}
        if key in res_idf.keys():
            d["tfIdf"] = res_idf[key]
        if key in res_isf.keys():
            d["tfIsf"] = res_isf[key]
        if key in sentenceDictLen.keys():
            d["length"] = sentenceDictLen[key]

        LocalfeatureVec[key] = d
    return LocalfeatureVec

if __name__ == "__main__":
    no_of_inputs = 20
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
        sentenceListSum = fileContentSummary.split((u"।"))
        no_of_sentence = len(sentenceList)
        for y in range(0,no_of_sentence):
            multi = math.pow(10,len(str(y)))
            sentId = ((x * multi) + y ) / multi
            sentenceDict[sentId] = sentenceList[y]
            #sentenceDict[((x * multi) + y ) / multi] = sentenceList[y]
            if (sentenceDict[sentId] in sentenceListSum):
                sentenceDictLabel[sentId] = 'Y'
            else:
                sentenceDictLabel[sentId] = 'N'
            sentenceDictLen[sentId] = len(sentenceDict[sentId].split())
    #call for tf-idf
    res_idf = tf_idf(sentenceDict)
    #call for tf-isf
    res_isf = tf_isf(sentenceDict)
    #merge into one dictionary
    featureVec = merge(sentenceDict)

    # ----TestData Set-------------------------------------
    #read test data
    fileNameTest = 'complete_corpus\\testFile\\testInput' + str(1) + ".txt"
    #fileContentTest = read_from_file(fileNameTest)
    fileContentTest = tokenize_testFile(fileNameTest)


    no_of_sentence_test = len(fileContentTest)
    for y in range(0, no_of_sentence_test):
        multi = math.pow(10, len(str(y)))
        sentenceDictTest[((1 * multi) + y) / multi] = fileContentTest[y]

    # call for tf-idf
    res_idf_test = tf_idf(sentenceDictTest)
    # call for tf-isf
    res_isf_test = tf_isf(sentenceDictTest)
    for k in sentenceDictTest.keys():
        sentenceDictLenTest[k] = len(sentenceDictTest[k].split())


        featureVecTest = merge(sentenceDictTest)
    test = []
    for w in featureVecTest.keys():
        #print (featureVec[w])
        test.append((featureVecTest[w]))
#-----------------------------------------
    train = []
    for w in featureVec.keys():
        #print (featureVec[w])
        train.append((featureVec[w],sentenceDictLabel[w]))
    classifier = nltk.classify.NaiveBayesClassifier.train(train)
    result = classifier.prob_classify_many(test)
    #result = classifier.classify_many(test)
    print ("hi")
    #k = (' ').join(result)
    #print(k)
    for i in result:
            print('N:'+str(i._prob_dict['N']) +'     Y:'+str(i._prob_dict['Y']))

