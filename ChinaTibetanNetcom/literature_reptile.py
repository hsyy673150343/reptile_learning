from bs4 import BeautifulSoup
from ChinaTibetanNetcom.news_reptile import download_page, make_dir, information_category, get_pages_num, news_tibet_pull_page


if __name__ == '__main__':
    make_dir('/home/hs/藏文语料/文学')
    url_tibet = 'https://ti.tibet3.com/'
    literature_kinds_link = information_category(url_tibet)[2]
    html_text_literature = download_page(literature_kinds_link)
    soup_literature = BeautifulSoup(html_text_literature, 'html.parser')
    pull_right_10 = soup_literature.body.find_all('div', class_='pull-right more')
    '''
    /literature/news/
    /literature/fiction/
    /literature/poem/
    /literature/prose/
    /literature/translation/
    /literature/treatise/
    /literature/special/--->里面还有9个分类
    '''
    cnt = 0
    for div in pull_right_10:
        literature_kinds_of = div.find('a').get('href')
        # print(literature_kinds_of)
        if literature_kinds_of == '/literature/special/':
            literature_kinds_link = url_tibet + literature_kinds_of
            html_literature_tibet = download_page(literature_kinds_link)
            soup_literature_tibet = BeautifulSoup(html_literature_tibet, 'html.parser')
            pull_right_9 = soup_literature_tibet.body.find_all('div', class_='pull-right more')
            for pull_right_9_div in pull_right_9:
                special_kinds_of = pull_right_9_div.find('a').get('href')
                special_kinds_of_link = url_tibet + special_kinds_of
                page_nums = get_pages_num(url_tibet, special_kinds_of)
                category_pages = 'detail category link:%s, pages numbers:%d' % (special_kinds_of_link, page_nums)
                print(category_pages)
                news_tibet_pull_page(url_tibet, special_kinds_of, page_nums + 1, 'literature', '文学')
        else:
            literature_kinds_link = url_tibet + literature_kinds_of
            page_nums = get_pages_num(url_tibet, literature_kinds_of)
            category_pages = 'detail category link:%s, pages numbers:%d' % (literature_kinds_link, page_nums)
            print(category_pages)
            news_tibet_pull_page(url_tibet, literature_kinds_of, page_nums + 1, 'literature', '文学')
        
