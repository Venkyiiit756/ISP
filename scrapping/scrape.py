#import the libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_number_of_days(row):
    #column can end with "gross" or some integer
    gross_col = [col for col in row.index if col.endswith('gross') ][0] 
    return gross_col 

#download the url
def download(url):
    return requests.get(url).text

#parse the html
def parse(html, i):
    soup = BeautifulSoup(html, 'html.parser')
    #extract the table
    #tables = soup.find('table')
    tables = soup.findAll('table', attrs={'border': '0', 'cellspacing': '0', 'width':'100%', 'cellpadding': '3'})

    df_list = []

    #iterate over the tables
    for table in tables:
        #get the the tag before table
        movie_name = table.previous_sibling.previous_sibling.text

        # read the HTML table from file
        html_table = pd.read_html(str(table))[0]

        #conver the table to dataframe with the first row as header
        html_table = pd.DataFrame(html_table.values[1:], columns=html_table.iloc[0])


        # add a column with the movie name
        html_table['Movie'] = movie_name

        #add new column "number of days" from column name which ends with "gross"
        temp_text = [col for col in html_table.columns if col.endswith('gross')][0]
        html_table['number of days'] = temp_text.split(' ')[0]

        #modify the "{number} days gross" column name to "gross"
        html_table = html_table.rename(columns={col: 'gross' for col in html_table.columns if col.endswith('gross')})

        #drop the column that contains string "Week"
        html_table = html_table.drop([col for col in html_table.columns if col.endswith('Collection')], axis=1)

        # display the DataFrame
        #print(html_table)


        #add dataframe into a list
        df_list.append(html_table)

    #iterate over the list of dataframes and combine them
    df_combined = pd.concat(df_list, ignore_index=True)


    # Show the combined data frame with the new "gross" column
    #print(df_combined)

    #write the dataframe to csv file
    df_combined.to_csv('collected_data.csv', index=False)



#call the functions
def scrape():
    #iterate over the pages
    for i in range(171, 172):
        html = download('https://web.archive.org/web/20041102084847/http://idlebrain.com:80/trade/collec/trade%d.html' % i)
        #print(html)
        parse(html, i)

#call the function
scrape()