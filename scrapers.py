from bs4 import BeautifulSoup as bs4
from requests import get
from selenium import webdriver
from flask import flash
from textract import process
from tika import parser
import requests
import time
import re
import private
import urllib
#from textract import process
from tika import parser
import smtplib

PHANTOMJS_PATH = './phantomjs'

class WebScrapers(object):
    

    def get_soup(self, url):
        request = requests.get(url)
        soup = bs4(request.text, 'html.parser')
        
        return soup

    
    def get_comm_td(self):
        url = 'https://www.commbank.com.au/content/dam/commbank/personal/apply-online/download-printed-forms/InvInterestRates_ADB1072.pdf'
        text = parser.from_file('./rates.pdf')
        
        text = text['content']
        line = ''
        count = 0
        record = False
        rates = []
        for t in text:
            line = line + t
            if t == '\n':
                
                if 'Term in Months' in line:
                    record = True

                if 'Term Deposit Rates' in line:
                    record = False

                if record:
                    rates.append(line)
                
                line = ''
        
        one_month = ''
        two_month = ''
        three_month = ''
        four_month = ''
        five_month = ''
        six_month = ''
        seven_month = ''
        eight_month = ''
        nine_month = ''
        ten_month = ''
        eleven_month = ''
        twelve_month = ''
        twentyfour_month = ''
        thirtysix_month = ''
        for rate in rates: 
            if '1 ' in rate[0:2]:
                one_month = rate.split(' ')[8].strip()

            if '2 ' in rate[0:2]:
                two_month = rate.split(' ')[8].strip()
            
            if '3 ' in rate[0:2]:
                three_month = rate.split(' ')[8].strip()

            if '4 ' in rate[0:3]:
                four_month = rate.split(' ')[8].strip()

            if '5 ' in rate[0:3]:
                five_month = rate.split(' ')[8].strip()

            if '6 ' in rate[0:3]:
                six_month = rate.split(' ')[8].strip()

            if '7 ' in rate[0:3]:
                seven_month = rate.split(' ')[8].strip()
            
            if '8 ' in rate[0:3]:
                eight_month = rate.split(' ')[8].strip()

            if '9 ' in rate[0:3]:
                nine_month = rate.split(' ')[8].strip()

            if '10' in rate[0:3]:
                ten_month = rate.split(' ')[8].strip()

            if '11' in rate[0:3]:
                eleven_month = rate.split(' ')[8].strip()

            if '12' in rate[0:3]:
                twelve_month = rate.split(' ')[8].strip()

            if '24' in rate[0:3]:
                twentyfour_month = rate.split(' ')[8].strip()

            if '36' in rate[0:3]:
                thirtysix_month = rate.split(' ')[8].strip()
         
        comm_td = [{
            'one_month': one_month,
            'two_month': two_month,
            'three_month': three_month,
            'four_month': four_month,
            'five_month': five_month,
            'six_month': six_month,
            'seven_month': seven_month,
            'eight_month': eight_month,
            'nine_month': nine_month,
            'ten_month': ten_month,
            'eleven_month': eleven_month,
            'twelve_month': twelve_month,
            'twentyfour_month': twentyfour_month,
            'thirtysix_month': thirtysix_month
        }]

        bank = {
            'name': 'CBA', 
            'product': 'Term Deposit',
            'logo': 'cba.jpg',
            'notes' : 'Interest Paid every 12 months and/or at maturity for terms less than 12 months.'
        }
        comm_td.append(bank)
        
        return comm_td


    def get_anz_advanced_td(self):
        url = 'https://www.anz.com.au/personal/bank-accounts/your-account/rates-fees-terms/#termdeposit'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        content = soup.find_all('div', {'class': 'table-scrollable'})
        
        row = content[0].find_all('tr')
         
        anz_td = [{ 
            'one_month': row[1].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'two_month': row[2].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'three_month': row[3].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'four_month': row[4].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'five_month': row[5].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'six_month': row[6].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'seven_month': row[7].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'eight_month': row[8].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'nine_month': row[9].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'ten_month': row[10].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'eleven_month': row[11].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'twelve_month': row[12].find_all('td')[4].find('span', {'class': 'productdata'}).string.split('%')[0],
            'twentyfour_month': row[12].find_all('td')[4].find('span', {'class': 'productdata'}).string.split('%')[0],
            'thirtysix_month': row[12].find_all('td')[4].find('span', {'class': 'productdata'}).string.split('%')[0]
        }]
        
        bank = {
            'name': 'ANZ Advanced Notice',
            'product': 'Term Deposit',
            'logo': 'anz.jpg',
            'notes': ''
        }
        anz_td.append(bank)
        
        return anz_td
   

    def get_anz_standard_td(self):
        url = 'https://www.anz.com.au/personal/bank-accounts/your-account/rates-fees-terms/#termdeposit'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        content = soup.find_all('div', {'class': 'table-scrollable'})
        
        row = content[1].find_all('tr')
        
        anz_td = [{ 
            'one_month': row[1].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'two_month': row[2].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'three_month': row[3].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'four_month': row[4].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'five_month': row[5].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'six_month': row[6].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'seven_month': row[7].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'eight_month': row[8].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'nine_month': row[9].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'ten_month': row[10].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'eleven_month': row[11].find_all('td')[0].find('span', {'class': 'productdata'}).string.split('%')[0],
            'twelve_month': row[12].find_all('td')[4].find('span', {'class': 'productdata'}).string.split('%')[0],
            'twentyfour_month': row[12].find_all('td')[4].find('span', {'class': 'productdata'}).string.split('%')[0],
            'thirtysix_month': row[12].find_all('td')[4].find('span', {'class': 'productdata'}).string.split('%')[0]
        }]
        
        bank = {
            'name': 'ANZ Standard Notice',
            'product': 'Term Deposit',
            'logo': 'anz.jpg',
            'notes': ''
        }
        anz_td.append(bank)
        
        return anz_td
    

    def get_west_td(self):
        url = 'https://www.westpac.com.au/personal-banking/bank-accounts/term-deposit/'
        soup = self.get_soup(url)
        content = soup.find('div', {'id': 'tab1'})
        
        rates = content.find_all('tr')
        
        one_month = ''
        two_month = ''
        three_month = ''
        four_month = ''
        five_month = ''
        six_month = ''
        seven_month = ''
        eight_month = ''
        nine_month = ''
        ten_month = ''
        eleven_month = ''
        twelve_month = ''
        twentyfour_month = ''
        thirtysix_month = ''

        for rate in rates[0:15]:
            search = rate.find('td', {'scope': 'row'})
            
            if search is not None:
                
                if search.findAll(text=re.compile('1 < 2')):
                    one_month = rate.find_all('td')[4].string.split('%')[0]

                if search.findAll(text=re.compile('2\xa0< 3')):
                    two_month = rate.find_all('td')[4].string.split('%')[0]

                if search.findAll(text=re.compile('3\xa0< 4')):
                    three_month = rate.find_all('td')[4].string.split('%')[0]
                
                if search.findAll(text=re.compile('4\xa0< 5')):
                    four_month = rate.find_all('td')[4].string.split('%')[0]
                
                if search.findAll(text=re.compile('5\xa0< 6')):
                    five_month = rate.find_all('td')[4].string.split('%')[0]

                if search.findAll(text=re.compile('6\xa0< 7')):
                    six_month = rate.find_all('td')[4].string.split('%')[0]

                if search.findAll(text=re.compile('7\xa0< 8')):
                    seven_month = rate.find_all('td')[4].string.split('%')[0]

                if search.findAll(text=re.compile('8\xa0< 9')):
                    eight_month = rate.find_all('td')[4].string.split('%')[0]

                if search.findAll(text=re.compile('9\xa0< 10')):
                    nine_month = rate.find_all('td')[4].string.split('%')[0]

                if search.findAll(text=re.compile('10\xa0< 11')):
                    ten_month = rate.find_all('td')[4].string.split('%')[0]
                
                if search.findAll(text=re.compile('11\xa0< 12')):
                    eleven_month = rate.find_all('td')[4].string.split('%')[0]

                if search.findAll(text=re.compile('12\xa0< 24')):
                    twelve_month = rate.find_all('td')[4].string.split('%')[0]

                if search.findAll(text=re.compile('24\xa0< 36')):
                    twentyfour_month = rate.find_all('td')[4].string.split('%')[0]
            
                if search.findAll(text=re.compile('36\xa0< 48')):
                    thirtysix_month = rate.find_all('td')[4].string.split('%')[0]

        west_td = [{
            'one_month': one_month,
            'two_month': two_month,
            'three_month': three_month,
            'four_month': four_month,
            'five_month': five_month,
            'six_month': six_month,
            'seven_month': seven_month,
            'eight_month': eight_month,
            'nine_month': nine_month,
            'ten_month': ten_month,
            'eleven_month': eleven_month,
            'twelve_month': twelve_month,
            'twentyfour_month': twentyfour_month,
            'thirtysix_month': thirtysix_month
        }]
  
        bank = {
            'name': 'Westpac',         
            'product': 'Term Deposit',
            'logo': 'westpac.jpg',
            'notes': ''
        }
        west_td.append(bank)
        
        return west_td    

    
    def get_nab_td(self):
        url = 'http://www.nab.com.au/personal/interest-rates-fees-and-charges/indicator-rates-selected-term-deposit-products'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'parbase table section'})
        rates = content.find_all('tr')
        
        one_month = ''
        two_month = ''
        three_month = ''
        four_month = ''
        five_month = ''
        six_month = ''
        seven_month = ''
        eight_month = ''
        nine_month = ''
        ten_month = ''
        eleven_month = ''
        twelve_month = ''
        twentyfour_month = ''
        thirtysix_month = ''

        for rate in rates:

            if '30 days' == rate.find('td').string:
                one_month = rate.find_all('td')[1].string.split('%')[0]
                
            if '60 days' == rate.find('td').string:
                two_month = rate.find_all('td')[1].string.split('%')[0]
            
            if '90 days*' == rate.find('td').string:
                three_month = rate.find_all('td')[1].string.split('%')[0]
                
            if '4 months' == rate.find('td').string:
                four_month = rate.find_all('td')[1].string.split('%')[0]
            
            if '5 months' == rate.find('td').string:
                five_month = rate.find_all('td')[1].string.split('%')[0]
                
            if '6 months*' == rate.find('td').string:
                six_month = rate.find_all('td')[1].string.split('%')[0]
            
            if '7 months' == rate.find('td').string:
                seven_month = rate.find_all('td')[1].string.split('%')[0]
                
            if '8 months*' == rate.find('td').string:
                eight_month = rate.find_all('td')[1].string.split('%')[0]
             
            if '9 months' == rate.find('td').string:
                nine_month = rate.find_all('td')[1].string.split('%')[0]

            if '10 months' == rate.find('td').string:
                ten_month = rate.find_all('td')[1].string.split('%')[0]
             
            if '11 months' == rate.find('td').string:
                eleven_month = rate.find_all('td')[1].string.split('%')[0]

            if '12 months*' == rate.find('td').string:
                twelve_month = rate.find_all('td')[1].string.split('%')[0]
             
            if '24 months*' == rate.find('td').string:
                twentyfour_month = rate.find_all('td')[1].string.split('%')[0]

            if '36 months*' == rate.find('td').string:
                thirtysix_month = rate.find_all('td')[1].string.split('%')[0]

        nab_td = [{
            'one_month': one_month,
            'two_month': two_month,
            'three_month': three_month,
            'four_month': four_month,
            'five_month': five_month,
            'six_month': six_month,
            'seven_month': seven_month,
            'eight_month': eight_month,
            'nine_month': nine_month,
            'ten_month': ten_month,
            'eleven_month': eleven_month,
            'twelve_month': twelve_month,
            'twentyfour_month': twentyfour_month,
            'thirtysix_month': thirtysix_month
        }]

        bank = {
            'name': 'NAB',
            'product': 'Term Deposit',
            'logo': 'nab.jpg',
            'notes': ''
        }
        nab_td.append(bank)
        
        return nab_td


    def get_george_td(self):
        url = 'https://www.stgeorge.com.au/personal/bank-accounts/term-deposits'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('tr')
         
        one_month = ''
        two_month = ''
        three_month = ''
        four_month = ''
        five_month = ''
        six_month = ''
        seven_month = ''
        eight_month = ''
        nine_month = ''
        ten_month = ''
        eleven_month = ''
        twelve_month = ''
        twentyfour_month = ''
        thirtysix_month = ''

        for rate in rates[0:15]:
            found = rate.find('td')
            if found is not None:
                
                if '1 to less than 2' in found.string:
                    found_rate = rate.find_all('td')[5]
                    one_month = found_rate.find('span').string
                
                if '2 to less than 3' in found.string:
                    found_rate = rate.find_all('td')[5]
                    two_month = found_rate.find('span').string 

                if '3 to less than 4' in found.string:
                    found_rate = rate.find_all('td')[5]
                    three_month = found_rate.find('span').string 
        
                if '4 to less than 5' in found.string:
                    found_rate = rate.find_all('td')[5]
                    four_month = found_rate.find('span').string
                
                if '5 to less than 6' in found.string:
                    found_rate = rate.find_all('td')[5]
                    five_month = found_rate.find('span').string 

                if '6 to less than 7' in found.string:
                    found_rate = rate.find_all('td')[5]
                    six_month = found_rate.find('span').string 
        
                if '7 to less than 8' in found.string:
                    found_rate = rate.find_all('td')[5]
                    seven_month = found_rate.find('span').string
                
                if '8 to less than 9' in found.string:
                    found_rate = rate.find_all('td')[5]
                    eight_month = found_rate.find('span').string 

                if '9 to less than 10' in found.string:
                    found_rate = rate.find_all('td')[5]
                    nine_month = found_rate.find('span').string 
        
                if '10 to less than 11' in found.string:
                    found_rate = rate.find_all('td')[5]
                    ten_month = found_rate.find('span').string
                
                if '11 to less than 12' in found.string:
                    found_rate = rate.find_all('td')[5]
                    eleven_month = found_rate.find('span').string 

                if '12 months' in found.string:
                    found_rate = rate.find_all('td')[5]
                    twelve_month = found_rate.find('span').string 
        
        george_td = [{
            'one_month': one_month,
            'two_month': two_month,
            'three_month': three_month,
            'four_month': four_month,
            'five_month': five_month,
            'six_month': six_month,
            'seven_month': seven_month,
            'eight_month': eight_month,
            'nine_month': nine_month,
            'ten_month': ten_month,
            'eleven_month': eleven_month,
            'twelve_month': twelve_month,
            'twentyfour_month': '-',
            'thirtysix_month': '-'
        }]

        bank = {
            'name': 'St George',
            'product': 'Term Deposit',
            'logo': 'george.jpg',
            'notes': ''
        }
        george_td.append(bank)
        
        return george_td
       
    
    def get_bankwest_td(self):
        url = 'http://www.bankwest.com.au/personal/savings-term-deposits/savings-accounts-term-deposits/gold-term-deposit?tab=rates-fees'
        soup = self.get_soup(url)
        content = soup.find('table', {'class': 'ratesTable'})
        rates = content.find_all('tr')
        
        one_month = ''
        two_month = ''
        three_month = ''
        four_month = ''
        five_month = ''
        six_month = ''
        seven_month = ''
        eight_month = ''
        nine_month = ''
        ten_month = ''
        eleven_month = ''
        twelve_month = ''
        twentyfour_month = ''
        thirtysix_month = ''

        for rate in rates:
            if '1 month' == rate.find('th').string:
                one_month = rate.find('span').string.split('%')[0]
                
            if '2 months' == rate.find('th').string:
                two_month = rate.find('span').string.split('%')[0]
            
            if '3 months' == rate.find('th').string:
                three_month = rate.find('span').string.split('%')[0]
            
            if '4 months' == rate.find('th').string:
                four_month = rate.find('span').string.split('%')[0]
            
            if '5 months' == rate.find('th').string:
                five_month = rate.find('span').string.split('%')[0]
            
            if '6 months' == rate.find('th').string:
                six_month = rate.find('span').string.split('%')[0]
            
            if '7 months' == rate.find('th').string:
                seven_month = rate.find('span').string.split('%')[0]
            
            if '8 months' == rate.find('th').string:
                eight_month = rate.find('span').string.split('%')[0]
              
            if '9 months' == rate.find('th').string:
                nine_month = rate.find('span').string.split('%')[0]
            
            if '10 months' == rate.find('th').string:
                ten_month = rate.find('span').string.split('%')[0]
            
            if '11 months' == rate.find('th').string:
                eleven_month = rate.find('span').string.split('%')[0]
        
            if '12 months' == rate.find('th').string:
                twelve_month = rate.find('span').string.split('%')[0]
        
            if '24 months' == rate.find('th').string:
                twentyfour_month = rate.find('span').string.split('%')[0]
        
            if '36 months' == rate.find('th').string:
                thirtysix_month = rate.find('span').string.split('%')[0]

        bankwest_td = [{
            'one_month': one_month,
            'two_month': two_month,
            'three_month': three_month,
            'four_month': four_month,
            'five_month': five_month,
            'six_month': six_month,
            'seven_month': seven_month,
            'eight_month': eight_month,
            'nine_month': nine_month,
            'ten_month': ten_month,
            'eleven_month': eleven_month,
            'twelve_month': twelve_month,
            'twentyfour_month': twentyfour_month,
            'thirtysix_month': thirtysix_month
        }]
           
        bank = {
            'name': 'Bankwest Gold',
            'product': 'Term Deposit',
            'logo': 'bankwest.jpg',
            'notes': 'In-store term deposit'
        }
        bankwest_td.append(bank)
        
        return bankwest_td


    def get_ubank_loyalty_td(self):
        url = 'https://www.ubank.com.au/banking-overview/term-deposits#rates'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'table-responsive rate-table-rhs'})
        rates = content.find_all('tr')

        one_month = ''
        three_month = ''
        four_month = ''
        six_month = ''
        nine_month = ''
        twelve_month = ''
        for rate in rates:
            found = rate.find('td')
            if found is not None:
                if 'UBank - with Loyalty Bonus' in found.string: 
                    stand = rate.find_all('td')
                    
                    one_month = stand[1].string.split('%')[0]
                    
                    three_month = stand[2].string.split('%')[0]
                    
                    four_month = stand[3].string.split('%')[0]
                    
                    six_month = stand[4].string.split('%')[0]
                    
                    nine_month = stand[5].string.split('%')[0]
                    
                    twelve_month = stand[6].string.split('%')[0]
        
        ubank_td = [{
            'one_month': one_month,
            'two_month': '-',
            'three_month': three_month,
            'four_month': four_month,
            'five_month': '-',
            'six_month': six_month,
            'seven_month': '-',
            'eight_month': '-',
            'nine_month': nine_month,
            'ten_month': '-',
            'eleven_month': '-',
            'twelve_month': twelve_month,
            'twentyfour_month': '-',
            'thirtysix_month': '-'
        }]
                    
        bank = {
            'name': 'UBank Loyalty Bonus',
            'product': 'Term Deposit',
            'logo': 'ubank.jpg',
            'notes': 'Rates only avaliable to existing customers rolling over full deposit'
        }
        ubank_td.append(bank)
        return ubank_td
    
    
    def get_ubank_standard_td(self):
        url = 'https://www.ubank.com.au/banking-overview/term-deposits#rates'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'table-responsive rate-table-rhs'})
        rates = content.find_all('tr')

        one_month = ''
        three_month = ''
        four_month = ''
        six_month = ''
        nine_month = ''
        twelve_month = ''
        for rate in rates:
            found = rate.find('td')
            if found is not None:
                if 'UBank - Standard rate' in found.string: 
                    stand = rate.find_all('td')
                    
                    one_month = stand[1].string.split('%')[0]
                    
                    three_month = stand[2].string.split('%')[0]
                    
                    four_month = stand[3].string.split('%')[0]
                    
                    six_month = stand[4].string.split('%')[0]
                    
                    nine_month = stand[5].string.split('%')[0]
                    
                    twelve_month = stand[6].string.split('%')[0]
        
        ubank_td = [{
            'one_month': one_month,
            'two_month': '-',
            'three_month': three_month,
            'four_month': four_month,
            'five_month': '-',
            'six_month': six_month,
            'seven_month': '-',
            'eight_month': '-',
            'nine_month': nine_month,
            'ten_month': '-',
            'eleven_month': '-',
            'twelve_month': twelve_month,
            'twentyfour_month': '-',
            'thirtysix_month': '-'
        }]
                    
        bank = {
            'name': 'UBank Standard',
            'product': 'Term Deposit',
            'logo': 'ubank.jpg',
            'notes': ''
        }
        ubank_td.append(bank)
        
        return ubank_td
    

    def get_boq_td(self):
        url = 'http://www.boq.com.au/todays_rates_term_deposits.htm'
        soup = self.get_soup(url)
        content = soup.find_all('table')
        rates = content[1].find_all('tr')
        
        one_month = ''
        two_month = ''
        three_month = ''
        four_month = ''
        five_month = ''
        six_month = ''
        seven_month = ''
        eight_month = ''
        nine_month = ''
        ten_month = ''
        eleven_month = ''
        twelve_month = ''
        twentyfour_month = ''
        thirtysix_month = ''

        for rate in rates:
            curr = rate.find('td').string
            
            if curr is not None:
                
                if '1 less than 2' == curr:
                    one_month = rate.find_all('td')[3].string

                if '2 less than 3' in curr:
                    two_month = rate.find_all('td')[3].string
                
                if '3 less than 4' in curr:
                    three_month = rate.find_all('td')[3].string.split('*')[0]

                if '4 less than 5' in curr:
                    four_month = rate.find_all('td')[3].string.split('*')[0] 
        
                if '5 less than 6' in curr:
                    five_month = rate.find_all('td')[3].string.split('*')[0] 

                if '6 less than 7' in curr:
                    six_month = rate.find_all('td')[3].string.split('*')[0] 
        
                if '7 less than 8' in curr:
                    seven_month = rate.find_all('td')[3].string.split('*')[0] 

                if '8 less than 9' in curr:
                    eight_month = rate.find_all('td')[3].string.split('*')[0] 
        
                if '9 less than 10' in curr:
                    nine_month = rate.find_all('td')[3].string.split('*')[0] 

                if '10 less than 11' in curr:
                    ten_month = rate.find_all('td')[3].string.split('*')[0] 
        
                if '11 less than 12' in curr:
                    eleven_month = rate.find_all('td')[3].string.split('*')[0] 

                if '12 less than 24' in curr:
                    twelve_month = rate.find_all('td')[3].string.split('*')[0] 
                
                if '24 less than 36' in curr:
                    twentyfour_month = rate.find_all('td')[3].string.split('*')[0] 
        
                if '36 less than 48' in curr:
                    thirtysix_month = rate.find_all('td')[3].string.split('*')[0] 
        
        boq_td = [{
            'one_month': one_month,
            'two_month': two_month,
            'three_month': three_month,
            'four_month': four_month,
            'five_month': five_month,
            'six_month': six_month,
            'seven_month': seven_month,
            'eight_month': eight_month,
            'nine_month': nine_month,
            'ten_month': ten_month,
            'eleven_month': eleven_month,
            'twelve_month': twelve_month,
            'twentyfour_month': twentyfour_month,
            'thirtysix_month': thirtysix_month
        }]
          
        bank = {
            'name': 'BOQ',
            'product': 'Term Deposit',
            'logo': 'boq.jpg',
            'notes': ''
        }
        boq_td.append(bank)
        
        return boq_td
    

    def get_rabo_td(self):
        url = 'https://www.rabodirect.com.au/rates/personal-rates/'
        soup = self.get_soup(url)
        content = soup.find_all('table', {'class': 'rates-table responsive'})
        rates = content[5].find_all('tr')
        
        one_month = ''
        three_month = ''
        six_month = ''
        nine_month = ''
        twelve_month = ''
        twentyfour_month = ''
        thirtysix_month = ''

        for rate in rates:
            curr = rate.find_all('td')
            if curr:
                if '1 month' in curr[0].string:
                    one_month = curr[1].string.strip()
                
                if '3 months' in curr[0].string:
                    three_month = curr[1].string.strip()
                
                if '6 months' in curr[0].string:
                    six_month = curr[1].string.strip()
                
                if '9 months' in curr[0].string:
                    nine_month = curr[1].string.strip()
                
                if '1 year' in curr[0].string:
                    twelve_month = curr[5].string.strip() 
                
                if '2 years' in curr[0].string:
                    twentyfour_month = curr[5].string.strip() 
                
                if '3 years' in curr[0].string:
                    thirtysix_month = curr[5].string.strip()
        
        rabo_td = [{
            'one_month': one_month,
            'two_month': '-',
            'three_month': three_month,
            'four_month': '-',
            'five_month': '-',
            'six_month': six_month,
            'seven_month': '-',
            'eight_month': '-',
            'nine_month': nine_month,
            'ten_month': '-',
            'eleven_month': '-',
            'twelve_month': twelve_month,
            'twentyfour_month': twentyfour_month,
            'thirtysix_month': thirtysix_month
        }]

        bank = {
            'name': 'RaboDirect',
            'product': 'Term Deposit',
            'logo': 'rabo.jpg',
            'notes': ''
        }
        rabo_td.append(bank)
        
        return rabo_td

     
    def get_bom_td(self):
        url = 'https://www.bankofmelbourne.com.au/help/interest-rates/fixed-term-deposits'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('table', {'class': 'table'})
        content = rates[0].find_all('tr') 

        one_month = ''
        two_month = ''
        three_month = ''
        four_month = ''
        five_month = ''
        six_month = ''
        seven_month = ''
        eight_month = ''
        nine_month = ''
        ten_month = ''
        eleven_month = ''
        twelve_month = ''

        for rate in content[1:]: 
            
            curr = rate.find_all('td')[0]
            
            if '1 to less than 2 months' in curr:
                one_month = rate.find_all('td')[5].string.split('%')[0]
            
            if '2 to less than 3 months' in curr:
                two_month = rate.find_all('td')[5].string.split('%')[0]
            
            if '3 to less than 4 months' in curr:
                three_month = rate.find_all('td')[5].string.split('%')[0] 
    
            if '4 to less than 5 months' in curr:
                four_month = rate.find_all('td')[5].string.split('%')[0] 
    
            if '5 to less than 6 months' in curr:
                five_month = rate.find_all('td')[5].string.split('%')[0]
            
            if '6 to less than 7 months' in curr:
                six_month = rate.find_all('td')[5].string.split('%')[0]
            
            if '7 to less than 8 months' in curr:
                seven_month = rate.find_all('td')[5].string.split('%')[0]
            
            if '8 to less than 9 months' in curr:
                eight_month = rate.find_all('td')[5].string.split('%')[0] 
    
            if '9 to less than 10 months' in curr:
                nine_month = rate.find_all('td')[5].string.split('%')[0] 
    
            if '10 to less than 11 months' in curr:
                ten_month = rate.find_all('td')[5].string.split('%')[0]

            if '11 to less than 12 months' in curr:
                eleven_month = rate.find_all('td')[5].string.split('%')[0]
            
            if '12 months' in curr:
                twelve_month = rate.find_all('td')[5].string.split('%')[0]
            
        bom_td = [{
            'one_month': one_month,
            'two_month': two_month,
            'three_month': three_month,
            'four_month': four_month,
            'five_month': five_month,
            'six_month': six_month,
            'seven_month': seven_month,
            'eight_month': eight_month,
            'nine_month': nine_month,
            'ten_month': ten_month,
            'eleven_month': eleven_month,
            'twelve_month': twelve_month,
            'twentyfour_month': '-',
            'thirtysix_month': '-'
        }]

        bank = {
            'name': 'BOM',
            'product': 'Term Deposit',
            'logo': 'bom.jpg',
            'notes': 'Amounts less than 250k'
        }
        bom_td.append(bank)
        
        return bom_td

    
    def get_ing_td(self):
        url = 'https://www.ingdirect.com.au/rates-and-fees/term-deposit-rates.html'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('div', {'class': 'table-row data'})
        
        three_month = ''
        four_month = ''
        six_month = ''
        seven_month = ''
        nine_month = ''
        eleven_month = ''
        twelve_month = ''
        twentyfour_month = ''

        for rate in rates:
            try:
                curr = rate.find('p').string
            
                if '90 day rate' in curr: 
                    three_month = rate.find('span').string

                if '120 day rate' in curr:
                    four_month = rate.find('span').string
                
                if '180 day rate' in curr: 
                    six_month = rate.find('span').string

                if '210 day rate' in curr:
                    seven_month = rate.find('span').string

                if '270 day rate' in curr: 
                    nine_month = rate.find('span').string

                if '330 day rate' in curr:
                    eleven_month = rate.find('span').string

                if '1 year rate' in curr:
                    twelve_month = rate.find('span').string
                
                if '2 year rate' in curr:
                    twentyfour_month = rate.find('span').string 
            except:
                curr = None

        ing_td = [{
            'one_month': '-',
            'two_month': '-',
            'three_month': three_month,
            'four_month': four_month,
            'five_month': '-',
            'six_month': six_month,
            'seven_month': seven_month,
            'eight_month': '-',
            'nine_month': nine_month,
            'ten_month': '-',
            'eleven_month': eleven_month,
            'twelve_month': twelve_month,
            'twentyfour_month': twentyfour_month,
            'thirtysix_month': '-'
        }]

        bank = {
            'name': 'ING Direct',
            'product': 'Term Deposit',
            'logo': 'ing.jpg',
            'notes': 'Loyalty bonus of +0.10% for full rollover.'
        }
        ing_td.append(bank)
        
        return ing_td
     

    def get_sun_td(self):
        url = 'https://www.suncorp.com.au/banking/investments/term-deposits.html#tab2'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('tbody')
        rates = rates[0].find_all('tr')

        one_month = rates[0].find_all('td')[4].string.split('%')[0]
        two_month = rates[1].find_all('td')[4].string.split('%')[0]
        three_month = rates[2].find_all('td')[4].string.split('%')[0]
        four_month = rates[3].find_all('td')[4].string.split('%')[0]
        five_month = rates[4].find_all('td')[4].string.split('%')[0]
        six_month = rates[5].find_all('td')[4].string.split('%')[0]
        seven_month = rates[6].find_all('td')[4].string.split('%')[0]
        eight_month = rates[7].find_all('td')[4].string.split('%')[0]
        nine_month = rates[8].find_all('td')[4].string.split('%')[0]
        ten_month = rates[9].find_all('td')[4].string.split('%')[0]
        eleven_month = rates[10].find_all('td')[4].string.split('%')[0]
        twelve_month = rates[11].find_all('td')[4].string.split('%')[0]
        twentyfour_month = rates[12].find_all('td')[4].string.split('%')[0]
        thirtysix_month = rates[13].find_all('td')[4].string.split('%')[0]

        sun_td = [{
            'one_month': one_month,
            'two_month': two_month,
            'three_month': three_month,
            'four_month': four_month,
            'five_month': five_month,
            'six_month': six_month,
            'seven_month': seven_month,
            'eight_month': eight_month,
            'nine_month': nine_month,
            'ten_month': ten_month,
            'eleven_month': eleven_month,
            'twelve_month': twelve_month,
            'twentyfour_month': twentyfour_month,
            'thirtysix_month': thirtysix_month
        }]
        
        bank = {
            'name': 'Suncorp',
            'product': 'Term Deposit',
            'logo': 'suncorp.jpg',
            'notes': ''
        }
        sun_td.append(bank)
        
        return sun_td
          

    def get_bendigo_td(self):
        url = 'http://www.bendigobank.com.au/public/personal/term-deposits/term-deposit-interest-rates'         
        soup = self.get_soup(url)
        content = soup.find_all('table', {'style': 'width: 100%'})
        rates = content[1].find_all('tr')
                
        one_month = rates[2].find_all('td')[1].string.split('%')[0]
        two_month = rates[3].find_all('td')[1].string.split('%')[0]
        three_month = rates[4].find_all('td')[1].string.split('%')[0]
        four_month = rates[5].find_all('td')[1].string.split('%')[0]
        five_month = rates[6].find_all('td')[1].string.split('%')[0]
        six_month = rates[7].find_all('td')[1].string.split('%')[0]
        seven_month = rates[8].find_all('td')[1].string.split('%')[0]
        eight_month = rates[9].find_all('td')[1].string.split('%')[0]
        nine_month = rates[10].find_all('td')[1].string.split('%')[0]
        ten_month = rates[11].find_all('td')[1].string.split('%')[0]
        eleven_month = rates[12].find_all('td')[1].string.split('%')[0]
        twelve_month = rates[13].find_all('td')[1].string.split('%')[0]
        twentyfour_month = rates[15].find_all('td')[5].string.split('%')[0]
        thirtysix_month = rates[16].find_all('td')[5].string.split('%')[0]

        bendigo_td = [{
            'one_month': one_month,
            'two_month': two_month,
            'three_month': three_month,
            'four_month': four_month,
            'five_month': five_month,
            'six_month': six_month,
            'seven_month': seven_month,
            'eight_month': eight_month,
            'nine_month': nine_month,
            'ten_month': ten_month,
            'eleven_month': eleven_month,
            'twelve_month': twelve_month,
            'twentyfour_month': twentyfour_month,
            'thirtysix_month': thirtysix_month
        }]
        
        bank = {
            'name': 'Bendigo',
            'product': 'Term Deposit',
            'logo': 'bendigo.jpg',
            'notes': ''
        }
        bendigo_td.append(bank)
        
        return bendigo_td
    
        
    def get_citi_td(self):
        url = 'https://www.citibank.com.au/australia/pdf/1995_Term_Deposit_Specials.pdf'
        citi_file = urllib.URLopener()
        citi_file.retrieve(url, 'citi_td.pdf')
        text = parser.from_file('./citi_td.pdf')
         
        text = text['content']
        line = ''
        count = 0
        record = False
        rates = []
        
        for t in text:
            line = line + t
            if t == '\n':
                
                if 'Term and Rates' in line:
                    record = True

                if '*All rates are nominal' in line:
                    record = False

                if record:
                    rates.append(line)
                
                line = ''
        citi_td = [{
            'one_month': rates[2].split(' ')[3].split('%')[0],
            'two_month': rates[4].split(' ')[3].split('%')[0],
            'three_month': rates[6].split(' ')[3].split('%')[0],
            'four_month': rates[8].split(' ')[3].split('%')[0],
            'five_month': rates[10].split(' ')[3].split('%')[0],
            'six_month': rates[12].split(' ')[3].split('%')[0],
            'seven_month': rates[14].split(' ')[3].split('%')[0],
            'eight_month': rates[16].split(' ')[3].split('%')[0],
            'nine_month': rates[18].split(' ')[3].split('%')[0],
            'ten_month': rates[20].split(' ')[3].split('%')[0],
            'eleven_month': rates[20].split(' ')[3].split('%')[0],
            'twelve_month': rates[20].split(' ')[3].split('%')[0],
            'twentyfour_month': rates[20].split(' ')[3].split('%')[0],
            'thirtysix_month': rates[20].split(' ')[3].split('%')[0]
        }]

        bank = {
            'name': 'Citibank',
            'product': 'Term Deposit',
            'logo': 'citi.jpg',
            'notes': 'Amounts over 75k'
        }
        citi_td.append(bank)

        return citi_td


    def collate_td(self):
         
        term_deposit = []
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(private.username_gm, private.password_gm)
        
        print 'fetching rates for ANZ Standard...'
        try:
            anz_standard_td = self.get_anz_standard_td()
            term_deposit.append(anz_standard_td)
            print 'Success :-)'
        except:
            msg = """ 
            From: Ratemate\
            Subject: ANZ Standard has failed.
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
    

        print 'fetching rates for ANZ Advanced Notice...'
        try:
            print 'Success :-)'
            anz_advanced_td = self.get_anz_advanced_td()
            term_deposit.append(anz_advanced_td)
        except:
            print 'Failed :-('


        print 'fetching rates for Commonwealth Bank...'
        try:
            comm_td = self.get_comm_td()
            term_deposit.append(comm_td)
            print 'Success :-)'
        except:
            print 'Failed :-('
        

        print 'fetching rates for Westpac...'
        try:
            westpac_td = self.get_west_td()
            term_deposit.append(westpac_td)
            print 'Success :-)'
        except:
            print 'Failed :-('

        
        print 'fetching rates for NAB...'
        try:
            nab_td = self.get_nab_td()
            term_deposit.append(nab_td)
            print 'Success :-)'
        except: 
            print 'Failed :-('

        print 'fetching rates for St George...'
        try:
            george_td = self.get_george_td()
            term_deposit.append(george_td)
            print 'Success :-)'
        except:
            print 'Failed :-('
        
        print 'fetching rates for Bank West...'
        try:
            bankwest_td = self.get_bankwest_td()
            term_deposit.append(bankwest_td)
            print 'Success :-)'
        except:
            print 'Failed :-('
            
        
        print 'fetching rates for UBank Standard...'
        try:
            ubank_td = self.get_ubank_standard_td()
            term_deposit.append(ubank_td)
            print 'Success :-)'
        except:
            print 'Failed :-('

        
        print 'fetching rates for UBank Loyalty...'
        try:
            ubank_td = self.get_ubank_loyalty_td()
            term_deposit.append(ubank_td)
            print 'Success :-)'
        except:
            print 'Failed :-('


        print 'fetching rates for Bank of Queensland...'
        try:
            boq_td = self.get_boq_td()
            term_deposit.append(boq_td)
            print 'Success :-)'
        except:
            print 'Failed :-('
       

        print 'fetching rates for Rabo Direct...'
        try:
            rabo_td = self.get_rabo_td()
            term_deposit.append(rabo_td)
            print 'Success :-)'
        except:
            print 'Failed :-('
                

        print 'fetching rates for Bank of Melbourne...'
        try:
            bom_td = self.get_bom_td()
            term_deposit.append(bom_td)
            print 'Success :-)'
        except:
            print 'Failed :-('


        print 'fetching rates for ING...'
        try:
            ing_td = self.get_ing_td()
            term_deposit.append(ing_td)
            print 'Success :-)'
        except:
            print 'Failed :-('


        print 'fetching rates for Suncorp...'
        try:
            sun_td = self.get_sun_td() 
            term_deposit.append(sun_td)
            print 'Success :-)'
        except:
            print 'Failed :-('
        
        print 'fetching rates for Bendigo Bank...'
        try:
            bendigo_td = self.get_bendigo_td()
            term_deposit.append(bendigo_td)
            print 'Success :-)'
        except: 
            print 'Failed :-('
        

        print 'fetching rates for CitiBank...'
        try:    
            citi_td = self.get_citi_td()
            term_deposit.append(citi_td)
            print 'Success :-)'
        except:
            print 'Failed :-('
        
        flash('Rates have been successfuly updated!')
        
        return term_deposit
    


    """""""""""""""""""""""""""""
        Online Saver Scrapers
    """""""""""""""""""""""""""""

    def get_comm_online(self):
        url = 'https://www.commbank.com.au/personal/accounts/savings-accounts/netbank-saver/rates-fees.html'
        soup = self.get_soup(url)
        content = soup.find('div',{'class': 'productInfoContainer clearfix'})   
        rates = content.find_all('tr')[1:3]
    
        count = 0
        for rate in rates:
            if count == 0:
                total_rate = rate.find_all('td')[1].string.split('%')[0]
                
            if count == 1:
                base_rate = rate.find_all('td')[1].string.split('%')[0]
         
            count = count + 1

        comm_online = [{
            'base': base_rate,
            'bonus': float(total_rate) - float(base_rate),
            'total': total_rate
        }]
        
        bank = {
            'product': 'Netbank Saver',
            'name': 'CBA',
            'logo': 'cba.jpg',  
            'notes': 'Valid for 3 months.'
        }
        comm_online.append(bank)
         
        return comm_online
   

    def get_anz_online(self):
        url = 'https://www.anz.com.au/personal/bank-accounts/savings-accounts/online-saver/'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        
        base_rate = soup.find('span', {'class': 'productdata'}).string.split('%')[0]
        
        total_rate = soup.find('span', {'class': 'promodata'}).string.split('%')[0]
        
        bonus_rate = float(total_rate) - float(base_rate)
        
        anz_online = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]
        
        bank = {
            'product': 'Online Saver',
            'name': 'ANZ',
            'logo': 'anz.jpg',
            'notes': 'Valid for 3 months.'
        }
        anz_online.append(bank)

        return anz_online
    

    def get_westpac_online(self):
        url = 'https://www.westpac.com.au/personal-banking/bank-accounts/savings-accounts/esaver/'
        soup = self.get_soup(url)
        content = soup.find('ul',{'class': 'lists lists-tick'})   
        rates = content.find_all('li')
        
        base_rate = rates[1].string.split('%')[0]

        bonus_rate = rates[0].string.split('%')[0]

        total_rate = float(base_rate) + float(bonus_rate)
        
        westpac_online = [{
            'base' : base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'product': 'eSaver',
            'name': 'Westpac',
            'logo': 'westpac.jpg',
            'notes': 'Valid for 5 months.'
        }
        westpac_online.append(bank)
        
        return westpac_online

    
    def get_nab_online(self):
        url = 'https://www.nab.com.au/personal/banking/savings-accounts/nab-isaver'
        soup = self.get_soup(url)
        content = soup.find('ul', {'class': 'isaver-layout'})
        rates = content.find_all('li')

        base_rate = rates[0].find('p').string

        bonus_rate = rates[1].find('p').string
        
        total_rate = float(base_rate) + float(bonus_rate) 
        
        nab_online = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'product': 'iSaver',
            'name': 'NAB',
            'logo': 'nab.jpg',
            'notes': 'Valid for 4 months.'
        }
        nab_online.append(bank)
        
        return nab_online


    def get_george_online(self):        
        url = 'https://www.stgeorge.com.au/personal/bank-accounts/bank-account-interest-rates'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('span', {'data-rate-type': 'rates'})
        
        base_rate = rates[0].string
        
        bonus_rate = rates[1].string
        
        total_rate = rates[2].string

        george_online = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'product': 'Maxi Saver',
            'name': 'St George',
            'logo': 'george.jpg',
            'notes': 'Valid for 3 months.'
        }
        george_online.append(bank)

        return george_online
    
    
    def get_bankwest_online(self):
        url = 'http://www.bankwest.com.au/personal/savings-term-deposits/savings-accounts-term-deposits/telenet-saver'
        soup = self.get_soup(url)
        
        base_rate = soup.find('div', {'class': 'pbDetails'})
        base_rate = base_rate.find('span').string.split('%')[0]
        
        total_rate = soup.find('div', {'class': 'pbRate1'})
        total_rate = total_rate.find('span', {'class': 'pbFigures'}).string
        
        bonus_rate = float(total_rate) - float(base_rate)
        
        bankwest_online = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]
        
        bank = {
            'product': 'TeleNet Saver',
            'name': 'Bankwest',
            'logo': 'bankwest.jpg',
            'notes': 'Valid for 4 months.'
        }
        bankwest_online.append(bank)
        
        return bankwest_online

        
    def get_ubank_ultra_online(self):
        url = 'https://www.ubank.com.au/banking-overview/savings-accounts'
        soup = self.get_soup(url)
        content = soup.find('tbody')
        
        content = content.find_all('tr')
        
        total_rate = content[1].find_all('td')[2].string.split('%')[0]

        base_rate = content[1].find_all('td')[3].string.split('%')[0]
        
        bonus_rate = float(total_rate) - float(base_rate)

        ubank_online = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]
        
        bank = {
            'product': 'USaver with Ultra',
            'name': 'UBank',
            'logo': 'ubank.jpg',
            'notes': 'Valid for balances under 200k.'
        }
        ubank_online.append(bank)
        
        return ubank_online
    
    
    def get_boq_online(self):
        url = 'http://www.boq.com.au/todaysrates_investmentaccounts.htm'
        soup = self.get_soup(url)
        content = soup.find_all('tbody')
        content = content[0].find_all('tr')

        base_rate = content[1].find_all('td')[2].string.split('%')[0]

        total_rate = content[3].find_all('td')[2]
        total_rate = str(total_rate).split(' ')[0].split('%')[0].split('<td>')[1]
        
        bonus_rate = float(total_rate) - float(base_rate)
        
        boq_online = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'name': 'BOQ',
            'product': 'WebSaving Account',
            'logo': 'ubank.jpg',
            'notes': 'Valid for 4 months.'
        }
        boq_online.append(bank)
        
        return boq_online
    
    
    def get_citi_online(self):
        url = 'https://www.citibank.com.au/aus/banking/savings_accounts/citibank_online_saver.htm'
        soup = self.get_soup(url)
        content = soup.find_all('tbody')
        content = content[1].find_all('tr')

        total_rate = content[0].find_all('td')[1].string.split('%')[0]
       
        base_rate = content[1].find_all('td')[1].string.split('%')[0]
        
        bonus_rate = float(total_rate) - float(base_rate)
        bonus_rate = round(bonus_rate, 2)        

        citi_online = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'name': 'Citibank',
            'product': 'Online Saver',
            'logo': 'citi.jpg',
            'notes': 'Valid for 4 months.'
        }
        citi_online.append(bank)
        
        return citi_online
    
    
    def get_rabo_online(self):
        url = 'https://www.rabodirect.com.au/high-interest-savings-account/?gclid=CIam9IPnv9ICFQt0vQodCw8MOw'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'ratesContent'})
        rates = content.find_all('div', {'class': 'pull-right'})
        
        bonus_rate = rates[0].find('strong').string.split('%')[0]
        
        total_rate = rates[2].find('strong').string.split('%')[0]
        
        base_rate = float(total_rate) - float(bonus_rate)
        base_rate = round(base_rate, 2)

        rabo_online = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'name': 'RaboDirect',
            'product': 'Term Deposit',
            'logo': 'rabo.jpg',
            'notes': 'Valid for 4 months.'
        }
        rabo_online.append(bank)
        
        return rabo_online
   

    def get_bom_online(self):
        url = 'https://www.bankofmelbourne.com.au/personal/bank-and-save/savings-account/maxi-saver'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('span', {'class': 'korolev fontsize120'})
        
        total_rate = rates[1].find('span').string
        
        base_rate = rates[2].find('span').string
        
        bonus_rate = float(total_rate) - float(base_rate)
        
        bom_online = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'name': 'BOM',
            'product': 'Term Deposit',
            'logo': 'bom.jpg',
            'notes': 'Valid for 3 months.'
        }
        bom_online.append(bank)
        
        return bom_online

    
    def get_ing_online(self):
        url = 'https://www.campaigns.ingdirect.com.au/savings-and-everyday-banking?cid=ps:goo:brand|toplevel:sm&pkwd=ing-savings-maximiser'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        
        rates = soup.find_all('div', {'class': 'rate-value'})
        total_rate = rates[0].string
        
        bonus_rate = soup.find('div', {'class': 'small-description'}).string.split(' ')[1].split('%')[0]
        
        base_rate = float(total_rate) - float(bonus_rate)
        
        ing_online = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'name': 'ING Direct',
            'product': 'Savings Maximiser',
            'logo': 'ing.jpg',
            'notes': 'Valid for 1 month balance under 100k.'
        }
        ing_online.append(bank)
        
        return ing_online


    def collate_online_savers(self):
        
        online_saver = []
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(private.username_gm, private.password_gm)

        print 'fetching rates for ANZ Online Saver...'
        try:
            anz_online = self.get_anz_online()
            online_saver.append(anz_online)
            print 'Success :-)'
        except:
            msg = """\
            From: Ratemate\
            ANZ Online has failed.
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
        
        print 'fetching rates for CBA Netbank Saver...'
        try:
            comm_online = self.get_comm_online()
            online_saver.append(comm_online)
            print 'Success :-)'
        except:
            msg = """\
            From: Ratemate\
            CBA Netbak Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
            
        print 'fetching rates for Westpac eSaver...'
        try:
            westpac_online = self.get_westpac_online()
            online_saver.append(westpac_online)
            print 'Success :-)'
        except:
            msg = """\
            From: Ratemate\
            Westpac eSaver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
            

        print 'fetching rates for nab isaver...'
        try:
            nab_online = self.get_nab_online()
            online_saver.append(nab_online)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            NAB iSaver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         

        print 'fetching rates for St George Maxi Saver...'
        try:
            george_online = self.get_george_online()
            online_saver.append(george_online)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            St George Maxi Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         
        
        print 'fetching rates for Bankwest TeleNet Saver...'
        try:
            bankwest_online = self.get_bankwest_online()
            online_saver.append(bankwest_online)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            Bankwest Telenet Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         

        print 'fetching rates for UBank Usaver Ultra...'
        try:
            ubank_ultra_online = self.get_ubank_ultra_online()
            online_saver.append(ubank_ultra_online)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            UBank Usaver Ultra has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         
    
        print 'fetching rates for BOQ WebSaving...'
        try:
            boq_online = self.get_boq_online()
            online_saver.append(boq_online)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            BOQ WebSaving has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         

        print 'fetching rates for Citibank Online Saver...'
        try:
            citi_online = self.get_citi_online()
            online_saver.append(citi_online)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            Citibank Online Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         
        
        print 'fetching rates for Rabo Savings Account...'
        try:
            rabo_online = self.get_rabo_online()
            online_saver.append(rabo_online)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            Rabo Savings Account has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         
        
        print 'fetching rates for BOM Maxi Saver...'
        try:
            bom_online = self.get_bom_online()
            online_saver.append(bom_online)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            BOM Maxi Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         

        print 'fetching rates for ING Savings Maximiser...'
        try:
            ing_online = self.get_ing_online()
            online_saver.append(ing_online)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            ING Savings Maximiser has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
            
        flash('Scraping Online Savings Rates Completed.')

        return online_saver


    
    """""""""""""""""""""""""""
        Goal Saver Scrapers

    """""""""""""""""""""""""""

    def get_comm_progress(self):
        url = 'https://www.commbank.com.au/personal/accounts/savings-accounts/goalsaver/rates-fees.html'
        soup = self.get_soup(url)
        content = soup.find('ul',{'type': 'disc'})   
        
        bonus_rate = content.find_all('li')[0].find('b').string.split('%')[0]
        base_rate = content.find_all('li')[2].string.split(' ')[5].split('%')[0]

        comm_progress = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': float(base_rate) + float(bonus_rate)
        }]
        
        bank = {
            'product': 'GoalSaver',
            'name': 'CBA',
            'logo': 'cba.jpg',  
            'notes': 'Balances up to 100k and deposit at least $200 monthly.'
        }
        comm_progress.append(bank)
        
        return comm_progress
   

    def get_anz_progress(self):
        url = 'https://www.anz.com.au/personal/bank-accounts/savings-accounts/progress-saver/'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        print 'here'
        base_rate = soup.find_all('span', {'class': 'productdata'})[2].string.split('%')[0]

        bonus_rate = soup.find_all('span', {'class': 'productdata'})[0].string.split('%')[0]

        total_rate = float(base_rate) + float(bonus_rate)
        
        anz_progress = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]
        
        bank = {
            'product': 'Progress Saver',
            'name': 'ANZ',
            'logo': 'anz.jpg',
            'notes': 'No withdrawals and deposit over $10 monthly.'
        }
        anz_progress.append(bank)
        
        return anz_progress
    

    def get_westpac_progress(self):
        url = 'https://www.westpac.com.au/personal-banking/bank-accounts/savings-accounts/reward-saver/'
        soup = self.get_soup(url)
        content = soup.find('tbody')   
        content = content.find_all('tr')

        base_rate = content[0].find_all('td')[1]
        base_rate = str(base_rate).split(' ')[1].split('>')[1].split('%')[0]
        
        bonus_rate = content[1].find_all('td')[1].string.split('%')[0]

        total_rate = float(base_rate) + float(bonus_rate)
        
        westpac_progress = [{
            'base' : base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'product': 'Reward Saver',
            'name': 'Westpac',
            'logo': 'westpac.jpg',
            'notes': 'Desposit $50 monthly and no withdrawal.'
        }
        westpac_progress.append(bank)
        
        return westpac_progress

    
    def get_nab_progress(self):
        url = 'https://www.nab.com.au/personal/banking/savings-accounts/nab-reward-saver'
        soup = self.get_soup(url)
        content = soup.find_all('p', {'class': 'number'})
        
        base_rate = content[0].string

        bonus_rate = content[1].string

        total_rate = float(base_rate) + float(bonus_rate) 
        
        nab_progress = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'product': 'Reward Saver',
            'name': 'NAB',
            'logo': 'nab.jpg',
            'notes': 'No withdrawals and at least 1 deposit monthly.'
        }
        nab_progress.append(bank)
        
        return nab_progress


    def get_george_progress(self):        
        url = 'https://www.stgeorge.com.au/personal/bank-accounts/savings-accounts/incentive-saver'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find('tbody')
        rates = rates.find_all('tr')

        base_rate = rates[0].find_all('td')[1].string.split('%')[0]
        
        bonus_rate = rates[1].find_all('td')[1].string.split('%')[0]
        
        total_rate = float(base_rate) + float(bonus_rate)

        george_progress = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'product': 'Incentive Saver',
            'name': 'St George',
            'logo': 'george.jpg',
            'notes': 'No withdrawals and at least 1 deposit monthly.'
        }
        george_progress.append(bank)
        
        return george_progress
    
    
    def get_bankwest_smart_progress(self):
        url = 'http://www.bankwest.com.au/personal/savings-term-deposits/savings-accounts-term-deposits/smart-esaver'
        soup = self.get_soup(url)
        
        total_rate = soup.find_all('span', {'class': 'pbFigures'})[0].string

        base_rate = soup.find('div', {'class': 'pbDetails'})
        base_rate = base_rate.find_all('li')[1].find('span').string.split('%')[0]

        bonus_rate = float(total_rate) - float(base_rate)
        
        bankwest_progress = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]
        
        bank = {
            'product': 'Smart eSaver',
            'name': 'Bankwest',
            'logo': 'bankwest.jpg',
            'notes': 'No withdrawals / no deposit requirements.'
        }
        bankwest_progress.append(bank)
        
        return bankwest_progress
    
    
    def get_bankwest_hero_progress(self):
        url = 'http://www.bankwest.com.au/personal/savings-term-deposits/savings-accounts-term-deposits/hero-saver'
        soup = self.get_soup(url)
        
        total_rate = soup.find_all('span', {'class': 'pbFigures'})[0].string
        
        base_rate = soup.find_all('div', {'id': 'contentColumn'})[0].find_all('span')[0].string.split('%')[0]

        bonus_rate = float(total_rate) - float(base_rate)
        
        bankwest_hero = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]
        
        bank = {
            'product': 'Hero Saver',
            'name': 'Bankwest',
            'logo': 'bankwest.jpg',
            'notes': 'No withdrawals and minimum depsoit of $200 monthly.'
        }
        bankwest_hero.append(bank)
        
        return bankwest_hero
    
    
    def get_rabo_progress(self):
        url = 'https://www.rabodirect.com.au/rates/personal-rates/'
        soup = self.get_soup(url)
        content = soup.find_all('tbody')
        rates = content[4].find_all('tr')

        total_rate = rates[0].find_all('td')[1].string.strip()
        
        base_rate = rates[0].find_all('td')[2].string.strip()
        
        bonus_rate = float(total_rate) - float(base_rate)

        rabo_progress = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'name': 'RaboDirect',
            'product': 'Premium Saver',
            'logo': 'rabo.jpg',
            'notes': 'Balance must increase by $200 monthly.'
        }
        rabo_progress.append(bank)
        
        return rabo_progress
   

    def get_bom_progress(self):
        url = 'https://www.bankofmelbourne.com.au/personal/bank-and-save/savings-account/incentive-saver'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('span', {'class': 'js-rates'})
        
        total_rate = rates[0].string

        base_rate = rates[1].string

        bonus_rate = float(total_rate) + float(base_rate)
        
        bom_progress = [{
            'base': base_rate,
            'bonus': bonus_rate,
            'total': total_rate
        }]

        bank = {
            'name': 'BOM',
            'product': 'Incentive Saver',
            'logo': 'bom.jpg',
            'notes': 'No mimimum monthly deposit.'
        }
        bom_progress.append(bank)
        return bom_progress


        
    def collate_progress_saver(self):
        
        progress_saver = []
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(private.username_gm, private.password_gm)

        print 'fetching rates for ANZ Progress Saver...'
        try:
            anz_progress = self.get_anz_progress()
            progress_saver.append(anz_progress)
            print 'Success :-)'
        except:
            msg = """\
            From: Ratemate\
            ANZ Progress has failed.
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
        
        print 'fetching rates for CBA Goal Saver...'
        try:
            comm_progress = self.get_comm_progress()
            progress_saver.append(comm_progress)
            print 'Success :-)'
        except:
            msg = """\
            From: Ratemate\
            CBA Goal Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
            
        print 'fetching rates for Westpac Reward Saver...'
        try:
            westpac_progress = self.get_westpac_progress()
            progress_saver.append(westpac_progress)
            print 'Success :-)'
        except:
            msg = """\
            From: Ratemate\
            Westpac Reward Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
            

        print 'fetching rates for NAB Reward Saver...'
        try:
            nab_progress = self.get_nab_progress()
            progress_saver.append(nab_progress)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            NAB Reward Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         

        print 'fetching rates for St George Incentive Saver...'
        try:
            george_progress = self.get_george_progress()
            progress_saver.append(george_progress)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            St George Incentive Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         
        
        print 'fetching rates for Bankwest Smart eSaver...'
        try:
            bankwest_smart_progress = self.get_bankwest_smart_progress()
            progress_saver.append(bankwest_smart_progress)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            Bankwest Smart eSaver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         

        print 'fetching rates for Bankwest Hero Saver...'
        try:
            bankwest_hero_progress = self.get_bankwest_hero_progress()
            progress_saver.append(bankwest_hero_progress)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            Bankwest Hero Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         
    
        print 'fetching rates for Rabo Premium Saver...'
        try:
            rabo_progress = self.get_rabo_progress()
            progress_saver.append(rabo_progress)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            Rabo Premium Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         

        print 'fetching rates for BOM Incentive Saver...'
        try:
            bom_progress = self.get_bom_progress()
            progress_saver.append(bom_progress)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            BOM Incentive Saver has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         
        flash('Scraping Online Savings Rates Completed.')

        return progress_saver

        

    """""""""""""""""""""""""""
    CASH MANAGER SCRAPERS

    """""""""""""""""""""""""""

    def get_comm_cash(self):
        url = 'https://www.commbank.com.au/personal/accounts/savings-accounts/commonwealth-direct-investment/rates-fees.html'
        soup = self.get_soup(url)
        content = soup.find('tbody')   
        content = content.find_all('tr')
        
        _500k = content[3].find_all('td')[1].find('p').string.split('%')[0]
        
        _250k = content[4].find_all('td')[1].find('p').string.split('%')[0]
        
        _100k = content[5].find_all('td')[1].find('p').string.split('%')[0]

        _50k = content[6].find_all('td')[1].find('p').string.split('%')[0]

        comm_cash = [{
            '500k and over': _500k,
            '250k - 500k': _250k,
            '100k - 250k': _100k,
            '50k - 100k': _50k
        }]
        
        bank = {
            'product': 'Direct Investment Account',
            'name': 'CBA',
            'logo': 'cba.jpg',  
            'notes': 'Standard Access.'
        }
        comm_cash.append(bank)
        
        return comm_cash
   

    def get_anz_cash(self):
        url = 'https://www.anz.com.au/personal/bank-accounts/savings-accounts/premium-cash-management/'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        
        rate = soup.find_all('tbody')
        rate = rate[1].find_all('tr')

        _500k = rate[6].find_all('td')[0].find('p').string.split('%')[0]

        _250k = rate[5].find_all('td')[0].find('p').string.split('%')[0]
        
        _100k = rate[4].find_all('td')[0].find('p').string.split('%')[0]
        
        _50k = rate[3].find_all('td')[0].find('p').string.split('%')[0]

        anz_cash = [{
            '500k and over': _500k,
            '250k - 500k': _250k,
            '100k - 250k': _100k,
            '50k - 100k': _50k
        }]
        
        bank = {
            'product': 'Premium Cash Management Account',
            'name': 'ANZ',
            'logo': 'anz.jpg',
            'notes': ''
        }
        anz_cash.append(bank)
        
        return anz_cash
   
    
    def get_nab_cash(self):
        url = 'https://www.nab.com.au/personal/banking/savings-accounts/nab-cash-manager'
        soup = self.get_soup(url)
        content = soup.find_all('p', {'class': 'number'})[0].string
    
        rate = content
        
        nab_cash = [{
            '500k and over': rate,
            '250k - 500k': rate,
            '100k - 250k': rate,
            '50k - 100k': rate 
        }]

        bank = {
            'product': 'Cash Manager',
            'name': 'NAB',
            'logo': 'nab.jpg',
            'notes': 'Minimium depsoit $5k then no minimum account balance.'
        }
        nab_cash.append(bank)
        
        return nab_cash


    def get_george_cash(self):        
        url = 'https://www.stgeorge.com.au/personal/bank-accounts/savings-accounts/investment-cash-account'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('tbody')
        rates = rates[1].find_all('tr') 
        
        _50k = rates[4].find_all('td')[1].find('span').string
        
        _100k = rates[5].find_all('td')[1].find('span').string

        _250k = rates[6].find_all('td')[1].find('span').string
        
        _500k = rates[7].find_all('td')[1].find('span').string

        george_cash = [{
            '500k and over': _500k,
            '250k - 500k': _250k,
            '100k - 250k': _100k,
            '50k - 100k': _50k
        }]

        bank = {
            'product': 'Cash Investment Account',
            'name': 'St George',
            'logo': 'george.jpg',
            'notes': ''
        }
        george_cash.append(bank)
         
        return george_cash
    
    
    def collate_cash(self):
        
        cash_manager = []
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(private.username_gm, private.password_gm)

        print 'fetching rates for ANZ Premium Cash Manager...'
        try:
            anz_cash = self.get_anz_cash()
            cash_manager.append(anz_cash)
            print 'Success :-)'
        except:
            msg = """\
            From: Ratemate\
            ANZ Cash Manager has failed.
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
        
        print 'fetching rates for CBA Direct Investment...'
        try:
            comm_cash = self.get_comm_cash()
            cash_manager.append(comm_cash)
            print 'Success :-)'
        except:
            msg = """\
            From: Ratemate\
            CBA Direct Investement has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
            

        print 'fetching rates for NAB Cash Manager...'
        try:
            nab_cash = self.get_nab_cash()
            cash_manager.append(nab_cash)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            NAB Cash Manager has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         

        print 'fetching rates for St George Investment Cash...'
        try:
            george_cash = self.get_george_cash()
            cash_manager.append(george_cash)
            print 'success :-)'
        except:
            msg = """\
            from: ratemate\
            St George Investment Cash has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'failed :-('
         
        
        flash('Scraping Cash Managment Accounts Completed.')

        return cash_manager

        


    """""""""""""""""""""""""""
    PENSIONER SCRAPERS

    """""""""""""""""""""""""""

    def get_comm_pensioner(self):
        url = 'https://www.commbank.com.au/personal/accounts/transaction-accounts/pensioner-security.html'
        soup = self.get_soup(url)
        content = soup.find('tbody').find_all('tr')   

        _0k = content[0].find_all('p')[1]
        _0k = str(_0k).split(' ')[0].split('%')[0].split('>')[1]
        
        _2k = content[1].find_all('p')[1]
        _2k = str(_2k).split('%')[0].split('>')[1]
        
        _5k = content[2].find_all('p')[1]
        _5k = str(_5k).split('%')[0].split('%')[0].split('>')[1]
        
        comm_pensioner = [{
            '0k': _0k,
            '2k': _2k,
            '5k': _5k
        }]
        
        bank = {
            'product': 'Pensioner Security Account',
            'name': 'CBA',
            'logo': 'cba.jpg',  
            'notes': ''
        }
        comm_pensioner.append(bank)
        
        return comm_pensioner
   

    def get_anz_pensioner(self):
        url = 'https://www.anz.com.au/personal/bank-accounts/everyday-accounts/pensioner-advantage/'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        
        rate = soup.find_all('tbody')
        _0k = rate[0].find_all('tr')[2].find('span').string.split('%')[0]
        
        _2k = rate[0].find_all('tr')[3].find('span').string.split('%')[0]
        
        _5k = rate[0].find_all('tr')[4].find('span').string.split('%')[0]
        
        anz_pensioner = [{
            '0k': _0k,
            '2k': _2k,
            '5k': _5k
        }]
        
        bank = {
            'product': 'Pensioner Advantage',
            'name': 'ANZ',
            'logo': 'anz.jpg',
            'notes': ''
        }
        anz_pensioner.append(bank)
        
        return anz_pensioner
   
 
    def collate_pensioner(self):
        
        pensioner = []
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(private.username_gm, private.password_gm)


        print 'fetching rates for ANZ Pensioner Advantage...'
        try:
            anz_pensioner = self.get_anz_pensioner()
            pensioner.append(anz_pensioner)
            print 'Success :-)'
        except:
            msg = """\
            From: Ratemate\
            ANZ Pensioner has failed.
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
       

        print 'fetching rates for CBA Pensioner Security...'
        try:
            comm_pensioner = self.get_comm_pensioner()
            pensioner.append(comm_pensioner)
            print 'Success :-)'
        except:
            msg = """\
            From: Ratemate\
            CBA Pensioner has failed..
            """
            server.sendmail('dtoumbourou@gmail.com', 'dtoumbourou@gmail.com', msg,)
            print 'Failed :-('
                
        
        flash('Scraping Pensioner Accounts Completed.')

        return pensioner

        
    
