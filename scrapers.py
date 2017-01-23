from bs4 import BeautifulSoup as bs
import requests

class WebScrapers(object):
    

    def get_soup(self, url):
        request = requests.get(url)
        soup = bs(request.text, 'html.parser')

        return soup


    def get_commbank_td(self):
        url = 'https://www.commbank.com.au/personal/accounts/term-deposits/rates-fees.html'
        soup = self.get_soup(url)
        content = soup.find('div', {'class': 'column full-col'})
        
        links = content.find_all('tr')
        for link in links:
            
            string = link.find('p').string
            if '3' in string:
                if '6' not in string:
                    string = string.split('m', 1)[0]
                    days_90 = link.find('div', {'class': 'path52 tablecell'})
                    print string
                    print days_90.find('p').string 

            if '7' in string:
                if '36' not in string:
                    string = string.split('m', 1)[0]
                    days_210 = link.find('div', {'class': 'path42 tablecell'})
                    print string
                    print days_210.find('p').string
                
            if '12' in string:
                string = string.split('m', 1)[0]
                days_360 = link.find('div', {'class': 'path32 tablecell'})
                print string
                print days_360.find('p').string

            print '\n' 
        return None


    def get_
