from flask import Flask, render_template
from scrapers import WebScrapers

app = Flask(__name__)

@app.route('/') 
def home():
    results = WebScrapers()
    results = results.get_commbank_td()

    print results

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
