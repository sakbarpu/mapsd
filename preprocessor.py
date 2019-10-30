
import sys, os
import glob
import fnmatch
import nltk
import regex
import string
import pickle
import csv
import numpy as np
import matplotlib.pyplot as plt
import re

__author__ = ["Shayan Ali Akbar"]
__email__ =  ["sakbar@purdue.edu"]

class Preprocessor:
    '''
	This class implements the functions for the preprocessing of content of file.
	The pipeline that we follow for preprocessing is as follows:
        (1)remove_punctuations
        (2)perform_camel_case_splitting
        (3)perform_lower_casing
        (4)remove_stopwords_using_file
        (5)perform_stemming
	'''

    def __init__(self):
        self.raw_content = None
        self.stopwords_file = None
        self.list_stopwords = None
        self.punctuation_removed_content = None
        self.camel_case_split_content = None
        self.lowercased_content = None
        self.stopword_removed_content = None
        self.stemmed_content = None
        self.current_content = None
        self.processed_content = None
        self.tokenized_content = None

    def read_stopwords(self):
        list_stopwords = []
        with open(self.stopwords_file) as f:
            for line in f:
                list_stopwords.append(line.strip())
        self.list_stopwords = list_stopwords
        return list_stopwords

    def perform_stemming(self):
        '''
		This function does the porter stemming using nltk
		ret1: the processed/stemmed content
		'''

        porter_stemmer = nltk.stem.PorterStemmer()
        # wn_lemmatizer = nltk.wordnet.WordNetLemmatizer()
        self.tokenized_content = [porter_stemmer.stem(i) for i in nltk.tokenize.word_tokenize(self.current_content)]
        # self.tokenized_content = [wn_lemmatizer.lemmatize(i) for i in nltk.tokenize.word_tokenize(self.current_content)]
        self.current_content = " ".join(self.tokenized_content)
        self.processed_content = self.current_content
        self.stemmed_content = self.current_content
        return self.stemmed_content

    def remove_stopwords_using_file(self):
        '''
		Remove all stopwords from the content
		ret1: the processed content
		'''

        content = self.current_content

        for stopword in self.list_stopwords:
            pattern = " " + stopword + " "
            content = regex.sub(pattern, " ", content)

        content = ''.join([i for i in content if not i.isdigit()])
        self.stopword_removed_content = content
        self.current_content = self.stopword_removed_content
        return self.stopword_removed_content

    def perform_lower_casing(self):
        '''
		Convert content to lower case
		ret1: processed lower cased content
		'''

        content = self.current_content
        self.lowercased_content = self.current_content.lower()
        self.current_content = self.lowercased_content
        return self.lowercased_content

    def perform_camel_case_splitting(self):
        '''
		Convert all camelcase terms into individual terms
		ret1: processed content without any camelcase terms
		'''

        content = self.current_content
        # self.camel_case_split_content = regex.sub(r'([a-z]*)([A-Z])', r'\1 \2', content)
        matches = regex.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', content, regex.DOTALL)
        self.camel_case_split_content = " ".join([m.group(0) for m in matches])
        self.current_content = self.camel_case_split_content
        return self.camel_case_split_content

    def remove_punctuations(self):
        '''
		Remove all punctuations from the contents
		ret1: The processed content
		'''

        content = self.raw_content
        self.punctuation_removed_content = "".join(l if l not in string.punctuation else " " for l in content)
        self.current_content = self.punctuation_removed_content
        return self.punctuation_removed_content

    def cleanhtml(self,raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def perform_preprocessing(self):
        self.current_content = self.raw_content
        self.punctuation_removed_content = self.remove_punctuations()
        self.camel_case_split_content = self.perform_camel_case_splitting()
        self.lowerecased_content = self.perform_lower_casing()
        #self.stopword_removed_content = self.remove_stopwords_using_file()
        self.stemmed_content = self.perform_stemming()
        self.processed_content = self.stemmed_content
