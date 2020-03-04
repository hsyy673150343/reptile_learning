from bs4 import BeautifulSoup
from ChinaTibetanNetcom.news_reptile import download_page, make_dir, information_category, get_pages_num, news_tibet_pull_page


if __name__ == '__main__':
    make_dir('/home/hs/藏文语料/教育')
    url_tibet = 'https://ti.tibet3.com/'
    edu_kinds_link = information_category(url_tibet)[3]
    html_text_edu = download_page(edu_kinds_link)
    soup_edu = BeautifulSoup(html_text_edu, 'html.parser')
    pull_right_5 = soup_edu.body.find_all('div', class_='pull-right more')
    for div in pull_right_5:
        edu_kinds_of = div.find('a').get('href')
        print(edu_kinds_of)
        if edu_kinds_of != '/edu/online-course/':
            edu_kinds_link = url_tibet + edu_kinds_of
            page_nums = get_pages_num(url_tibet, edu_kinds_of)
            category_pages = 'detail category link:%s, pages numbers:%d' % (edu_kinds_link, page_nums)
            print(category_pages)
            news_tibet_pull_page(url_tibet, edu_kinds_of, page_nums+1, 'edu', '教育')
        else:
            continue
