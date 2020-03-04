from selenium import webdriver
import time
import os


if not os.path.exists('/home/hs/藏文语料'):
    os.mkdir('/home/hs/藏文语料')

driver = webdriver.Chrome()
driver.get('https://ti.tibet3.com/')
time.sleep(3)

def pull_page_one_stage(a_tag_xpath):
    a_tag = driver.find_element_by_xpath(a_tag_xpath)
    a_link = a_tag.get_attribute('href')
    print(a_link)
    driver.get(a_link)


def next_page_1(page_li_url):
    print(page_li_url)
    driver.get(page_li_url)
    ul = driver.find_elements_by_xpath("//div[@class='posts col-md-8 col-xs-12']/ul")
    ul_length = len(ul)
    print(ul_length)  # 5
    li = driver.find_elements_by_xpath("//div[@class='posts col-md-8 col-xs-12']/ul/li")
    print(len(li)) # 25
    op_file = open('/home/hs/藏文语料/news.txt', 'a+', encoding='utf-8')
    for i in li:
        op_file.write(i.find_element_by_class_name('text').text + '\n')
    op_file.close()
    page_li_a = driver.find_elements_by_xpath("//nav[@class='pagination-wrap']/ul/li/a")
    if page_li_a[-1].text in ['363','358','61','37','34']:
        driver.get("https://ti.tibet3.com/news/tibet/")
        return
    else:
        pass
    for j in page_li_a:
        if j.text =='འོག་ངོས།': # 下一页
            page_li_url = j.get_attribute('href')
        else:
            continue
    '''下一页'''
    next_page_1(page_li_url)


def pull_page_two_stage(a_tag_xpath):
    a_tag = driver.find_element_by_xpath(a_tag_xpath)
    a_link = a_tag.get_attribute('href')
    print(a_link)
    next_page_1(a_link)

if __name__ == '__main__':
    links = driver.find_elements_by_xpath('/html/body/div[1]/nav/div[1]/div[2]/ul/li/a')
    length = len(links)
    '''news culture literature edu law economy tour general gesar(格萨尔) folkways（社会习俗）'''
    for i in range(0, length-3):
        links = driver.find_elements_by_xpath('/html/body/div[1]/nav/div[1]/div[2]/ul/li/a')
        link = links[i]
        url = link.get_attribute('href')
        print(url)
        driver.get(url)
        time.sleep(1)
        class_breadcrumb = driver.find_element_by_class_name('breadcrumb')
        class_ = class_breadcrumb.find_element_by_xpath('//a[2]')
        # print(class_.text)
        if class_.text is not 'བརྙན་ཟློས།':# 不爬取video类
            if class_.text == 'གསར་འགྱུར།':# 新闻类
                '''a_tag_1,2,3'''
                pull_page_one_stage("//div[@class='col-md-8']/div[1]/div[1]/a")

                '''a_tag_1_1,2,3,4,5'''
                pull_page_two_stage("//div[@class='col-md-8']/div[1]/div[1]/a")
                pull_page_two_stage("//div[@class='col-md-8']/div[2]/div[1]/a")
                pull_page_two_stage("//div[@class='col-md-8']/div[3]/div[1]/a")
                pull_page_two_stage("//div[@class='col-md-8']/div[4]/div[1]/a")
                pull_page_two_stage("//div[@class='col-md-8']/div[5]/div[1]/a")

            break




