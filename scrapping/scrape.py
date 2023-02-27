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
    status = requests.get(url).status_code
    if status == 200:
        return requests.get(url).text
    else:
        print("Error in downloading the url")
        return None

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

        #if a column exits
        if 'This Week Collection' in html_table.columns:
            #drop the column
            html_table = html_table.drop(['This Week Collection'], axis=1)

        # add a column with the movie name
        html_table['Movie'] = movie_name

        #add new column "number of days" from column name which ends with "gross"
        temp_text_list = [col for col in html_table.columns if col.endswith('gross') or col.endswith('share') or col.endswith('grossd') or ('days' in col)]

        if(temp_text_list == []):
            continue
        else:
            temp_text = temp_text_list[0]

        if(temp_text.endswith('share')):
            html_table = html_table.rename(columns={temp_text: 'share'})
        elif(temp_text.endswith('grossd')):
            html_table = html_table.rename(columns={temp_text: 'gross'})
        elif(temp_text.endswith('gross')):
            html_table = html_table.rename(columns={temp_text: 'gross'})
        elif('days' in temp_text):
            html_table = html_table.rename(columns={temp_text: 'gross'})
        else:
            html_table = html_table.rename(columns={temp_text: 'gross'})

        if(temp_text.endswith('share') or temp_text.endswith('grossd') or temp_text.endswith('gross')):
            html_table['number of days'] = temp_text.split(' ')[0]
        else:
            html_table['number of days'] = temp_text.split(' ')[2][1:3]

        #modify the "{number} days gross" column name to "gross"
        #html_table = html_table.rename(columns={col: 'gross' for col in html_table.columns if col.endswith('gross')})

        #drop the column that contains string "Week"
        #html_table = html_table.drop([col for col in html_table.columns if col.endswith('Collection')], axis=1)

        # display the DataFrame
        #print(html_table)


        #add dataframe into a list
        df_list.append(html_table)

    #iterate over the list of dataframes and combine them
    df_combined = pd.concat(df_list, ignore_index=True)


    # Show the combined data frame with the new "gross" column
    #print(df_combined)

    #write the dataframe to csv file
    #df_combined.to_csv('collected_data.csv', index=False)

    return df_combined



#call the functions
def scrape():

    df_list = []
    #iterate over the pages
    for i in range(150, 261):
        url = "https://web.archive.org/web/20041102084847/http://idlebrain.com:80/trade/collec/trade" + str(i) + ".html"
        print(url, "=============================\n\n\n")

        html = download(url)

        if (html == None):
            continue

        df = parse(html, i)
        df_list.append(df)
    
    #combine the dataframes if df_list not empty
    if (len(df_list) == 0):
        return

    df_combined = pd.concat(df_list, ignore_index=True)

    #write the dataframe to csv file
    df_combined.to_csv('collected_data.csv', index=False)
    

#call the function
scrape()

#https://web.archive.org/web/20070223101739/http://www.idlebrain.com/trade/collec/trade151.html