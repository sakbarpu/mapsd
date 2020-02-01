import sys, os
import itertools
import numpy
from preprocessor import Preprocessor

import gensim
from gensim.models import Phrases
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models import LdaMulticore

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from pprint import pprint

class LineSentences:
        '''
        The purpose of this class is to read sentences/documents from a single file.
        The format of the file is such that each document is on a separate line.

        '''

        def __init__(self, inpath):

                self.infile = open(inpath, encoding="iso-8859-15")

        def __iter__(self):

                self.infile.seek(0)
                for line in itertools.islice(self.infile, None):
                        yield line

        def __len__(self):
                self.infile.seek(0)
                c = 0
                for line in itertools.islice(self.infile, None):
                        c+=1
                return c

        def __getitem__(self, key):
                self.infile.seek(0)
                if type(key) is int:
                        return next(itertools.islice(self.infile, key, key+1))
                elif type(key) is tuple:
                        tmp = []
                        for x in itertools.islice(self.infile, key[0], key[1]):
                                tmp.append(x)
                        return tmp

out_path = sys.argv[1] #output dir
stop_words = set(stopwords.words("english"))

docs = LineSentences(os.path.join(out_path,"RANDOM_DOCS"))

# Tokenize the documents.

# Split the documents into tokens.
tokenizer = RegexpTokenizer(r'\w+')
docs = [tokenizer.tokenize(doc) for doc in docs]

# Remove numbers, but not words that contain numbers.
docs = [[token for token in doc if not token.isnumeric()] for doc in docs]

# Remove words that are only one character.
docs = [[token for token in doc if len(token) > 1] for doc in docs]

# Compute bigrams.

# Add bigrams and trigrams to docs (only ones that appear 20 times or more).
bigram = Phrases(docs, min_count=20)
for idx in range(len(docs)):
	for token in bigram[docs[idx]]:
		if '_' in token:
			# Token is a bigram, add to document.
			docs[idx].append(token)

# Remove rare and common tokens.

# Create a dictionary representation of the documents.
dictionary = Dictionary(docs)

# Filter out words that occur less than 20 documents, or more than 50% of the documents.
dictionary.filter_extremes(no_below=20, no_above=0.5)

# Bag-of-words representation of the documents.
corpus = [dictionary.doc2bow(doc) for doc in docs]

print('Number of unique tokens: %d' % len(dictionary))
print('Number of documents: %d' % len(corpus))

# Train LDA model.

# Set training parameters.
num_topics = 200
chunksize = 2000
passes = 20
iterations = 100
eval_every = None  # Don't evaluate model perplexity, takes too much time.

# Make a index to word dictionary.
temp = dictionary[0]  # This is only to "load" the dictionary.
id2word = dictionary.id2token

model = LdaModel.load("/home/ubuntu/mnt/cloudNAS2/SoftKBase/mapsd/data/topics/preprocessed_data/preprocessed_data/lda_RANDOM_DOCS_model/lda_model")

#top_topics = model.top_topics(corpus) #, num_words=20)

# Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
#avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
#print('Average topic coherence: %.4f.' % avg_topic_coherence)

#pprint(top_topics)
#print (top_topics)

def get_doc_topics(lda, bow):
	gamma, _ = lda.inference([bow])
	topic_dist = gamma[0] / sum(gamma[0])  # normalize distribution
	return [(topicid, topicvalue) for topicid, topicvalue in enumerate(topic_dist)]

def get_top_topics_only(topic_dist):
	top_topics = []
	count = 0
	max_topic = ("",float("-inf"))
	for topic,value in topic_dist:
		if value > max_topic[1]:
			max_topic = (topic,value)
	return max_topic

topics_all_docs = []
with open(os.path.join(out_path,"all_docs_topics.txt"),'w') as f:
	for i in range(len(docs)):
		if i%1000 == 0: print (i,'/',len(docs))
		#print ("\n")
		#predict a topic for a document
		important_words = docs[i]
		#print (important_words)
		#print (len(important_words))

		ques_vec = []
		ques_vec = dictionary.doc2bow(important_words)
		#print ("ques_vec", ques_vec)
		
		t,v = get_top_topics_only(get_doc_topics(model,ques_vec))
		#topics_all_docs.append((t,v))

		#topic_vec = []
		#topic_vec = model[ques_vec]
		#print ("topic_vec", topic_vec)
		

		#word_count_array = numpy.empty((len(topic_vec), 2), dtype = numpy.object)
		#for i in range(len(topic_vec)):
		#	word_count_array[i, 0] = topic_vec[i][0]
		#	word_count_array[i, 1] = topic_vec[i][1]

		#print ("word count array")
		#print (word_count_array)

		#idx = numpy.argsort(word_count_array[:, 1])
		#idx = idx[::-1]
		#word_count_array = word_count_array[idx]

		#final = []
		#final = model.print_topic(word_count_array[0, 0], 10)

		#question_topic = final.split('*') ## as format is like "probability * topic"
		#print (question_topic)
		f.write(str(t) + " " + str(v) + "\n")

