import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

def account(driver, num_em):
    driver.get('https://irkutsk.hh.ru/account/login?backurl=%2F')

    number = driver.find_element(By.XPATH, "//input[@placeholder='Email или телефон']")
    number.send_keys(num_em)

    next = driver.find_element(By.XPATH, "//button[@class='bloko-button bloko-button_kind-primary']")
    next.click()

    time.sleep(20)
    next1 = driver.find_element(By.XPATH, "//button[@class='bloko-button bloko-button_kind-primary']")
    next1.click()

    time.sleep(20)
    next2 = driver.find_element(By.XPATH, "//button[@class='bloko-button bloko-button_kind-primary bloko-button_stretched']")
    next2.click()

    time.sleep(3)

def link(driver, links, page, li):
    url = li + '&page=' + str(page)
    driver.get(url)

    it = driver.find_elements_by_class_name('vacancy-serp-item')
    for item in it:
        link = item.find_element(By.CLASS_NAME, 'bloko-link').get_attribute('href')
        links.append(link)

    print(links)

def info(driver, l, x):
    driver.get(l)

    x = []

    try:
        time.sleep(2)

        сontact = driver.find_element(By.XPATH, "//h2[@class='bloko-header-2']//button[@class='bloko-link bloko-link_pseudo']")
        сontact.click()

        name = driver.find_element(By.XPATH, "//div[@class='vacancy-contacts__body']//p//span").text
        number = driver.find_element(By.XPATH, "//p[@class='vacancy-contacts__phone-desktop']").text
        email = driver.find_element(By.XPATH, "//a[@data-qa='vacancy-contacts__email']").get_attribute('href').replace('mailto:', '')
    except:
        name = 'не указано'
        number = 'не указано'
        email = 'не указано'

    try:
        x.append({
            'title': driver.find_element(By.XPATH, "//h1[@class='bloko-header-1']//span").text,
            'price': driver.find_element(By.XPATH, "//span[@class='bloko-header-2 bloko-header-2_lite']").text,
            'company': driver.find_element(By.XPATH, "//span[@data-qa='bloko-header-2']//span").text,
            'address': driver.find_element(By.XPATH, "//div[@class='bloko-column bloko-column_xs-0 bloko-column_s-8 bloko-column_m-8 bloko-column_l-10']//a[@class='bloko-link bloko-link_disable-visited']//span[1]").text,
            'name': name,
            'number': number,
            'email': email,
            'link': l
        })

    except Exception:
        try:
            x.append({
                'title': driver.find_element(By.XPATH, "//h1[@class='bloko-header-1']//span").text,
                'price': driver.find_element(By.XPATH, "//span[@class='bloko-header-2 bloko-header-2_lite']").text,
                'company': driver.find_element(By.XPATH, "//span[@data-qa='bloko-header-2']//span").text,
                'address': driver.find_element(By.XPATH, "//div[@class='vacancy-company vacancy-company_with-logo']//p").text,
                'name': name,
                'number': number,
                'email': email,
                'link': l
            })

        except:
            try:
                x.append({
                    'title': driver.find_element(By.XPATH, "//h1[@class='bloko-header-1']//span").text,
                    'price': driver.find_element(By.XPATH, "//span[@class='bloko-header-2 bloko-header-2_lite']").text,
                    'company': driver.find_element(By.XPATH, "//span[@data-qa='bloko-header-2']//span").text,
                    'address': driver.find_element(By.XPATH, "//div[@class='bloko-column bloko-column_xs-0 bloko-column_s-8 bloko-column_m-8 bloko-column_l-10']//a[@class='bloko-link bloko-link_disable-visited']//span[1]").text,
                    'name': name,
                    'number': number,
                    'email': email,
                    'link': l
                })

            except:
                x.append({
                    'title': driver.find_element(By.XPATH, "//h1[@class='bloko-header-1']//span").text,
                    'price': driver.find_element(By.XPATH, "//span[@class='bloko-header-2 bloko-header-2_lite']").text,
                    'company': driver.find_element(By.XPATH, "//span[@data-qa='bloko-header-2']//span").text,
                    'address': driver.find_element(By.XPATH, "//div[@class='vacancy-company vacancy-company_with-logo']//p").text,
                    'name': name,
                    'number': number,
                    'email': email,
                    'link': l
                })

    print(x)
    return x

def save(x):
    with open('parser.csv', 'w', newline='') as ex:
        writer = csv.writer(ex, delimiter=';')
        writer.writerow(['вакансия', 'зарплата', 'компания', 'адрес', 'имя', 'номер', 'email', 'ссылка'])
        for dict in x:
            writer.writerow([dict['title'], dict['price'], dict['company'], dict['address'], dict['name'], dict['number'], dict['email'], dict['link']])

def parser():
    li = input('ссылка hh.ru: ')
    pages = input('сколько страниц: ')
    num_em = input('введите номер телефона или email: ')

    pag = int(pages)

    driver = webdriver.Chrome()

    account(driver, num_em)

    links = []
    for page in range(0, pag):
        link(driver, links, page, li)

    x = []
    for l in links:
        x.extend(info(driver, l, x))

    save(x)
    os.startfile('parser.csv')

    driver.close()

ready = input('пройдите проверку на робота сами, на это даётся 20 сек,\nвведите код который придёт, на это даётся 20 сек\nне нажимайте кнопку "потвердить" и "продолжить"\nесли готовы нажмите enter')
if ready == '':
    parser()