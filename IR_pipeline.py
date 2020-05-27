# IR Assignment by K'Ci Beckford (kb16315) & Hope Alexander (ha16593)

import nltk
import requests
from bs4 import BeautifulSoup
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
import math


def initial_processing_URL1():

    # Compiles raw HTML web page
    url1 = 'http://www.multimediaeval.org/mediaeval2019/memorability/'
    first_req = requests.get(url1)  # requests.get() pulls web page from
    html_page1 = first_req.content  # takes all content on page
    soup1 = BeautifulSoup(html_page1, 'html.parser')  # html parser used to identfify various html tags on website
    plain_text_main = soup1.find_all('body')  # finds all content between <body> tags and converts to plain text
    # print(plain_text_main)

    # Lists used for upcoming processes
    preformatted_text = []
    splits = []
    filtered_sentences = []
    sentences = []

    # Roughly separates the raw HTML into sentences
    for text in plain_text_main:
        text = text.get_text()
        sentence = sent_tokenize(str(text))
        #print(sentence)
        for line in sentence:  # for statement takes sentences and remove all new line (\n) elements
            delimit_line = line.replace("\n", ", ")
            preformatted_text.append(delimit_line)

    # Removes some content that is not main text
    for i in preformatted_text:
        if "." in i:  # for statement adds space after period by replacing with string
            i = i.replace(".", ". ")
            filtered_sentences.append(i)

    filtered_sentences.pop(0)  # this removes excess data on the form a "sentence"

    k = 43  # k is a predefined index number to remove a number of excess data from the lest
    without_extra = filtered_sentences[: len(sentences) - k]  # without_extra is the modified list without excess data

    # for statement takes conjoined words in the sentences and separates them if capital letter is present
    for f in without_extra:
        match_upper = re.findall(r'[A-Z]', f)
        for u in match_upper:
            capital = u
            if "i. e." in f:  # if statement caters for specific instances of 'i.e.' being processed as a word
                f = f.replace("i. e.", "i.e.")
                sentences.append(f)
                break
            elif "e. g." in f:  # if statement caters for specific instances of 'e.g.' being processed as a word
                f = f.replace("e. g.", "e.g.")
                sentences.append(f)
                break
            elif "." + " " + capital in f: # if statement splits instances by period (.) within sentence
                item = re.split('(?<=[.]) +', f)
                for separated in item:
                    sentences.append(separated)
                break
            else:
                pass

    for blank in sentences:  # for statement removes empty strings in sentences list
        if blank == "":
            sentences.remove(blank)

    web_page_A = ' '.join(sentences)  # combines all sentences into one long string for processing

    return web_page_A  # returns long sting on sentences with periods


def initial_processing_URL2():  # follows same structure ass initial_processing_URL1, however has some code removed

    url2 = 'https://sites.google.com/view/siirh2020/'
    second_req = requests.get(url2)
    html_page2 = second_req.content
    soup2 = BeautifulSoup(html_page2, 'html.parser')
    plain_text_main = soup2.find_all('body')
    # print(plain_text_main)

    preformatted_text = []
    splits = []
    processed_sentences = []
    sentences = []

    # Roughly separates the raw HTML into sentences
    for text in plain_text_main:
        text = text.get_text()
        sentence = sent_tokenize(str(text))
        # print("senetence: ", sentence)
        for line in sentence:
            delimit_line = line.replace("\n", ", ")
            preformatted_text.append(delimit_line)
        # print("preformmated_text: ", preformatted_text)


    # Removes some content that is not main text
    for i in preformatted_text:
        if "." in i:
            i = i.replace(".", ". ")
            processed_sentences.append(i)
    # print("filtered_sentences: ", filtered_sentences)

    processed_sentences.pop(0)

    for f in processed_sentences:
        match_upper = re.findall(r'[A-Z]', f)
        for u in match_upper:
            capital = u
            if "." + " " + capital in f:
                item = re.split('(?<=[.]) +', f)
                for separated in item:
                    sentences.append(separated)
                break
            else:
                pass

    for blank in sentences:
        if blank == "":
            sentences.remove(blank)

    web_page_B = ' '.join(sentences)
    # print(web_page_B)

    return web_page_B


def remove_stopwords(s):  # function used to remove stop words from sentences (s)

    return [word for word in s if not word in stop_words]


def remove_punct(s):  # function used to remove punctuation from sentences (s)
    no_punct = re.sub('[^\w\s]', '', s)

    return no_punct


# assigns a document id to each sentence and counts the length (number of words) in each
def get_raw_sentences(sent):
    doc_info = []
    i = 0
    for sent in cleaned_sentences:
        i += 1
        count = count_words(sent)
        temp = {'doc_id' : i, 'doc_length' : count}
        doc_info.append(temp)

    return doc_info

# function to count the words in each document
def count_words(sent):
    count = 0
    words = nltk.word_tokenize(sent)  # tokenises all words in each sentence
    for word in words:
        count += 1

    return count

