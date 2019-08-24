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


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        print("crawler_interpark - " + s + " is not english")
        return False
    else:
        print("crawler_interpark -  " + s + " is english")
        return True

def throw_up_unicode(character):
    unicode_escaped_letters = str(character.encode("raw_unicode_escape"))
    #print(unicode_escaped_letters)
    separated_list = unicode_escaped_letters.split('\\')
    #print(separated_list)
    semi_code_list = separated_list[2:]
    code_list =semi_code_list[::2]
    #print(code_list)

    query = ""

    for i in code_list:
        x = re.sub('[^a-zA-Z0-9]+', '', i)
        query+="%"+str(x.capitalize().swapcase())
        #print(query)

    #print("unicode escaped query is: " + query)
    return query

#returns list of {artist_name, title, url, startdate, enddate, crawleddate}
def interpark_ticket_finder(query,name_string_type):
    #find artist
    target_interpark_url="http://ticket.interpark.com/search/ticket.asp?search="+ query #This contains ticket URL


    # setup Driver|Chromeclose
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(r"C:\Users\pc\Desktop\chromedriver", chrome_options=options)
    driver.implicitly_wait(10) # waiting web source for three seconds implicitly

    #get interpark url
    driver.get(target_interpark_url)

    # get interpark poster image
    e= driver.find_element_by_id('ticketplay_result')
    poster_list = e.find_elements_by_tag_name('img')
    poster_url_list = []
    # print(poster_list)
    for i in range(len(poster_list)):
        url_item = poster_list[i].get_attribute('src')
        poster_url_list.append(url_item)
    # post_url_list contains png url for tickets
    poster_url_list = [s for s in poster_url_list if "Play" in s]

    # find url that includes play image
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #parsing
    active_ticket_information_soup = soup.find_all("div", {"class": "result_Ticket", "id": "ticketplay_result"}) #Not including titles but pretty
    #print(active_ticket_information_soup)
    #print(len(active_ticket_information_soup))
    title_href = active_ticket_information_soup[0]
    #print(title_href)
    h4_titles = title_href.find_all("h4")
    #print(h4_titles)
    date_soup_list= active_ticket_information_soup[0].find_all("td", {"class": "info_Date"}) #print(date_soup_list)

    b=[]
    for i in h4_titles:
        links = i.find_all('a')
        for link in links:
            # print(link)
            #making title and url dictionary
            url = link['href']
            b.append({'artist_name':name_string_type, "title":i.text, "url":url})
        for index_no in range(len(b)):
            #print(index_no)
            tag_and_date = date_soup_list[index_no] #print(tag_and_date)
            no_tag_date = tag_and_date.text #print(no_tag_date) #print(no_tag_date)
            sixteen_digit_date = re.sub('[^0-9]+', '', no_tag_date)
            length_string = len(sixteen_digit_date)
            first_length = round(length_string / 2)
            first_half = sixteen_digit_date[0:first_length]
            second_half = sixteen_digit_date[first_length:]
            starting_dt = datetime.strptime(first_half, "%Y%m%d")
            end_dt = datetime.strptime(second_half, "%Y%m%d") + timedelta(days=1)
            start_date = starting_dt.strftime("%Y-%m-%d")
            end_date = end_dt.strftime("%Y-%m-%d")
            b[index_no]['start_date'] = start_date
            b[index_no]['end_date'] = end_date
            #adding crawled date
            b[index_no]['crawled_date'] = today_str
            b[index_no]['poster_png']= poster_url_list[index_no]
        print('crawler_interpark - ' + str(b))
    driver.close()
    return b

#if sentence halts after isEnglish() returns specific value(True or False value).
#Therefore, evolved interpark ticket finder has to be made in order to continue interpark ticket finder

def evolved_interpark_ticket_finder(name_string_type):
    #if name is in korean, it has to be translated into query
    if not isEnglish(name_string_type):
        return interpark_ticket_finder(throw_up_unicode(name_string_type),name_string_type)
    #if name is in English, it can be just be used as query
    else:
        return interpark_ticket_finder(name_string_type,name_string_type)
