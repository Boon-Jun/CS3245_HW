#!/usr/bin/python
from nltk.util import ngrams
from nltk.probability import FreqDist, LaplaceProbDist
from math import log10
import sys
import getopt

def word_observed(LM, word):
    for language, model in LM.iteritems():
        if model._freqdist[word] >= 1:
            return True
    return False

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print 'building language models...'

    lines = open(in_file, "r")
    observedFourGrams = set()
    LM = {}

    for line in lines: #This loop generates the count language model without one-smoothing with punctuations removed.
        word_list = line.split()
        language = word_list[0]
        word_string = ' '.join(word_list[1:]).lower()
        fourGrams = ngrams(list(word_string), 4)

        if language not in LM:
            LM[language] = FreqDist()

        for gram in fourGrams:
            strGram = ''.join(gram)
            LM[language][strGram] += 1
            observedFourGrams.add(strGram)

    for language in LM: #This loop converts each count model to a probabilistic model with add-one smoothing
        LM[language] = LaplaceProbDist(LM[language], len(observedFourGrams))

    return LM

def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    lines = open(in_file, 'r')
    results = open(out_file, 'a')
    results.seek(0)
    results.truncate()

    print "testing language models..."

    for line in lines:
        bestLanguage = 'other'
        highestLogProb = 1 #Set log(probability) to 1 to indicate that the value is not yet set.
                           #This is because probability <= 1, therefore log(probability) <= 0

        formattedString = ' '.join(line.split()).lower()#Split the string, and then join the list of words to ensure
                                                        #that there will only be one blank space between each word.

        fourGramsList = ngrams(list(formattedString), 4)
        word_list = [''.join(fourGram) for fourGram in fourGramsList]

        for language, model in LM.iteritems(): #Calculate the probabilities for each model
            calculatedLogProb = 0
            notFound = 0

            for word in word_list:
                if word_observed(LM, word):
                    calculatedLogProb += log10(model.prob(word))#Instead of multiplying probabilities, adding
                                                                #log(probability) allows us to compare probabilities
                                                                #without facing the problem where the probability
                                                                #is very small after consecutive multiplications.

                    if model._freqdist[word] == 0: #word is not found for this specific model.
                        notFound += 1
                else:
                    notFound += 1

            hasBetterProbability = calculatedLogProb > highestLogProb or highestLogProb == 1
            hasSufficientFourGrams= len(word_list) > 0 and float(notFound)/len(word_list) < 0.75 #An arbitrarily chosen threshold that
                                                                                                 #seems to work well with the test data set.

            if hasBetterProbability and hasSufficientFourGrams:
                highestLogProb = calculatedLogProb
                bestLanguage = language
        results.write(bestLanguage + ' ' + line)

def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None


try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
