from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import time
import pandas as pd


ID = "id"
NAME = "name"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"

# BEAUTIFUL SOUP
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def get_homes():
    # Gets all links of homes
    all_link_elements = soup.find_all("a", class_="link-overlay")

    # Turns into List
    for x in all_link_elements:
        href = x["href"]
        if "http" not in href:
            all_links.append(f"https://mlstoronto.searchrealty.co/{href}")
        else:
            all_links.append(href)




def get_address():

    # Gets all of the adresses
    all_address = soup.find_all(class_='property-address')

    num = 1

    # Goes into a list
    for address in all_address:

        # We need to append every other object since the class "property-address" included the address and the square footage
        num += 1
        if num % 2 == 0:
            ok = str(address.get_text())

            # Get's rid of \n at the beginning of every address object while also getting rid of white space at the end of address
            real_address = ok[2:].strip()
            list_address.append(real_address)

            #get's postal code to split addresses into areas



            #checks to see if the data is in the proper format, if it isn't, the data will be removed from the set
            split_address = real_address.split(", ")
            if len(split_address) == 3:
                postal_code = split_address[2]
                split_postal_code = postal_code.split(" ")

                if len(split_postal_code) == 3:
                    partial_postal_code = split_postal_code[1]
                    list_postal_codes.append(partial_postal_code)
                else:
                    list_address.pop(num - 2)
                    list_price.pop(num - 2)
                    all_links.pop(num - 2)
            else:
                list_address.pop(num - 2)
                list_price.pop(num - 2)
                all_links.pop(num - 2)












def get_price():
    # Get all prices of homes

    all_price = soup.find_all(class_="property-price")

    #puts all the prices into a sorted list
    for x in all_price:
        list_price.append(x.text)

    #cleans the data
    for n in range(len(list_price)):
        price = list_price[n]

        # sees if the rent of a building includes other words
        # ie($2950 + 2 bathrooms)
        x = price.split()



        # gets rid of the extra words to only include the price of unit)
        if len(x) > 1:
            price = x[0]




            if len(price) == 6:
                # gets rid of $ sign in price
                price = price[1:]
                # get rid of comma
                price = price[0:1] + price[2:]



            # this is used for rental prices where the price is over $10,000. Since there is an extra digit between $1,000 and $10,000, we have to split the string in a different place
            elif len(price) == 7:
                # gets rid of $ sign in price
                price = price[1:]
                #gets rid of comma
                price = int(price[0:2] + price[3:])

            #takes out the old value and inputs the new value
            list_price.pop(n)
            list_price.insert(n, price)








baths = input("What number of baths do you want: ")
beds = input("What number of beds do you want: ")
lower_bound = input('What is the lowest price in monthly rent you would like to see: ')
upper_bound = input('What is the highest price in monthly rent you would like to see: ')


WEBSITE = f"https://mlstoronto.searchrealty.co/search?sortby=latest&acl_city=Toronto%2C+ON&minbeds={beds}&maxbeds={beds}&minbaths={baths}&maxbaths={baths}&haslat=1&haslong=1&page=1&type=grid&listingtype=Rental"

chrome_driver_path = "C:\Chrome Driver\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(WEBSITE)
soup = BeautifulSoup(driver.page_source, 'html.parser')



# Gets the total number of pages in website
num_of_page = soup.find_all(class_="pagination-item")
list_pages = []
for x in num_of_page:
    page = x.get_text()
    if not page == "":
        list_pages.append(page)
num_pages = list_pages[len(list_pages) - 1]

all_links = []
list_address = []
list_price = []
list_postal_codes = []




#web scraping

for x in range(int(num_pages)):
    page = x + 1
    NEW_WEBSITE = f"https://mlstoronto.searchrealty.co/search?sortby=latest&acl_city=Toronto%2C+ON&minbeds={beds}&maxbeds={beds}&minbaths={baths}&maxbaths={baths}&haslat=1&haslong=1&page={page}&type=grid&listingtype=Rental"



    driver.get(NEW_WEBSITE)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    get_price()
    get_homes()
    get_address()






data_dict = {
    "prices": list_price,
    "address": list_address,
    "links": all_links,
    "area": list_postal_codes
}
data = pd.DataFrame(data_dict)



sorted_df = data.sort_values(by=['prices']).reset_index(drop=True).drop(df.columns[0], axis=1)


#finding the minimum index in the dataframe that can fit within the given interval
for x in range(0, len(sorted_df.index)):
    if sorted_df['prices'][x] >= lower_bound:
        low_index = x
        print(low_index)
        break

#finding the maximumindex in the dataframe that can fit within the given interval
for x in reversed(range(len(sorted_df.index))):
    if sorted_df['prices'][x] <= upper_bound:
        upper_index = x
        print(upper_index)
        break

#cuts the dataframe based on the given index values found
new_df = sorted_df.iloc[low_index:upper_index, :]


#turns dataframe into csv file
new_df.to_csv("real_estate_data.csv")





