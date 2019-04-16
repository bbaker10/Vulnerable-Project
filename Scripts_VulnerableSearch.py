# AUTHOR: Brooke Baker
# ASSIGNMENT: Final Project
# OVERVIEW: This script takes a compilation of texts (from a religious viewpoint, business viewpoint, security viewpoint) and searches for the various forms of the word vulnerable (including vulnerability, vulnerableness, vulnerably). This script then writes out to three csv files (per category), one with the aggregate information, one with the sentences that contained some form of the word vulnerable, and one with a frequency analysis on the words found in the match sentences.
# REMINDER: General Conference talks need encoding='utf-8' in with open statement, the business and security articles do not; switch before running

### IMPORT STATEMENTS ###
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia
import csv
import nltk.data
import os
import re
import statistics
import string

### GLOBAL VARIABLE DECLARATIONS ###
directory = 'C:/Users/Brooke/Documents/My Documents/BYU/Winter 2019/LING 360/Final Project/'
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
stop_words = set(stopwords.words('english'))
stop_words.add('us')
exclude = set(string.punctuation)
exclude.remove('-')
exclude.add('“')
exclude.add('”')

### FUNCTIONS ###
# function to find forms of vulnerability in category's text
def get_matches(category):
    # declare local variables
    category_directory = directory + category + '/'
    match_sentences = {}
    all_sentiment = []
    match_sentiment = []
    freqs = {}
    total_words = 0
    num_matches = 0
    first_sentence = True

    if category == 'General Conference':
        category_abbrev = 'gen_conf'
    elif category == 'Business':
        category_abbrev = 'business'
    else:
        category_abbrev = 'security'

    # loop through all files in category_directory
    for filename in os.listdir(category_directory):
        with open(category_directory + "/" + filename, "r") as infile:
            doc = infile.read()
            
            # perform category-specific cleaning
            doc = clean_file(category, doc)
            
            # split into sentences
            sentences = '\n-----\n'.join(tokenizer.tokenize(doc))
            sentences = sentences.split('\n-----\n')

            for sentence in sentences:
                # append number of words to total_words
                total_words += len(sentence.split())

                if first_sentence:
                    # store link and title for first sentence
                    link_and_title = sentence.split('\n')
                    link = link_and_title[0]
                    title = link_and_title[1][:-1]
                    print('Working on ' + filename + '...')
                    first_sentence = False
                else:
                    # check for forms of vulnerable
                    # get sentiment of sentence
                    current_sentiment = sia().polarity_scores(sentence)
                    all_sentiment.append(current_sentiment['compound'])

                    # find matches
                    matches = re.findall(r'(vulnerab[a-z]*\b)', sentence)
                    
                    if len(matches) > 0:
                        # append the number of matches to num_matches
                        num_matches += len(matches)

                        # append the sentence with the match to match_sentences dictionary, along with its link and title
                        match_sentences[sentence] = [title, link]

                        # append match sentiment to match sentiment
                        match_sentiment.append(current_sentiment['compound'])

                        # clean sentence of punctuation and capitalization
                        sentence = ''.join(ch for ch in sentence if ch not in exclude)
                        words = sentence.lower().split()

                        # remove stop words and forms of the word vulnerable
                        words = [wd for wd in words if not wd in stop_words and not wd.startswith('vulnerab') and not wd == '--']

                        # store to freqs dictionary
                        for word in words:
                            freqs[word] = freqs.get(word, 0) + 1

        # at the end of the doc, reset the first_sentence boolean
        first_sentence = True

    # sort noun_pair frequencies in descending order
    freq_list = sorted(freqs.items(), key=lambda x:x[1], reverse=True)

    # get overall sentiment and match sentiment
    overall_sentiment = round(statistics.mean(all_sentiment), 2)
    match_sentiment = round(statistics.mean(match_sentiment), 2)
    
    # store category's aggregate results to csv
    print(f"Writing {category}'s aggregate data...", end='')
    with open(f'{directory}vulnerability_analysis_stats.csv', 'a', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=",")
        if os.stat(f"{directory}vulnerability_analysis_stats.csv").st_size == 0:
            writer.writerow(['Category', 'Num_Matches', 'Total_Words', 'Freq', 'Avg_Overall_Sent', 'Avg_Match_Sent'])
        writer.writerow([category, num_matches, total_words, round((num_matches/total_words)*1000, 5), overall_sentiment, match_sentiment])
    print(' Done')

    # store category's match sentences to csv
    print(f"Writing {category}'s sentence matches...", end='')
    with open(f'{directory}{category_abbrev}_vulnerable_sentences.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=",")
        if os.stat(f"{directory}{category_abbrev}_vulnerable_sentences.csv").st_size == 0:
            writer.writerow(['Document', 'Link', 'Sentence'])
        for key in match_sentences:
            writer.writerow([match_sentences[key][0], match_sentences[key][1], key])
    print(' Done')

    # store category's match words to csv
    print(f"Writing {category}'s match words...", end='')
    with open(f'{directory}{category_abbrev}_word_freq.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=",")
        if os.stat(f"{directory}{category_abbrev}_word_freq.csv").st_size == 0:
            writer.writerow(['Word', 'Num_Occurances', 'Freq', 'Sentiment'])
        for key, value in freq_list:
            writer.writerow([key, value, round((value/total_words)*1000, 5), sia().polarity_scores(key)['compound']])
    print(' Done')

# function to clean document
def clean_file(category, doc):
    if category == 'General Conference':
        # remove footnotes
        doc = re.sub(r'(\.”?)([0-9]){1,}', r'\1', doc)
    elif category == 'Business':
        # remove swearing
        doc = re.sub(r'(God)', r'#$@&%*!', doc)
    return doc

### FUNCTION CALLS ###
# get_matches('General Conference')
get_matches('Business')
get_matches('Security')