from bs4 import BeautifulSoup
from ChinaTibetanNetcom.news_reptile import download_page, make_dir, information_category, get_pages_num, news_tibet_pull_page


if __name__ == '__main__':
    make_dir('/home/hs/藏文语料/文化')
    url_tibet = 'https://ti.tibet3.com/'
    culture_kinds_link = information_category(url_tibet)[1]
    html_text_culture = download_page(culture_kinds_link)
    soup_culture = BeautifulSoup(html_text_culture, 'html.parser')
    pull_right_10 = soup_culture.body.find_all('div', class_='pull-right more')
    '''
    /culture/news/
    /culture/books/
    /culture/kaspa/
    /culture/gonde/
    /culture/philosophy/
    /culture/sungtsom/
    /culture/jesdus/
    /culture/gyunshes/
    /culture/srolgyun/
    /culture/dengrab/
    '''
    for div in pull_right_10:
        culture_kinds_of = div.find('a').get('href')
        culture_kinds_link = url_tibet + culture_kinds_of
        page_nums = get_pages_num(url_tibet, culture_kinds_of)
        category_pages = 'detail category link:%s, pages numbers:%d' % (culture_kinds_link, page_nums)
        print(category_pages)
        news_tibet_pull_page(url_tibet, culture_kinds_of, page_nums+1, 'culture', '文化')
