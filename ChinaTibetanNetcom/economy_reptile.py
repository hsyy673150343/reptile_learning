from bs4 import BeautifulSoup
from ChinaTibetanNetcom.news_reptile import download_page, make_dir, information_category, get_pages_num, news_tibet_pull_page


if __name__ == '__main__':
    make_dir('/home/hs/藏文语料/经济')
    url_tibet = 'https://ti.tibet3.com/'
    economy_kinds_link = information_category(url_tibet)[5]
    html_text_economy = download_page(economy_kinds_link)
    soup_economy = BeautifulSoup(html_text_economy, 'html.parser')
    pull_right_4 = soup_economy.body.find_all('div', class_='pull-right more')
    for div in pull_right_4:
        economy_kinds_of = div.find('a').get('href')
        print(economy_kinds_of)
        economy_kinds_link = url_tibet + economy_kinds_of
        page_nums = get_pages_num(url_tibet, economy_kinds_of)
        category_pages = 'detail category link:%s, pages numbers:%d' % (economy_kinds_link, page_nums)
        print(category_pages)
        news_tibet_pull_page(url_tibet, economy_kinds_of, page_nums+1, 'economy', '经济')

