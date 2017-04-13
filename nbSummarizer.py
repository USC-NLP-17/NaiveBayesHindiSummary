import codecs
import re
#1. Get Sentence list with Sentid

def read_from_file(self, filename):
    f = codecs.open(filename, encoding='utf-8')
    self.text = f.read()
    self.clean_text()

if __name__ == "__main__":
    for x in range(1, 21):
        fileName = 'complete_corpus\\machine_output\\tokenized' + str(x) + ".txt"
        #fileName = filePath+"input"+str(x)+".txt"
        read_from_file(fileName)