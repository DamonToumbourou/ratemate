from bs4 import BeautifulSoup as bs4
from requests import get
from selenium import webdriver
import requests
import time
import re

PHANTOMJS_PATH = './phantomjs'

class WebScrapers(object):
    

    def get_soup(self, url):
        request = requests.get(url)
        soup = bs4(request.text, 'html.parser')
        
        return soup


    def get_comm_td(self):
        """
        comm_td = [
            {
                'short': [
                    'days': days,
                    'rate': rate
                ]
            },
            {
                'mid': [
                    'days': days,
                    'rate': rate
                ]
            },
            {
                'long_': [
                    'days': days,
                    'rate': rate
                ]
            }
        ] 
        """
        url = 'https://www.commbank.com.au/personal/accounts/term-deposits/rates-fees.html'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'column full-col'})
        
        links = content.find_all('tr')

        term_comm = []
        for link in links:
            
            string = link.find('p').string
            if '3' in string:
                if '6' not in string:
                    rate = string.split('m', 1)[0]
                    days_90 = link.find('div', {'class': 'path52 tablecell'})
                    short = {
                        'months': days_90.find('p').string,
                        'rate': rate
                    }
                    term_comm.append(short)

            if '7' in string:
                if '36' not in string:
                    rate = string.split('m', 1)[0]
                    days_210 = link.find('div', {'class': 'path42 tablecell'})
                    
                    mid = { 
                        'months': days_210.find('p').string,
                        'rate': rate
                    }
                    term_comm.append(mid)

            if '12' in string:
                rate = string.split('m', 1)[0]
                days_360 = link.find('div', {'class': 'path32 tablecell'})
                
                long_ = {
                    'months': days_360.find('p').string,
                    'rate': rate
                }
                term_comm.append(long_)

        return term_comm

    
    def get_anz_td(self):
        """
        anz_td = [{
            'standard': [
                'short': {
                    'days': days,
                    'rate': rate,
                }
                'mid': {
                    'days': days,
                    'rate': rate,
                }
                'long': {
                    'days': days,
                    'rate' rate,
                }
            },
        """
        url = 'https://www.anz.com.au/personal/bank-accounts/compare/term-deposits'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        content = soup.find_all('span', {'data-subsection': 'ANTD'})
        
        count = 0
        anz_td = []
        advanced = []
        standard = []
        for rates in content:
            
            if count is 0:
                short = {
                    'months': '3',
                    'rate': rates.string
                }
                advanced.append(short)
            
            if count is 2:
                mid = {
                    'months': '6',
                    'rate': rates.string
                }
                advanced.append(mid)

            if count is 3:
                long_ = {
                    'months': '12',
                    'rate': rates.string
                }
                advanced.append(long_)
            
            if count is 4:
                short = {
                    'months': '3',
                    'rate': rates.string
                }
                standard.append(short)

            if count is 6:
                mid = {
                    'months': '6',
                    'rate': rates.string
                }
                standard.append(mid)

            if count is 7:
                long_ = {
                    'months': '12',
                    'rate': rates.string
                }
                standard.append(long_)

            count = count + 1
        
        anz_td.append(advanced)
        anz_td.append(standard)
        
        return anz_td
    

    def get_west_td(self):
        url = 'https://www.westpac.com.au/personal-banking/bank-accounts/term-deposit/'
        soup = self.get_soup(url)
        content = soup.find('div', {'id': 'tab1'})
        
        rates = content.find_all('tr')

        west_td = []
        for rate in rates[0:15]:
            search = rate.find('td', {'scope': 'row'})
            
            if search is not None:
                if search.findAll(text=re.compile('3\xa0< 4')):
                    
                    short = { 
                        'months': '3',
                        'rate': rate.find_all('td')[4].string
                    }
                    west_td.append(short)

                if search.findAll(text=re.compile('6\xa0< 7')):

                    mid = {
                        'months': '6',
                        'rate': rate.find_all('td')[4].string
                    }
                    west_td.append(mid)

                if search.findAll(text=re.compile('12\xa0< 24')):
                    
                    long_ = {
                        'months': '12',
                        'rate': rate.find_all('td')[4].string
                    }
                    west_td.append(long_)
        
        return west_td    

    
    def get_nab_td(self):
        url = 'http://www.nab.com.au/personal/interest-rates-fees-and-charges/indicator-rates-selected-term-deposit-products'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'parbase table section'})
        rates = content.find_all('tr')

        nab_td = []
        for rate in rates:
            
            if '90 days*' == rate.find('td').string:
                
                short = {
                    'months': '3',
                    'rate': rate.find_all('td')[1].string.split()[0]
                }
                nab_td.append(short) 
                
            if '6 months*' == rate.find('td').string:
                
                mid = {
                    'months': '6',
                    'rate': rate.find_all('td')[1].string.split()[0]
                }
                nab_td.append(mid)
            
            if '8 months*' == rate.find('td').string:
                
                mid = {
                    'months': '8',
                    'rate': rate.find_all('td')[1].string.split()[0]
                }
                nab_td.append(mid)

            if '12 months*' == rate.find('td').string:
                
                long_ = {
                    'months': '12',
                    'rate': rate.find_all('td')[1].string.split()[0]
                }
                nab_td.append(long_)
        
        return nab_td


    def get_george_td(self):
        url = 'https://www.stgeorge.com.au/personal/bank-accounts/term-deposits'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('tr')
        
        george_td = []
        for rate in rates[0:15]:
            found = rate.find('td')
            if found is not None:
                
                if '3 to less than 4' in found.string:
                    found_rate = rate.find_all('td')[6]
                    
                    short = {
                        'months': '3',
                        'rate': found_rate.find('span').string
                    }
                    george_td.append(short)
                
                if '6 to less than 7' in found.string:
                    found_rate = rate.find_all('td')[6]
                    
                    mid = {
                        'months': '6',
                        'rate': found_rate.find('span').string
                    }
                    george_td.append(mid)

                if '12 months' == found.string:
                    found_rate = rate.find_all('td')[6]
                    
                    long_ = {
                        'months': '12',
                        'rate': found_rate.find('span').string
                    }
                    george_td.append(long_)

        return george_td
       
    
    def get_bankwest_td(self):
        url = 'http://www.bankwest.com.au/personal/savings-term-deposits/savings-accounts-term-deposits/gold-term-deposit?tab=rates-fees'
        soup = self.get_soup(url)
        content = soup.find('table', {'class': 'ratesTable'})
        rates = content.find_all('tr')

        bankwest_td = []
        for rate in rates:
            
            if '3 months' == rate.find('th').string:
                short = {
                    'months': '3',
                    'rate': rate.find('span').string.split()[0]
                }
                bankwest_td.append(short)
            
            if '7 months' == rate.find('th').string:
                mid = {
                    'months': '7',
                    'rate': rate.find('span').string.split()[0]
                }
                bankwest_td.append(mid)
                    
            if '12 months' == rate.find('th').string:
                rat = rate.find_all('span')
                long_ = {
                    'months': '12',
                    'rate': rat[3].string.split()[0]
                }
                bankwest_td.append(long_)
        
        return bankwest_td


    def get_ubank_td(self):
        url = 'https://www.ubank.com.au/banking-overview/term-deposits#rates'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'table-responsive rate-table-rhs'})
        rates = content.find_all('tr')

        ubank_td = []
        standard = []
        loyalty = []
        for rate in rates:
            found = rate.find('td')
            if found is not None:
                if 'UBank - Standard rate' in found.string: 
                    stand = rate.find_all('td')
                    
                    short = { 
                        'months': '3',
                        'rate': stand[1].string
                    }
                    standard.append(short)
                    
                    mid = { 
                        'months': '6',
                        'rate': stand[3].string
                    }
                    standard.append(mid)
                    
                    long_ = { 
                        'months': '12',
                        'rate': stand[5].string
                    }
                    standard.append(long_)
                    
                if 'UBank - with Loyalty Bonus' in found.string: 
                    stand = rate.find_all('td')
                    
                    short = { 
                        'months': '3',
                        'rate': stand[1].string
                    }
                    loyalty.append(short)
                    
                    mid = { 
                        'months': '6',
                        'rate': stand[3].string
                    }
                    loyalty.append(mid)
                    
                    long_ = { 
                        'months': '12',
                        'rate': stand[5].string
                    }
                    loyalty.append(long_)

        ubank_td.append([{
            'standard': standard, 
            'loyalty': loyalty
        }])

        return ubank_td
    

    def get_boq_td(self):
        url = 'http://www.boq.com.au/todays_rates_term_deposits.htm'
        soup = self.get_soup(url)
        content = soup.find_all('table')
        rates = content[1].find_all('tr')

        boq_td = []
        for rate in rates:
            curr = rate.find('td').string
            if curr is not None:
                
                if '3 less than 4' in curr:
                    short = {
                        'months': '3',
                        'rate' : rate.find_all('td')[3].string
                    }
                    boq_td.append(short)

                if '6 less than 7' in curr:
                    mid = {
                        'months': '6',
                        'rate' : rate.find_all('td')[3].string
                    }
                    boq_td.append(mid)
                 
                if '12 less than 24' in curr:
                    long_ = {
                        'months': '12',
                        'rate' : rate.find_all('td')[3].string
                    }
                    boq_td.append(long_)
        
        return boq_td
    

    def get_rabo_td(self):
        url = 'https://www.rabodirect.com.au/rates/personal-rates/'
        soup = self.get_soup(url)
        content = soup.find_all('table', {'class': 'rates-table responsive'})
        rates = content[5].find_all('tr')
        
        rabo_td = []
        for rate in rates:
            curr = rate.find_all('td')
            if curr:
                
                if '3 months' in curr[0].string:
                    short = {
                        'months': '3',
                        'rate': curr[1].string.strip()
                    }
                    rabo_td.append(short)
                
                if '6 months' in curr[0].string:
                    mid = {
                        'months': '6',
                        'rate': curr[1].string.strip()
                    }
                    rabo_td.append(mid)
                
                if '1 year' in curr[0].string:
                    long_ = {
                        'months': '12',
                        'rate': curr[5].string.strip()
                    }
                    rabo_td.append(long_)
        print rabo_td
        return rabo_td

     
    def get_bom_td(self):
        url = 'https://www.bankofmelbourne.com.au/help/interest-rates/fixed-term-deposits'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('table', {'class': 'table table-striped table-bordered'})
        content = rates[0].find_all('tr') 

        bom_td = []
        for rate in content: 
            curr = rate.find('th').string
            if curr:
                
                if '3 to less than 4 months' in curr:
                    short = {
                        'months': '3',
                        'rate': rate.find('span').string
                    }
                    bom_td.append(short)
                
                if '6 to less than 7 months' in curr:
                    mid = {
                        'months': '6',
                        'rate': rate.find('span').string
                    }
                    bom_td.append(mid)

                if '12 months' == curr:
                    long_ = {
                        'months': '12',
                        'rate': rate.find('span').string
                    }
                    bom_td.append(long_)
        
        return bom_td

    
    def get_ing_td(self):
        url = 'https://www.ingdirect.com.au/savings/term-deposit.html'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('div', {'class': 'table-row data'})

        ing_td = []
        for rate in rates:
            curr = rate.find('p').string
            
            if '90 day rate' in curr: 
                short = {
                    'months': '3',
                    'rate': rate.find('span').string
                }
                ing_td.append(short)

            if '120 day rate' in curr:
                short = {
                    'months': '4',
                    'rate': rate.find('span').string
                }
                ing_td.append(short)

            if '210 day rate' in curr:
                mid = {
                    'months': '7',
                    'rate': rate.find('span').string
                }
                ing_td.append(mid)

            if '1 year rate' in curr:
                long_ = {
                    'months': '12',
                    'rate': rate.find('span').string
                }
                ing_td.append(long_)
        
        note = {
            'note': 'loyalty bonus +.10',
            'interest': 'on maturity'
        }
        ing_td.append(note)
        
        return ing_td
     

    def get_sun_td(self):
        url = 'https://www.suncorp.com.au/banking/investments/term-deposits.html'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('span', {'class': 'rate'})
    
        sun_td = [{
            'months': '3',
            'rate': rates[0].string
        },
        {
            'months': '6',
            'rate': rates[1].string
        },
        {
            'months': '12',
            'rate': rates[2].string
        }]    
        
        return sun_td
          

    def get_bendigo_td(self):
        url = 'http://www.bendigobank.com.au/public/personal/term-deposits/term-deposit-interest-rates'         
        soup = self.get_soup(url)
        content = soup.find_all('table', {'style': 'width: 100%'})
        rates = content[1].find_all('tr')
        
        bendigo_td = []
        for rate in rates:
           
            curr = rate.find('td')
            if curr is not None:
                curr_rate = rate.find_all('td')
                
                if '3 Months' == curr.string:
                    short = {
                        'months': '3',
                        'rate': curr_rate[1].string
                    }
                    bendigo_td.append(short)
                
                if '6 Months' == curr.string:
                    mid = {
                        'months': '6',
                        'rate': curr_rate[1].string
                    }
                    bendigo_td.append(mid)
                
                if '12 Months' == curr.string:
                    long_ = {
                        'months': '12',
                        'rate': curr_rate[1].string
                    }
                    bendigo_td.append(long_)

        return bendigo_td
    
    
    def get_citi_td(self):
        url = 'https://www.citibank.com.au/term-deposit/?intcid=BN-Productpage-MidpageTD-RET'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'box blue_box'})
        rate = str(content.find('h2'))
        rate = rate.split('>')[1]
        rate = rate.split('<')[0].split()[0]
        
        citi_td = [{
            'month': '6',
            'rate': rate
        }]
        return citi_td


    def collate_td(self):
        #anz_td = self.get_anz_td()
        #comm_td = self.get_comm_td()
        #westpac_td = self.get_west_td()
        #nab_td = self.get_nab_td()
        #george_td = self.get_george_td()
        #bankwest_td = self.get_bankwest_td()
        #ubank_td = self.get_ubank_td()
        #boq_td = self.get_boq_td()
        #rabo_td = self.get_rabo_td()
        #bom_td = self.get_bom_td()
        #ing_td = self.get_ing_td()
        #sun_td = self.get_sun_td() 
        #bendigo_td = self.get_bendigo_td()
        citi_td = self.get_citi_td()


        return None
