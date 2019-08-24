from crawler_interpark_ticket import evolved_interpark_ticket_finder
from crawler_melon_ticket import evolved_melon_ticket_finder

def concert_ticket_data_list_crawler(string_input):
    #evolved interpark ticket finder returns list of ticket data
    # data format is {artist_name, title, url, start_date, end_date, crawled_date}
    ticket_data_interpark_list = evolved_interpark_ticket_finder(string_input)

    #evolved melon ticket finder returns list of ticket data
    # data format is {artist_name, title, url, start_date, end_date, crawled_date}
    ticket_data_melon_list = evolved_melon_ticket_finder(string_input)

    #two lists are combined
    concert_ticket_data_list = ticket_data_interpark_list + ticket_data_melon_list
    print("combined crawler - this is combined " + str(concert_ticket_data_list))

    no_of_avail_concerts = len(concert_ticket_data_list)
    str_no_of_avail_concerts = str(no_of_avail_concerts)
    print("combined crawler - there are total " + str_no_of_avail_concerts + " items of concerts available right now")

    #How do I make two return values?
    #Like {list : [], no_of_concerts: 6}?

    return concert_ticket_data_list
