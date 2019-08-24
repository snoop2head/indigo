from selenium import webdriver
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta

#today's date
today_int = date.today()
today_str = str(today_int)

#time right now
now_int = datetime.now()
now_str = str(now_int)



def artist(name):
    #webdriver option without showing chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(r"C:\Users\pc\Desktop\chromedriver", chrome_options=options)
    driver.implicitly_wait(10) # waiting web source for three seconds implicitly

    # get melon url
    artist_url = "https://www.melon.com/search/total/index.htm?q="+str(name)+"&section=&linkOrText=T&ipath=srch_form"
    driver.get(artist_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #parsing information
    #artist_info = soup.find_all('div',{'class':{'info_01'}})
    #artist_info_specific = artist_info.find_all("a", {'class':{'atistname'}})
    #print(artist_info)
    #print(artist_info_specific)
    artist_number = soup.find('input',{'name':{'artistId'}})['value']
    #print(artist_number)
    driver.close()
    return artist_number

#returns list of {artist_name, title, url, startdate, enddate, crawleddate}
def melon_ticket_finder(artist_number,name_string_type):
    #find artist
    artist_id=str(artist_number) #yerin baek's artist number 698776, ADOY's artist number 1704627
    melon_ticket_url="https://ticket.melon.com/artist/index.htm?artistId="+artist_id
    #artist_name="ADOY"
    #melon_ticket_url_2="https://ticket.melon.com/search/index.htm?q="+artist_name+"#"

    #setup driver|chrome

    #webdriver option without showing chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(r"C:\Users\pc\Desktop\chromedriver", chrome_options=options)
    driver.implicitly_wait(10) # waiting web source for three seconds implicitly

    # get melon url
    driver.get(melon_ticket_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # get melon ticket image
    e_list= driver.find_elements_by_class_name('show_infor')
    poster_url_list = []
    for i in e_list:
        poster = i.find_element_by_tag_name('img')
        # print(poster_list)
        url_item = poster.get_attribute('src')
        poster_url_list.append(url_item)
        # poster_url_list = [s for s in poster_url_list if "Play" in s]
    # post_url_list contains png url for tickets
    # print(poster_url_list)

    #parsing information
    all_text_notices = soup.find_all('div',{'class':{'show_infor'}})
    urls_and_titles = soup.find_all('span',{'class':{'show_title'}})
    on_sale=soup.find_all('span',{'class':{'ico_list ico_list4'}})
    all_date_list = soup.find_all('td',{'class':'show_date'}) #print(all_date_list)

    #{title:url} database for tickets)
    a =[]

    for i in urls_and_titles:
        links = i.find_all('a')
        #limiting the length of list smaller than plays available
        if len(a) < len(on_sale):
            for link in links:
                #formating url
                url='https://ticket.melon.com/'+link['href']
                a.append({'artist_name':name_string_type,'title':i.text, "url":url})
                #print(a)
        else:
            break

    for index_no in range(len(a)):
        #print(index_no)
        tag_and_date = all_date_list[index_no] #print(tag_and_date)
        no_tag_date = tag_and_date.text #print(no_tag_date) #print(no_tag_date)
        sixteen_digit_date = re.sub('[^0-9]+', '', no_tag_date)
        length_string = len(sixteen_digit_date)
        first_length = round(length_string / 2)
        first_half = sixteen_digit_date[0:first_length]
        second_half = sixteen_digit_date[first_length:]
        starting_dt = datetime.strptime(first_half, "%Y%m%d")
        end_dt = datetime.strptime(second_half, "%Y%m%d") + timedelta(days=1)
        #print(end_dt)
        start_date = starting_dt.strftime("%Y-%m-%d")
        end_date = end_dt.strftime("%Y-%m-%d")
        a[index_no]['start_date'] = start_date
        a[index_no]['end_date'] = end_date
        #adding crawled date
        a[index_no]['crawled_date'] = today_str
        a[index_no]['poster_png'] = poster_url_list[index_no]

    print(a)
    driver.close()
    return a

def evolved_melon_ticket_finder(name_string_type):
    artist_number= artist(name_string_type)
    return melon_ticket_finder(artist_number,name_string_type)

def from_sixteen_digit_to_make_start_date_end_date(sixteen_digit_date):
    length_string = len(sixteen_digit_date)
    first_length = round(length_string / 2)
    first_half = sixteen_digit_date[0:first_length]
    second_half = sixteen_digit_date[first_length:]
    starting_dt = datetime.strptime(first_half, "%Y%m%d")
    end_dt = datetime.strptime(second_half, "%Y%m%d")
    start_date = starting_dt.strftime("%Y-%m-%d")
    end_date = end_dt.strftime("%Y-%m-%d")
    return start_date, end_date

