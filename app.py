from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request

from nltk_summarizer import nltk_summarizer
import time
import spacy

# Web Scraping Pkg
from bs4 import BeautifulSoup
# from urllib.request import urlopen
from urllib.request import urlopen

nlp = spacy.load('en_core_web_sm')
app = Flask(__name__)


def readingTime(mytext):
    total_words= len([token.text for token in nlp(mytext)])
    estimatedTime= total_words/ 200.0
    return estimatedTime

def get_text(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary = nltk_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
	start = time.time()
	if request.method == 'POST':
		raw_url = request.form['raw_url']
		rawtext = get_text(raw_url)
		final_reading_time = readingTime(rawtext)
		final_summary = nltk_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

# @app.route('/comparer',methods=['GET','POST'])
# def comparer():
# 	start = time.time()
# 	if request.method == 'POST':
# 		rawtext = request.form['rawtext']
# 		final_reading_time = readingTime(rawtext)
		
# 		# NLTK
# 		final_summary_nltk = nltk_summarizer(rawtext)
# 		summary_reading_time_nltk = readingTime(final_summary_nltk)
# 		# Sumy
		
# 		end = time.time()
# 		final_time = end-start
# 	return render_template('compare_summary.html',ctext=rawtext,final_summary_nltk=final_summary_nltk,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time_nltk=summary_reading_time_nltk)

if __name__ == '__main__':
	app.run(debug=True)