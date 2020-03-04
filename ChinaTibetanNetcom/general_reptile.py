from bs4 import BeautifulSoup
from ChinaTibetanNetcom.news_reptile import download_page, make_dir, information_category, get_pages_num, news_tibet_pull_page


if __name__ == '__main__':
    make_dir('/home/hs/藏文语料/通识')
    url_tibet = 'https://ti.tibet3.com/'
    general_kinds_link = information_category(url_tibet)[7]
    html_text_general = download_page(general_kinds_link)
    soup_general = BeautifulSoup(html_text_general, 'html.parser')
    pull_right_5 = soup_general.body.find_all('div', class_='pull-right more')
    for div in pull_right_5:
        general_kinds_of = div.find('a').get('href')
        print(general_kinds_of)
        general_kinds_link = url_tibet + general_kinds_of
        page_nums = get_pages_num(url_tibet, general_kinds_of)
        category_pages = 'detail category link:%s, pages numbers:%d' % (general_kinds_link, page_nums)
        print(category_pages)
        news_tibet_pull_page(url_tibet, general_kinds_of, page_nums+1, 'general', '通识')
