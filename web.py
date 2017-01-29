from flask import Flask, render_template
from scrapers import WebScrapers

app = Flask(__name__)

@app.route('/') 
def home():
    results = WebScrapers()
    results = results.collate_td()
    

    return render_template('index.html')


@app.route('/term_deposit')
def term_deposit():

    return render_template('term_deposit.html')


if __name__ == "__main__":
    app.run(debug=True)