# function creates dictionaries to assign an id to each sentence as a unique document
def total_dictionary(sents):
    i = 0
    dictionaries_list = []  # list of dictionaries
    for sent in sents:
        i += 1
        dictionary = {}  # dictionary of words in sentence
        words = nltk.word_tokenize(sent)  # tokenises all words in each sentence
        for word in words:
            word = word.lower()  # set all words to lowercase
            if word in dictionary:
                dictionary[word] += 1  # appends to dictionary and updates count
            else:
                dictionary[word] = 1
            temp = {'doc_id': i, 'dictionary': dictionary}  # temporary variable storing dictionary of words with id
        dictionaries_list.append(temp)

    return dictionaries_list  # returns list of dictionaries


def calculateTF(doc_info, dictionaries_list):  # function calculates Term Frequencey
    tf_scores = []  # list of TF scores
    for tempDict in dictionaries_list:
        id = tempDict['doc_id']  # assigns calculated doc id to variable
        for k in tempDict['dictionary']:  # for loop takes all word stored in dictionary and applies values to tf formula
            temp = {'doc_id': id,
                    'tf_score': tempDict['dictionary'][k]/doc_info[id-1]['doc_length'],
                    'key': k}  # temp is dictionary of tf values with associated words and ids
            tf_scores.append(temp)
    return tf_scores


def calculateIDF(doc_info, dictionaries_list):  # function calculates Inverse Document Frequency
    idf_scores = []  # list of IDF scores
    counter = 0
    for dict in dictionaries_list:  # for loop takes all dictionaries from stored dictionaries
        counter += 1
        for k in dict['dictionary'].keys():  # for loop compares total docs with number of words per doc and applies values to idf formula
            count = sum([k in tempDict['dictionary'] for tempDict in dictionaries_list])
            temp = {'doc_id': counter, 'idf_score': math.log(len(doc_info)/count), 'key': k}
            # # temp is dictionary of idf values with associated words and ids

            idf_scores.append(temp)

    return idf_scores


# function takes calculated values from Tf and IDF functions and applies them to TF-IDF formula
def calculateTF_IDF(tf_scores, idf_scores):
    tf_idf_scores = []  # list of TF-IDF scores
    for idf_data in idf_scores:
        for tf_data in tf_scores:
            if idf_data['key'] == tf_data['key'] and idf_data['doc_id'] == tf_data['doc_id']:
                temp = {'doc_id': idf_data['doc_id'],
                        'tf_idf_score': idf_data['idf_score'] * tf_data['tf_score'],
                        'word': tf_data['key']}
        tf_idf_scores.append(temp)

    for tf_idf_recs in tf_idf_scores:  # for loop cleanly prints out all TF-IDF records
        print(tf_idf_recs)

    return tf_idf_scores


# all fully processed words used from documents are processed though a stemmer to get stemmed variances of each
def stemming_for_analysis(stemming_list):
    stemmed_instances = []
    ss = SnowballStemmer("english")  # stemmer instance created
    for unstemmed in stemming_list:
        for words in unstemmed:
            stemmed_words = ss.stem(words)
            stemmed_instances.append(stemmed_words)

    return stemmed_instances


if __name__ == '__main__':
    first_web_page = initial_processing_URL1()  # reference to URL 1
    # print(first_web_page)
    second_web_page = initial_processing_URL2()  # reference to URL 2
    # print(second_web_page)

    ''' replace with second to see results for the other URL '''
    original_sentences = sent_tokenize(first_web_page)  # initial string is tokenised into individual sentences
    # print(original_sentences)

    cleaned_sentences = [remove_punct(s) for s in original_sentences]  # removes punctuation
    # print(cleaned_sentences)

    tokenise_remaining = [nltk.word_tokenize(s) for s in cleaned_sentences]  # words without punctuation are tokenised
    # print(tokenise_remaining)

    stop_words = list(set(stopwords.words('english')))  # reference to list of imported stop words
    no_stopwords = [remove_stopwords(sent) for sent in tokenise_remaining]  # list of words without stop words

    filtered_words = [remove_stopwords(s) for s in no_stopwords]  # all stop words removed
    # print(filtered_words)

    pos_tagging = [nltk.pos_tag(sent_tokens) for sent_tokens in filtered_words]  # POS tagging for each clean word
    # print(pos_tagging)

    pure = []  # list of purified sentences
    for rem_words_list in filtered_words:  # for loop combines cleaned words into full sentences again
        pure_sentences = ' '.join(set(rem_words_list))
        pure.append(pure_sentences)
    # print(pure)

    doc_info = get_raw_sentences(pure)  # sentences applied to documents function
    # print(doc_info)

    flist = total_dictionary(pure)  # sentences applied to dictionaries function
    # print(flist)

    tf_scores = calculateTF(doc_info, flist)  # processed data applied to TF formula
    # print(tf_scores)

    idf_scores = calculateIDF(doc_info, flist)  # processed data applied to IDF formula
    # print(idf_scores)

    tf_idf = calculateTF_IDF(tf_scores, idf_scores)  # TF and IDF totals applied to TF-IDF formula
    # print(tf_idf)

    print()

    analysis_group = stemming_for_analysis(filtered_words)  # applies cleaned words to stemming function
    print("Below is a list of all words from the dataset above after Stemming to be stored in DB")
    for stems in analysis_group:
        print(stems)

    ''' * All commented prints are for debugging purposed * '''
