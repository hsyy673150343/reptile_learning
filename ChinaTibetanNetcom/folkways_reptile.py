from bs4 import BeautifulSoup
from ChinaTibetanNetcom.news_reptile import download_page, make_dir, information_category, get_pages_num, news_tibet_pull_page

if __name__ == '__main__':
    make_dir('/home/hs/藏文语料/社会习俗')
    url_tibet = 'https://ti.tibet3.com/'
    folkways_kinds_link = information_category(url_tibet)[9]
    html_text_folkways = download_page(folkways_kinds_link)
    soup_folkways = BeautifulSoup(html_text_folkways, 'html.parser')
    pull_right_3 = soup_folkways.body.find_all('div', class_='pull-right more')
    for div in pull_right_3:
        folkways_kinds_of = div.find('a').get('href')
        print(folkways_kinds_of)
        folkways_kinds_link = url_tibet + folkways_kinds_of
        page_nums = get_pages_num(url_tibet, folkways_kinds_of)
        category_pages = 'detail category link:%s, pages numbers:%d' % (folkways_kinds_link, page_nums)
        print(category_pages)
        news_tibet_pull_page(url_tibet, folkways_kinds_of, page_nums + 1, 'folkways', '社会习俗')
