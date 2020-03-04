from bs4 import BeautifulSoup
from ChinaTibetanNetcom.news_reptile import download_page, make_dir, information_category, get_pages_num, news_tibet_pull_page


if __name__ == '__main__':
    make_dir('/home/hs/藏文语料/旅游')
    url_tibet = 'https://ti.tibet3.com/'
    tour_kinds_link = information_category(url_tibet)[6]
    html_text_tour = download_page(tour_kinds_link)
    soup_tour = BeautifulSoup(html_text_tour, 'html.parser')
    pull_right_3 = soup_tour.body.find_all('div', class_='pull-right more')
    for div in pull_right_3:
        tour_kinds_of = div.find('a').get('href')
        print(tour_kinds_of)
        tour_kinds_link = url_tibet + tour_kinds_of
        page_nums = get_pages_num(url_tibet, tour_kinds_of)
        category_pages = 'detail category link:%s, pages numbers:%d' % (tour_kinds_link, page_nums)
        print(category_pages)
        news_tibet_pull_page(url_tibet, tour_kinds_of, page_nums+1, 'tour', '旅游')