from bs4 import BeautifulSoup
from ChinaTibetanNetcom.news_reptile import download_page, make_dir, information_category, get_pages_num, news_tibet_pull_page

if __name__ == '__main__':
    make_dir('/home/hs/藏文语料/格萨尔')
    url_tibet = 'https://ti.tibet3.com/'
    gesar_kinds_link = information_category(url_tibet)[8]
    html_text_gesar = download_page(gesar_kinds_link)
    soup_gesar = BeautifulSoup(html_text_gesar, 'html.parser')
    pull_right_4 = soup_gesar.body.find_all('div', class_='pull-right more')
    for div in pull_right_4:
        gesar_kinds_of = div.find('a').get('href')
        print(gesar_kinds_of)
        gesar_kinds_link = url_tibet + gesar_kinds_of
        page_nums = get_pages_num(url_tibet, gesar_kinds_of)
        category_pages = 'detail category link:%s, pages numbers:%d' % (gesar_kinds_link, page_nums)
        print(category_pages)
        news_tibet_pull_page(url_tibet, gesar_kinds_of, page_nums + 1, 'gesar', '格萨尔')
