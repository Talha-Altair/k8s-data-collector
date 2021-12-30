'''
Created on 
Course work: 
@author: 
Source:
    
'''
import requests
from bs4 import BeautifulSoup

def get_required_links(link):

    LINK = link

    url_text = requests.get(LINK).text
    soup = BeautifulSoup(url_text,'lxml') 

    all_links = []

    required_link_list = []

    all_content = soup.find_all ("div", class_ = "container-results large-images")

    for main_content in all_content:

        content = main_content.find_all("div", class_ = "clearfix")

        for data in content:

            href = data.find_all("a", class_ = "title") 

            page = str(href).split ('href="')[1].split('">\n')[0]


            all_links.append(f"https://www.kijiji.ca{page}")


    required_num_of_links = 10

    iter = 1

    for link in all_links:

        if required_num_of_links >= iter :

            required_link_list.append(link)

            iter += 1

    return required_link_list



def score_content(data):

    if data == 'Link Does Not Exist':
        return 0

    score = 10000

    # print(data['Kilometers'],type(data['Kilometers']))

    try:
        kilometers = int(str(data['Kilometers']).replace(',',''))
    except:
        return 0

    year = int(data['Year'])

    if kilometers > 150000:
        factor = (kilometers - 150000)/10 * 2
        score =  score - factor

    if year < 2017:
        factor = (2017 - year ) * 500
        score = score - factor
    
    return int(score)

def get_car_data(LINK):
    
    try:
        url_text = requests.get(LINK).text
    except:
        return "Link Does Not Exist"
    soup = BeautifulSoup(url_text,'lxml') 

    current_car_content = []
    all_content = soup.find_all ("div", id = "AttributeList")

    for ul_items in all_content:
        li_items = ul_items.find_all ("ul", class_ = "itemAttributeList-1090551278")

        for li_item in li_items:
            all_items = li_item.find_all ("li", class_ = "itemAttributeWrapper-37588635")

            for item in all_items[1:]:
                current_car_content.append(item.text)


    result = clean_content(current_car_content)

    return result

def clean_content(data):

    feature_list = [
                "Condition",
                "Year",
                "Make",
                "Model",
                "Trim",
                "Colour",
                "Body Type",
                "No of Seats",
                "Drivetrain",
                "Transmission",
                "Fuel Type",
                "Stock",
                "Kilometers"
            ]

    final_dict = {}

    for element in data:
        for feature in feature_list:
            if feature in element:
                a = element.split(feature)
                final_dict[feature] = a[1]

    return final_dict

def get_data(link):

    required_links = get_required_links(link)
    data = []
    count = 0

    for required_link in required_links:
        count += 1
        current_data = get_car_data(required_link)
        
        current_dict = {
            "Car_option" : count,
            "Link" : required_link,
            "Features" : current_data,
            "score" : score_content(current_data)
        }

        data.append(current_dict)

    return data

def startpy():
    data = get_data()

    print('data : ', data)

if __name__ == '__main__':
    startpy()