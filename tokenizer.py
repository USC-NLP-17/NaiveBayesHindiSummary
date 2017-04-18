# -*- coding: utf-8 -*-
import codecs
import re

from numpy import unicode


class Tokenizer():
    '''class for tokenizer'''

    def __init__(self, text=None):
        if text is not None:
            self.text = text
            self.clean_text()
        else:
            self.text = None
        self.sentences = []
        self.tokens = []
        self.stemmed_word = []
        self.final_list = []
        self.final_Sentences=[]
    # self.final_tokens=[]


    def read_from_file(self, filename):
        f = codecs.open(filename, encoding='utf-8')
        self.text = f.read()
        self.clean_text()

    def generate_sentences(self):
        '''generates a list of sentences'''
        text = self.text
        text = text.replace(u'?', u'।')
        self.sentences = text.split(u"।")

    def print_sentences(self, sentences=None):
        print("COUNT: ", len(self.sentences))
        if sentences:
            for i in sentences:
                print(i)
        else:
            for i in self.sentences:
                print(i)

    def clean_text(self):

        text = self.text
        text = re.sub(r'(\d+)', r'', text)
        text = text.replace('\n', '')
        text = text.replace(u',', '')
        text = text.replace(u'"', '')
        text = text.replace(u'(', '')
        text = text.replace(u')', '')
        text = text.replace(u'"', '')
        text = text.replace(u':', '')
        text = text.replace(u"'", '')
        text = text.replace(u"’", '')
        text = text.replace(u"‘", '')
        text = text.replace(u"‘‘", '')
        text = text.replace(u"’’", '')
        text = text.replace(u"''", '')
        text = text.replace(u".", '')
        self.text = text

    def remove_only_space_words(self):
        tokens = filter(lambda tok: tok.strip(), self.tokens)
        tokens = [tok for tok in self.tokens if tok.strip()]
        self.tokens = tokens

    def hyphenated_tokens(self):

        for i,each in enumerate(self.tokens):
            if '-' in each:
                tok = each.split('-')
                self.tokens.remove(each)
                self.tokens.insert(i,tok[0])
                self.tokens.insert(i+1,tok[1])

    def tokenize(self):
        '''done'''
        if not self.sentences:
            self.generate_sentences()

        sentences_list = self.sentences

        for each in sentences_list:
            tokens = []
            word_list = each.split(' ')
            tokens = tokens + word_list
            self.tokens = tokens
            # remove words containing spaces
            self.remove_only_space_words()
            # remove hyphenated words
            self.hyphenated_tokens()
            self.generate_stem_dict()
            self.remove_stop_words()
            self.formSentence()
    def print_tokens(self, print_list=None):
        '''done'''
        if print_list is None:
            for i in self.tokens:
                print(i)
        else:
            for i in print_list:
                print(i)

    def formSentence(self):
        finalSentence=""
        for word in self.final_tokens:
            finalSentence +=word+" "
        self.final_Sentences.append(finalSentence)

    def print_finalSentence(self, x,fileName):
        #fileName = 'complete_corpus\\machine_output\\tokenized' + str(x) + ".txt"
        f = open(fileName, "w+", encoding="utf8")

        for sentence in self.final_Sentences:
            if(len(sentence.strip())>0):
                f.write(sentence.strip()+" " + u"\u0964" + " ")


    def tokens_count(self):
        '''done'''
        return len(self.tokens)

    def sentence_count(self):
        '''done'''
        return len(self.sentences)

    def len_text(self):
        '''done'''
        return len(self.text)


    def generate_stem_words(self, word):
        suffixes = {
            1: [u"ो", u"े", u"ू", u"ु", u"ी", u"ि", u"ा"],
            2: [u"कर", u"ाओ", u"िए", u"ाई", u"ाए", u"ने", u"नी", u"ना", u"ते", u"ीं", u"ती", u"ता", u"ाँ", u"ां", u"ों",
                u"ें"],
            3: [u"ाकर", u"ाइए", u"ाईं", u"ाया", u"ेगी", u"ेगा", u"ोगी", u"ोगे", u"ाने", u"ाना", u"ाते", u"ाती", u"ाता",
                u"तीं", u"ाओं", u"ाएं", u"ुओं", u"ुएं", u"ुआं"],
            4: [u"ाएगी", u"ाएगा", u"ाओगी", u"ाओगे", u"एंगी", u"ेंगी", u"एंगे", u"ेंगे", u"ूंगी", u"ूंगा", u"ातीं",
                u"नाओं", u"नाएं", u"ताओं", u"ताएं", u"ियाँ", u"ियों", u"ियां"],
            5: [u"ाएंगी", u"ाएंगे", u"ाऊंगी", u"ाऊंगा", u"ाइयाँ", u"ाइयों", u"ाइयां"],
        }
        for L in 5, 4, 3, 2, 1:
            if len(word) > L + 1:
                for suf in suffixes[L]:
                    # print type(suf),type(word),word,suf
                    if word.endswith(suf):
                        # print 'h'
                        return word[:-L]
        return word

    def generate_stem_dict(self):
        '''returns a dictionary of stem words for each token'''
        # suffixes = {
        #   				1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
        #   				2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें"],
        #   				3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं"],
        #   				4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
        #   				5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
        # 			}

        stem_word = {}
        self.stemmed_word = []
        # if not self.tokens:
        #     self.tokenize()
        for each_token in self.tokens:
            # print type(each_token)
            temp = self.generate_stem_words(each_token)
            # print temp
            stem_word[each_token] = temp
            self.stemmed_word.append(temp)

        return stem_word

    def remove_stop_words(self):
        f = codecs.open("stopwords.txt", encoding='utf-8')
        self.final_tokens=[]
        # if not self.stemmed_word:
        #     self.generate_stem_dict()
        stopwords = [x.strip() for x in f.readlines()]
        # stopwords = []
        tokens = [i for i in self.stemmed_word if unicode(i) not in stopwords]
        self.final_tokens = tokens
        return tokens

def tokenize_testFile(fileName1):
    res = []
    o = Tokenizer()
    o.read_from_file(fileName1)
    o.generate_sentences()
    o.tokenize()
    for sentence in o.final_Sentences:
        if (len(sentence.strip()) > 0):
            data = sentence.strip() + " " + u"\u0964" + " "
            res.append(data)
    return res

if __name__ == "__main__":
    for x in range(1, 21):
        t = Tokenizer()
        filePath = 'complete_corpus\\input\\'
        fileName = filePath+"input"+str(x)+".txt"

        t.read_from_file(fileName)
        t.generate_sentences()
        t.tokenize()
        # t.print_tokens(t.final_tokens)
        t.print_finalSentence(x,'complete_corpus\\machine_output\\tokenized' + str(x) + ".txt")

        tSum = Tokenizer()
        filePath1 = 'complete_corpus\\human_output\\'
        fileName1 = filePath1 + "output" + str(x) + ".txt"
        tSum.read_from_file(fileName1)
        tSum.generate_sentences()
        tSum.tokenize()
        tSum.print_finalSentence(x,'complete_corpus\\machine_output\\tokenizedSummary' + str(x) + ".txt")



