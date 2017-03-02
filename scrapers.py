from bs4 import BeautifulSoup as bs4
from requests import get
from selenium import webdriver
from flask import flash
import requests
import time
import re
import smtplib
import private

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
        
        term_comm = []
        
        short = {
            'days': '90',
            'rate': soup.find('div', {'class': 'path52 tablecell'}).find('p').string.split()[0]
        }
        term_comm.append(short)
        mid = {
            'days': '210',
            'rate': soup.find('div', {'class': 'path42 tablecell'}).find('p').string.split()[0]
        }
        term_comm.append(mid)
        long_ = {
            'days': '360',
            'rate': soup.find('div', {'class': 'path32 tablecell'}).find('p').string.split()[0]
        }
        term_comm.append(long_)

        bank = {
            'name': 'CBA',
            'logo': 'https://s0.yellowpages.com.au/1032b3ff-284c-4cae-a4a0-7f3678a7b017/commonwealth-bank-home-lending-solutions-highett-3190-logo.jpg'
        }
        term_comm.append(bank)
        
        return term_comm

    
    def get_anz_advanced_td(self):
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
        for rates in content:
            
            if count is 0:
                short = {
                    'days': '90',
                    'rate': rates.string.split()[0]
                }
                anz_td.append(short)
            
            if count is 2:
                mid = {
                    'days': '120',
                    'rate': rates.string.split()[0]
                }
                anz_td.append(mid)

            if count is 3:
                long_ = {
                    'days': '360',
                    'rate': rates.string.split()[0]
                }
                anz_td.append(long_)
            
            count = count + 1
            
        bank = { 
            'name': 'ANZ Advanced',
            'logo': 'https://pbs.twimg.com/profile_images/706597288299212800/xRvtFYma_400x400.jpg'
        }
        anz_td.append(bank)

        return anz_td
    
    
    def get_anz_standard_td(self):
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
        for rates in content:
            
            if count is 4:
                short = {
                    'days': '90',
                    'rate': rates.string.split()[0]
                }
                anz_td.append(short)

            if count is 6:
                mid = {
                    'days': '180',
                    'rate': rates.string.split()[0]
                }
                anz_td.append(mid)

            if count is 7:
                long_ = {
                    'days': '360',
                    'rate': rates.string.split()[0]
                }
                anz_td.append(long_)
            
            count = count + 1
            
        bank = { 
            'name': 'ANZ Standard',
            'logo': 'https://pbs.twimg.com/profile_images/706597288299212800/xRvtFYma_400x400.jpg'
        }
        anz_td.append(bank)

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
                        'days': '90',
                        'rate': rate.find_all('td')[4].string
                    }
                    west_td.append(short)

                if search.findAll(text=re.compile('6\xa0< 7')):

                    mid = {
                        'days': '180',
                        'rate': rate.find_all('td')[4].string
                    }
                    west_td.append(mid)

                if search.findAll(text=re.compile('12\xa0< 24')):
                    
                    long_ = {
                        'days': '360',
                        'rate': rate.find_all('td')[4].string
                    }
                    west_td.append(long_)
        
        bank = {
            'name': 'Westpac',
            'logo': 'https://pbs.twimg.com/profile_images/695349302118391808/hC-wlVS6_400x400.jpg'
        }
        west_td.append(bank)
        
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
                    'days': '90',
                    'rate': rate.find_all('td')[1].string.split()[0]
                }
                nab_td.append(short) 
                
            if '8 months*' == rate.find('td').string:
                
                mid = {
                    'days': '240',
                    'rate': rate.find_all('td')[1].string.split()[0]
                }
                nab_td.append(mid)

            if '12 months*' == rate.find('td').string:
                
                long_ = {
                    'days': '360',
                    'rate': rate.find_all('td')[1].string.split()[0]
                }
                nab_td.append(long_)
        
        bank = {
            'name': 'NAB',
            'logo': 'https://pbs.twimg.com/profile_images/820753240648130561/tWPXUFde_reasonably_small.jpg'
        }
        nab_td.append(bank)

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
                    found_rate = rate.find_all('td')[5]
                    
                    short = {
                        'days': '90',
                        'rate': found_rate.find('span').string + '%'
                    }
                    george_td.append(short)
                
                if '6 to less than 7' in found.string:
                    found_rate = rate.find_all('td')[5]
                    
                    mid = {
                        'days': '180',
                        'rate': found_rate.find('span').string + '%'
                    }
                    george_td.append(mid)

                if '12 months' == found.string:
                    found_rate = rate.find_all('td')[5]
                    
                    long_ = {
                        'days': '360',
                        'rate': found_rate.find('span').string + '%'
                    }
                    george_td.append(long_)

        bank = {
            'name': 'St George',
            'logo': 'https://lh3.googleusercontent.com/-bJWvppmM7qc/AAAAAAAAAAI/AAAAAAAAAIQ/8bilcXY9y5M/s120-c/photo.jpg'
        }
        george_td.append(bank)

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
                    'days': '90',
                    'rate': rate.find('span').string.split()[0]
                }
                bankwest_td.append(short)
            
            if '7 months' == rate.find('th').string:
                mid = {
                    'days': '210',
                    'rate': rate.find('span').string.split()[0]
                }
                bankwest_td.append(mid)
                    
            if '12 months' == rate.find('th').string:
                rat = rate.find_all('span')
                long_ = {
                    'days': '360',
                    'rate': rat[3].string.split()[0]
                }
                bankwest_td.append(long_)
        
        bank = {
            'name': 'Bankwest',
            'logo': 'http://is3.mzstatic.com/image/thumb/Purple22/v4/d7/d0/3a/d7d03a65-e915-23e9-287e-9a630767edd9/source/175x175bb.jpg'
        }
        bankwest_td.append(bank)
        
        return bankwest_td


    def get_ubank_td(self):
        url = 'https://www.ubank.com.au/banking-overview/term-deposits#rates'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'table-responsive rate-table-rhs'})
        rates = content.find_all('tr')

        ubank_td = []
        for rate in rates:
            found = rate.find('td')
            if found is not None:
                if 'UBank - with Loyalty Bonus' in found.string: 
                    stand = rate.find_all('td')
                    
                    short = { 
                        'days': '90',
                        'rate': stand[1].string
                    }
                    ubank_td.append(short)
                    
                    mid = { 
                        'days': '180',
                        'rate': stand[3].string
                    }
                    ubank_td.append(mid)
                    
                    long_ = { 
                        'days': '360',
                        'rate': stand[5].string
                    }
                    ubank_td.append(long_)
                    
        bank = {
            'name': 'UBank Loyalty Bonus',
            'logo': 'https://pbs.twimg.com/profile_images/816872981175484416/BwQu6mb-.jpg'
        }
        ubank_td.append(bank)

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
                        'days': '90',
                        'rate' : rate.find_all('td')[3].string.split('*')[0] + '%'
                    }
                    boq_td.append(short)

                if '6 less than 7' in curr:
                    mid = {
                        'days': '180',
                        'rate' : rate.find_all('td')[3].string.split('*')[0] + '%'
                    }
                    boq_td.append(mid)
                 
                if '12 less than 24' in curr:
                    long_ = {
                        'days': '360',
                        'rate' : rate.find_all('td')[3].string.split('*')[0] + '%'
                    }
                    boq_td.append(long_)
        
        bank = {
            'name': 'BOQ',
            'logo': 'https://pbs.twimg.com/profile_images/458816630949019649/ggOeeSFX_400x400.jpeg'
        }
        boq_td.append(bank)

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
                        'days': '90',
                        'rate': curr[1].string.strip() + '%'
                    }
                    rabo_td.append(short)
                
                if '6 months' in curr[0].string:
                    mid = {
                        'days': '180',
                        'rate': curr[1].string.strip() + '%'
                    }
                    rabo_td.append(mid)
                
                if '1 year' in curr[0].string:
                    long_ = {
                        'days': '360',
                        'rate': curr[5].string.strip() + '%'
                    }
                    rabo_td.append(long_)

        bank = {
            'name': 'RaboDirect',
            'logo': 'https://www.rabobank.com/en/images/rabobank-logo68x80.jpg'
        }
        rabo_td.append(bank)

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
                        'days': '90',
                        'rate': rate.find('span').string + '%'
                    }
                    bom_td.append(short)
                
                if '6 to less than 7 months' in curr:
                    mid = {
                        'days': '180',
                        'rate': rate.find('span').string + '%'
                    }
                    bom_td.append(mid)

                if '12 months' == curr:
                    long_ = {
                        'days': '360',
                        'rate': rate.find('span').string + '%'
                    }
                    bom_td.append(long_)
        
        bank = {
            'name': 'BOM',
            'logo': 'https://pbs.twimg.com/profile_images/617918130505908225/NxsY5iOB.jpg'
        }
        bom_td.append(bank)

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
                    'days': '90',
                    'rate': rate.find('span').string + '%'
                }
                ing_td.append(short)

            if '210 day rate' in curr:
                mid = {
                    'days': '210',
                    'rate': rate.find('span').string + '%'
                }
                ing_td.append(mid)

            if '1 year rate' in curr:
                long_ = {
                    'days': '360',
                    'rate': rate.find('span').string + '%'
                }
                ing_td.append(long_)
        
        bank = {
            'name': 'ING Direct',
            'logo': 'http://investukraine.net/wordpress/wp-content/uploads/2016/08/ing.jpeg'
        }
        ing_td.append(bank)
        
        return ing_td
     

    def get_sun_td(self):
        url = 'https://www.suncorp.com.au/banking/investments/term-deposits.html'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('span', {'class': 'rate'})
    
        sun_td = [{
            'days': '90',
            'rate': rates[0].string
        },
        {
            'days': '180',
            'rate': rates[1].string
        },
        {
            'days': '360',
            'rate': rates[2].string
        }]    
        
        bank = {
            'name': 'Suncorp',
            'logo': 'http://www.kingsleysoccerclub.com/images/suncorplogo.png'
        }
        sun_td.append(bank)

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
                        'days': '90',
                        'rate': curr_rate[1].string
                    }
                    bendigo_td.append(short)
                
                if '6 Months' == curr.string:
                    mid = {
                        'days': '180',
                        'rate': curr_rate[1].string
                    }
                    bendigo_td.append(mid)
                
                if '12 Months' == curr.string:
                    long_ = {
                        'days': '360',
                        'rate': curr_rate[1].string
                    }
                    bendigo_td.append(long_)

        bank = {
            'name': 'Bendigo',
            'logo': 'https://www.communities.bendigobank.com.au/__data/assets/image/0025/19816/BendigoBanklogo.png'
        }
        bendigo_td.append(bank)

        return bendigo_td
    
    
    def get_citi_td(self):
        url = 'https://www.citibank.com.au/term-deposit/?intcid=BN-Productpage-MidpageTD-RET'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'box blue_box'})
        rate = str(content.find('h2'))
        rate = rate.split('>')[1]
        rate = rate.split('<')[0].split()[0]
        
        citi_td = [{
            'days': '90',
            'rate': '0'
        },
        {
            'days': 180,
            'rate': rate
        },
        {
            'days': 360,
            'rate': '0'
        } ]

        bank = {
            'name': 'Citibank',
            'logo': 'http://www.ipepalau.com/wp-content/uploads/2011/01/Citibank-Thumbnail.png'
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
            msg = """\
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
        

        print 'fetching rates for UBank...'
        try:
            ubank_td = self.get_ubank_td()
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
            'bank': 'CBA',
            'logo': 'https://s0.yellowpages.com.au/1032b3ff-284c-4cae-a4a0-7f3678a7b017/commonwealth-bank-home-lending-solutions-highett-3190-logo.jpg',
            'notes': ''
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
            'bank': 'ANZ',
            'logo': 'https://pbs.twimg.com/profile_images/706597288299212800/xRvtFYma_400x400.jpg',
            'notes': ''
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
            'bank': 'Westpac',
            'logo': 'https://pbs.twimg.com/profile_images/695349302118391808/hC-wlVS6_400x400.jpg',
            'notes': ''
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
            'bank': 'NAB',
            'logo': 'https://pbs.twimg.com/profile_images/820753240648130561/tWPXUFde_reasonably_small.jpg',
            'notes': ''
        }
        nab_online.append(bank)
        
        return nab_online


    def get_stgeorge_online(self):        
        url = 'https://www.stgeorge.com.au/personal/bank-accounts/bank-account-interest-rates'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url)
        soup = bs4(browser.page_source, 'html.parser')
        rates = soup.find_all('tr')
        
    def collate_online_savers(self):
        
        #comm_online = self.get_comm_online()
        #anz_online = self.get_anz_online()
        #westpac_online = self.get_westpac_online()
        #nab_online = self.get_nab_online()
        
        
        return None


    
    """""""""""""""""""""""""""
        Goal Saver Scrapers

    """""""""""""""""""""""""""


    def get_comm_goal(self):
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

        comm_saver = [{
            'base': base_rate,
            'bonus': float(total_rate) - float(base_rate),
            'total': total_rate
        }]
        
        bank = {
            'name': 'CBA',
            'logo': 'http://i.utdstc.com/icons/120/commbank-android.png',
            'notes': ' '
        }
        comm_saver.append(bank)
         
        return comm_saver

