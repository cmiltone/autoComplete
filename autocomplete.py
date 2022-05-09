"""Author: @cmiltone"""
"""
    This module does text analysis to auto complete words
    
"""
from collections import Counter
import re
from string import ascii_lowercase
import operator


#Function definitions

def freqDist(text):
        #prepare a word frequency distribution of word in the text
        word_dict = {}
        unique_words = list(set(text))
        for w in unique_words:
                if len(w) > 1:
                        word_dict.update({w:text.count(w)})

        return word_dict


def dataStructure(text):	        
        #prepare data structure
        #top level part
        longest_word_length = len(max(text, key=len))
        slots = list(range(0, longest_word_length))

        alphabet = list(ascii_lowercase)
        n = 0
        while n < longest_word_length:
                slots[n] = {key: set() for key in alphabet}
                n += 1
        
        #add word to slots...
        slots_keys = list(alphabet)
        for word in text:
                slots_key = 0
                chars = list(word)
                for char in chars:
                        if char in slots_keys and slots_key < len(slots):
                                slots[slots_key][char].add(word)
                                slots_key += 1

        return slots

        
def autoComplete(text='file.txt', word='2600-0.txt'):
        """
        generate the most likely words given a portion of the begining of the word
        and their likelihood of occurrences
        """
        ds = dataStructure(text)
        word = list(word)
        suggestions = set()
        for k in word:
                i = word.index(k)
                if not len(suggestions):
                        suggestions = ds[i][word[i]]
                else:
                        suggestions&=ds[i][word[i]]

        suggestions = [w for w in suggestions]
        occurrences = freqDist(text)
        #suggestions
        sg = dict()
        for i in suggestions:
                if i in occurrences:
                        sg.update({i:occurrences[i]})
        cummulative_freq = sum(sg.values())
        percentages = dict()
        for w in sg:
                percentages.update({w:sg[w]*100/cummulative_freq})
        
        #sort percentages
        sorted_keys = sorted(percentages.items(), key=operator.itemgetter(1), reverse=True)
        sorted_pc = dict()
        for k in sorted_keys:
                if k in percentages:
                        sorted_pc.update({k: percentages[k]})
        top5 = [sk for sk in sorted_keys][:5]
        print "Top FIVE possible words with chances of occurences as percentages:\n", top5
        
        

def main():
        #ask for text source file name
        text_source = input("Welcome. Enter the file that contains the text (within quotes e.g '2600-0.txt'):\n")
        #open file and read lines of text
        f = open(text_source)
        text = f.read()
        #strip special chars and break text into words**
        text = re.sub('[^A-Za-z0-9]+', ' ', text).lower().split()
        f.close()
        #get suggestions
        word = "cont"
        word = input("Enter beggining portion of word(in quotes e.g 'cont'):\n")
        autoComplete(text, word)
        
        print "Type 'main()' to try again, 'exit()' to quit shell."
        

if __name__ == "__main__":
    main()        
	
        
