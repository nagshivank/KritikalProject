import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from flask import Flask, render_template, request

import bs4 as bs
# import urllib2
# from urllib2 import urlopen

import string
import operator

class summarize:

    def get_summary(self, input, max_sentences):
        sentences_original = sent_tokenize(input)
        print("len of original text", len(sentences_original))
        if max_sentences > len(sentences_original):
            print("Error, number of requested sentences exceeds number of sentences inputted")
        s = input.replace('\n', " ")
        words_chopped = word_tokenize(s.lower())
        sentences_chopped = sent_tokenize(s.lower())
        stop_words = set(stopwords.words("english"))
        punc = set(string.punctuation)

        filtered_words = []
        for w in words_chopped:
            if w not in stop_words and w not in punc:
                filtered_words.append(w)
        total_words = len(filtered_words)
        word_frequency = {}
        for w in filtered_words:
            if w in word_frequency.keys():
                word_frequency[w] += 1.0  # increment the value: frequency
            else:
                word_frequency[w] = 1.0  # add the word to dictionary

        for word in word_frequency:
            word_frequency[word] = (word_frequency[word]/total_words)
        print(sentences_original)
        # for each sentence add sum of weighted frequency values
        tracker = [0.0] * len(sentences_original)
        for i in range(0, len(sentences_original)):
            for word in word_frequency:
                if word in sentences_original[i]:
                    tracker[i] += word_frequency[word]

        print("tracker =====", tracker)
        output_sentences = []
        print("max sentences =====", max_sentences)
        for i in range(0, len(tracker)):
            # pick sentences with max weighted words
            index, value = max(enumerate(tracker), key=operator.itemgetter(1))
            if len(output_sentences) + 1 <= max_sentences and sentences_original[index] not in output_sentences:
                output_sentences.append(sentences_original[index])
            if len(output_sentences) > max_sentences:
                break
            tracker.remove(tracker[index])
        print("output_sentences==============", output_sentences)
        sorted_output_sentences = self.sort_sentences(sentences_original, output_sentences)
        return sorted_output_sentences

    # sort on the basis of original sentence order
    def sort_sentences(self, original, output):
        sorted_sent_arr = []
        sorted_output = []
        for i in range(0, len(output)):
            if output[i] in original:
                sorted_sent_arr.append(original.index(output[i]))
        sorted_sent_arr = sorted(sorted_sent_arr)
        for i in range(0, len(sorted_sent_arr)):
            sorted_output.append(original[sorted_sent_arr[i]])
        print("===== sorted_output======", sorted_output)
        return sorted_output


# app = Flask(__name__)
#
#
# @app.route('/templates', methods=['POST'])
# def original_text_form():
#     title = 'Summarizer'
#     text = request.form['input_text']
#     max_value = sent_tokenize(text)
#     num_sent = int(request.form['num_sentences'])
#     sum1 = summarize()
#     summary = sum1.get_summary(text, num_sent)
#     print(summary)
#     return render_template("index.html", title=title, original_text=text,
#                            output_summary=summary, num_sentences=max_value)
#
#
#
# @app.route('/')
# def homepage():
#     title = 'Text Summarizer'
#     return render_template("index.html", title=title)
#
#
# if __name__ == "__main__":
#     app.debug = True
#     app.run()