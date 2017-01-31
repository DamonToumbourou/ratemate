from flask import Flask, render_template, url_for, g, redirect, session, request, flash
from scrapers import WebScrapers
from openpyxl import Workbook
import os
import sqlite3
import time

app = Flask(__name__)
app.config.from_object(__name__) 

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'ratemate.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('init the database')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/') 
def home():
    
    return render_template('index.html')


@app.route('/term_deposit')
def term_deposit():
    db = get_db()
    cur = db.execute('select logo, date, name, short, short_rate, mid, mid_rate, long, long_rate, date from term_deposit')
    term_deposit = cur.fetchall()
     
    wb = Workbook()
    ws = wb.active
    
    count = 1
    alp = 'A'
    for term in term_deposit:
       print chr(ord(alp)+count)
       count = count + 1


    wb.save('static/test.xlsx')
 
    return render_template('term_deposit.html', term_deposit=term_deposit)


@app.route('/add', methods=['GET', 'POST'])
def add_td():
    results = WebScrapers()
    results = results.collate_td()
    
    db = get_db()
    print 'len'
    print len(results)
    for result in results:
        name = result[3]['name']
        logo = result[3]['logo']
        short_day = result[0]['days']
        short_rate = result[0]['rate']
        mid_day = result[1]['days']
        mid_rate = result[1]['rate']
        long_day = result[2]['days']
        long_rate = result[2]['rate']
        date = time.strftime('%d/%m/%Y')
        print name 
        print logo
        print short_day
        print short_rate
        print mid_day
        print mid_rate
        print long_day
        print long_rate
        print date
        print '\n'

        db.execute('insert into term_deposit (name, logo, short, short_rate, mid, mid_rate, long, long_rate, date) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', [name, logo, short_day, short_rate, mid_day, mid_rate, long_day, long_rate, date])
    
    db.commit()
    flash('Database updated')

    return redirect(url_for('term_deposit'))


if __name__ == "__main__":
    app.run(debug=True)
