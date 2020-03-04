from bs4 import BeautifulSoup
from ChinaTibetanNetcom.news_reptile import download_page, make_dir, information_category, get_pages_num, news_tibet_pull_page


if __name__ == '__main__':
    make_dir('/home/hs/藏文语料/法律')
    url_tibet = 'https://ti.tibet3.com/'
    law_kinds_link = information_category(url_tibet)[4]
    html_text_law = download_page(law_kinds_link)
    soup_law = BeautifulSoup(html_text_law, 'html.parser')
    pull_right_4 = soup_law.body.find_all('div', class_='pull-right more')
    for div in pull_right_4:
        law_kinds_of = div.find('a').get('href')
        print(law_kinds_of)
        law_kinds_link = url_tibet + law_kinds_of
        page_nums = get_pages_num(url_tibet, law_kinds_of)
        category_pages = 'detail category link:%s, pages numbers:%d' % (law_kinds_link, page_nums)
        print(category_pages)
        news_tibet_pull_page(url_tibet, law_kinds_of, page_nums+1, 'law', '法律')

