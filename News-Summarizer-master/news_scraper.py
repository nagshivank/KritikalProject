import feedparser as fp
import json
import newspaper
from flask import Flask, render_template, request
from nltk.tokenize import sent_tokenize, word_tokenize
from summarizer import summarize
# from newspaper import Article


def get_data(company):
    data = dict()
    # data[company] = {}
    # companies = {}
    if company in companies:
        value = companies[company]
        print("company ====", company)
        paper = newspaper.build(value['link'], memoize_articles=False)
        news_paper = {
            'link': value['link'],
            'articles': []
        }
        count = 1
        for content in paper.articles:
            if count > 2:
                break
            try:
                content.download()
                content.parse()
            except Exception as e:
                print(e)
                print("Continuing")
                continue
            article = dict()
            article['title'] = content.title
            article['text'] = content.text
            max_value = sent_tokenize(article['text'])
            num_sent = 5
            summ = summarize()
            summary = summ.get_summary(article['text'], num_sent)
            article['summary'] = ''.join(summary)
            news_paper['articles'].append(article)
            count += 1
        # data[company] = news_paper
        print("========== data============", news_paper)
        return news_paper['articles']
app = Flask(__name__)

@app.route('/templates', methods=['POST'])
def original_text_form():
    title = 'News Summarizer'
    select = request.form.get('newspaper_select')
    print(str(select))
    data = get_data(str(select))
    # text = request.form['input_text']
    # max_value = sent_tokenize(text)
    # num_sent = int(request.form['num_sentences'])
    # sum1 = summarize()
    # summary = sum1.get_summary(text, num_sent)
    # print(summary)

    return render_template("index.html", company=str(select), title=title, output_data=data, data=newspaper_data)



@app.route('/')
def homepage():
    title = 'News Summarizer'
    return render_template("index.html", title=title, data=newspaper_data)


if __name__ == "__main__":
    with open('./data/newspapers.json') as file:
        companies = json.load(file)
    newspaper_data = []
    for name, value in companies.items():
        newspaper_data.append({"name": name})
    app.debug = True
    app.run()