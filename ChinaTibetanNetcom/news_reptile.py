import requests
from bs4 import BeautifulSoup
from lxml import etree
import os


def make_dir(path):
    if not os.path.exists('/home/hs/藏文语料'):
        os.mkdir('/home/hs/藏文语料')
    if not os.path.exists(path):
        os.mkdir(path)


def download_page(url):
    headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"}
    try:
        req = requests.get(url, headers)
        req.encoding = 'utf-8'
        req_text = req.text
        return req_text
    except requests.exceptions.ConnectionError:
        requests.status_codes = 'Connection refused'


def get_class_list(class_html):
    soup = BeautifulSoup(class_html, 'html.parser')
    class_list = soup.body.find_all('ul', class_='nav navbar-nav')
    class_ = []
    for ul in class_list:
        ul_li = ul.find_all('li')
        for li in ul_li:
            a_tag = li.find('a')
            link = a_tag.get('href')
            class_.append(link)
    return class_


cnt = 0


def entry_content(tag, original_url, category, create_file_category):
    temp = ''
    global cnt
    for i in tag:
        '''进入每一条新闻的链接'''
        content_link = original_url + i.get('href')
        content_link_split = content_link[:-5].split('/')
        # print(content_link_split)
        '''过滤无关网页'''
        if category in content_link:
            if content_link != temp:
                cnt += 1
                print(content_link)
                print(cnt)
                # 不加try前运行到43526.html的时候出错
                try:
                    content_html_text = download_page(content_link)
                    html_content_soup = BeautifulSoup(content_html_text, 'html.parser')
                    news_entry_content = html_content_soup.find('div', class_='entry-content')
                    entry_content_p = news_entry_content.find_all('p')
                    # print(entry_content_p)
                    # print(type(entry_content_p[0]))
                except Exception as e:
                    print(e)
                else:
                    for p_inner in entry_content_p:
                        file_name = ('/home/hs/藏文语料/%s/%s' % (create_file_category, '_'.join(content_link_split[4:]))) + '.txt'
                        with open(file_name, 'a+', encoding='utf-8') as f:
                            f.write(p_inner.text + '\n')
            else:
                # print('这一条新闻与上一条相同,舍弃～！不保存！！')
                continue
            temp = content_link
        else:
            continue


def page_1(original_url, detail_category_info, category, create_file_category):
    detail_category_info_link = original_url + detail_category_info
    print(detail_category_info_link)
    html_text_1 = download_page(detail_category_info_link)
    html = etree.HTML(html_text_1)

    a_tag_1 = html.xpath("//div[@class='posts col-md-8 col-xs-12']/ul/li//a")
    entry_content(a_tag_1, original_url, category, create_file_category)


def page_1_to_end(original_url, detail_category_info, page_index, category, create_file_category):
    detail_category_info_link = original_url + detail_category_info + page_index
    print(detail_category_info_link)
    html_text_1_to_end = download_page(detail_category_info_link)
    html = etree.HTML(html_text_1_to_end)
    a_tag_1_to_end = html.xpath("//div[@class='posts col-md-8 col-xs-12']/ul/li//a")
    entry_content(a_tag_1_to_end, original_url,category, create_file_category)


def news_tibet_pull_page(original_url, detail_category_info, pages_num, category, create_file_category):
    page_1(original_url, detail_category_info, category, create_file_category)
    for page in range(2, pages_num):
        index = 'index_%d.html' % page
        page_1_to_end(original_url, detail_category_info, index, category, create_file_category)


def get_pages_num(original_url, detail_category):
    inner_link = original_url + detail_category
    page_information = download_page(inner_link)
    page_html = etree.HTML((page_information))
    pagination = page_html.xpath("//ul[@class='pagination']/li/a")
    # print(type(pagination)) # list
    if pagination:  # 两页或者两页以上才有翻页的属性
        # print(pagination[-1])
        last_page_text = pagination[-1].text
        if last_page_text == 'མཇུག་ངོས།':  # 最后一页(两页或者两页以上才有'མཇུག་ངོས།'这个属性)
            last_page_link = pagination[-1].get('href')
            page_num = last_page_link[:-5].split('/' or '_')[-1].split('_')[-1]
            return int(page_num)
    else:
        page_num = 1
        return page_num


def news(original_url):
    news_link = information_category(original_url)[0]
    html_text_news = download_page(news_link)
    # print(html_text_news)
    soup_news = BeautifulSoup(html_text_news, 'html.parser')
    pull_right_3 = soup_news.body.find_all('div', class_='pull-right more')
    # print(pull_right_3)
    for div_pull_right_3 in pull_right_3:
        '''/news/tibet/ /news/china/ /news/international/'''
        region = div_pull_right_3.find('a').get('href')
        if region == '/news/tibet/':
            news_tibet_link = original_url + region
            html_news_tibet = download_page(news_tibet_link)
            soup_news_tibet = BeautifulSoup(html_news_tibet, 'html.parser')
            pull_right_5 = soup_news_tibet.body.find_all('div', class_='pull-right more')
            for div_pull_right_5 in pull_right_5:
                '''/news/tibet/xz qh sc gs yn 西藏 青海 四川 甘肃 云南'''
                # 藏族分布区域
                detail_category_info = div_pull_right_5.find('a').get('href')
                detail_category_link = original_url + detail_category_info
                page_nums = get_pages_num(original_url, detail_category_info)
                category_pages = 'detail category link:%s, pages numbers:%d' % (detail_category_link, page_nums)
                print(category_pages)
                news_tibet_pull_page(original_url, detail_category_info, page_nums + 1, 'news', '新闻')
        else:
            detail_category_link = original_url + region
            page_nums = get_pages_num(original_url, region)
            category_pages = 'detail category link:%s, pages numbers:%d' % (detail_category_link, page_nums)
            print(category_pages)
            news_tibet_pull_page(original_url, region, page_nums + 1, 'news', '新闻')


def information_category(url):
    category_link_list = []
    html_text = download_page(url)
    for i in get_class_list(html_text):
        if i != '/video/':
            category_link = url + i
            category_link_list.append(category_link)
    '''news culture literature edu law economy tour general gesar(格萨尔) folkways（社会习俗）'''
    return category_link_list[:-3]


if __name__ == '__main__':
    url_tibet = 'https://ti.tibet3.com/'
    '''新闻 /news/'''
    make_dir('/home/hs/藏文语料/新闻')
    news(url_tibet)

