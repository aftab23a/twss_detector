import re
import sys 

import nltk
from nltk.tokenize import word_tokenize
import string 
from textblob.classifiers import NaiveBayesClassifier

reload(sys) 
sys.setdefaultencoding('ISO-8859-1')
positiveData = '../data/twssstories.txt'
negativeData1 = '../data/wikiquotes.txt'
negativeData2 = '../data/fml.txt'
negativeData3 = '../data/tflnonesent.txt'

def readFile(path): 
	f = open(path, 'r')
	text = f.read()
	f.close()
	return text.split('\n')

def cleanData(text):
	for t in text:
		text[t] = re.compile("[^\w]")
	return text 

# take in a some array of strings (each index has a sentence)
# return the first 3/4 of the array of strings for training data
# assumes everything is randomly sorted and there is no bias in terms of ordering
def getTraining(text): 
	length = len(text)
	numLines = float(length*3)/4
	return text[:int(numLines)]

# add a "pos" or "neg" tag to the end of each sentence 
# this tag will allow us to train the classifier on positive & negative datasets
# eg. ("Put it back in, it's still moist in the middle.", 'pos')
# returns a tuple containing a "string" and a 'tag'
def tagPos(text, feature):
	data = []
	for t in text:
		tup = () 
		t = t.replace("'", "")
		t = ' '.join(word.strip(string.punctuation) for word in t.split()) 
		tup = (t, feature)
		#data[t] = feature
		data.append(tup)
	return data


# combine pos neg data

# get positive training data 
txt = readFile(positiveData)
txt = getTraining(txt) 
txt = tagPos(txt, "pos")
# get negative training data 
negText = readFile(negativeData1)# + negativeData2 + negativeData3) 
negText1 = readFile(negativeData2)
negText2 = readFile(negativeData3)
print len(negText)
print len(negText1)
print len(negText2)

negText = getTraining(negText)
negText1 = getTraining(negText1)
negText2 = getTraining(negText2)

taggedNeg = tagPos(negText + negText1 + negText2, "neg")

print len(negText)
print len(negText1)
print len(negText2)
print len(taggedNeg)

#pos_neg_text = {} 
#pos_neg_text.update(txt)
#pos_neg_text.update(taggedNeg)
pos_neg_text = taggedNeg + txt
print len(pos_neg_text)
# write results to a doc
f = open('parsedData.txt', 'w')
f.write('\n'.join(str(v) for v in pos_neg_text))
f.close()

# after getting the tagged and parsed data, 
# iterate through each line in the resulting txt file and 
# feed to the classifer. 
cl = NaiveBayesClassifier(pos_neg_text)



# # Sklearn 
# classifier = MultinomialNB()
# # count vectorizer supports counds of n-grams of words or conseq. chars
# # the index of a word in the vocab is linked to its frequency in the whole training corpus
# count_vect = CountVectorizer()
# trainCounts = count_vect.fit_transform(data)
# tfidf_Transformer = TfidfTransformer() 

# y_pred = NB.fit()
# cleanText = re.compile("[^\w]")
# cleanText = cleanText.sub(' ', text)

# train = cleanText.split()

# classifier = nltk.classify.NaiveBayesClassifier.train(train)


# # some docs are longer than others, 
# # use tf_idf to downscale the weights of teh words that occur in many docs 
# # and are therefore less informative
