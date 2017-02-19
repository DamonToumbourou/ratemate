from flask import Flask, render_template, url_for, g, redirect, session, request, flash
from scrapers import WebScrapers
from openpyxl import Workbook
import os
import sqlite3
import datetime

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
    col_2_2nd = 'A'
    col_2 = 'C'
    col_3_2nd = 'B'
    col_3 = 'D'
    new_count = 0
    new_count_3 = 1
    for term in term_deposit:
        ws['A2'] = term[1] # date 
        ws['B2'] = 'Short term' 
        ws['B3'] = 'Mid term'
        ws['B4'] = 'Long term'
        ws[ col_2 + '1'] = term[2] # bank name
        ws[ col_2 + '2'] = int(term[3]) # days short
        ws[ col_2 + '3'] = int(term[5]) # days mid 
        ws[ col_2 + '4'] = int(term[7]) # days long

        if term[4]:
            ws[ col_3 + '2'] = float(term[4].strip('%')) # rate short
            ws[ col_3 + '3'] = float(term[6].strip('%')) # rate short
            ws[ col_3 + '4'] = float(term[8].strip('%')) # rate short

        count = count + 3
         
        if count <= 23:
            col_2 = chr(ord(col_2) + 3)
            col_3 = chr(ord(col_3) + 3)

        if count >= 24:
            col_2 = 'A' + chr(ord(col_2_2nd) + (new_count))
            col_2 = 'A' + chr(ord(col_3_2nd) + (new_count_3))
            
            new_count = new_count + 3

    wb.save('static/test.xlsx')
 
    return render_template('term_deposit.html', term_deposit=term_deposit)


@app.route('/add', methods=['GET'])
def add_td():
    
    db = get_db()
    db = db.execute('select date from term_deposit')
    dates = db.fetchall()
    uptodate = False
    # if db None
    if not dates:
        if get_write_td():
            print 'get_write_td'
    # if not None check when last scraped
    else:
        today = datetime.datetime.now() 
        seven_days_ago = datetime.datetime
        
        for date in dates:
            if seven_days_ago > date:
                print 'TDs have been scraped in the last 7 days... not scraping' 
                uptodate = True
            else:
                print 'TDs have not been scraped in the last 7 days... scraping TDs'
                if get_write_td():
                    print 'Successfuly scraped'
                    flash('TDs have been updated')
                else:
                    print 'Error scraping'
                    flash('There has been an error scraping TDs')
    
    if uptodate:
        flash('TDs have already been updated within the last 7 days')

    return redirect(url_for('term_deposit'))


def get_write_td():
    results = WebScrapers()
    results = results.collate_td()

    db_write = get_db()
    for result in results:
        print '******************'
        print results
        print '******************'

        name = result[3]['name']
        print 'name'
        print name
        logo = result[3]['logo']
        short_day = result[0]['days']
        print 'short_day'
        print short_day
        short_rate = result[0]['rate']
        print 'short_rate'
        print short_rate
        mid_day = result[1]['days']
        print mid_day
        mid_rate = result[1]['rate']
        print mid_rate
        long_day = result[2]['days']
        print long_day
        long_rate = result[2]['rate']
        print long_rate
        date = datetime.datetime.now()
        print date

        db_write.execute('insert into term_deposit (name, logo, short, short_rate, mid, mid_rate, long, long_rate, date) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', [name, logo, short_day, short_rate, mid_day, mid_rate, long_day, long_rate, date])
        db_write.commit()
    
    return True


if __name__ == "__main__":
    app.run(debug=True)
