#import the libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd



#download the url
def download(url):
    return requests.get(url).text


#parse the html
def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    #extract the table
    #tables = soup.find('table')
    tables = soup.findAll('table', attrs={'border': '0', 'cellspacing': '0', 'width':'100%', 'cellpadding': '3'})

    #iterate over the tables
    for table in tables:
        # read the HTML table from file
        html_table = pd.read_html(str(table))[0]
        # display the DataFrame
        print(html_table)



    



    

    
    
        
    
#call the functions
def scrape():
    html = download('https://web.archive.org/web/20041102084847/http://idlebrain.com:80/trade/collec/trade172.html')
    #print(html)
    parse(html)

#call the function
scrape()