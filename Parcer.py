import requests
from bs4 import BeautifulSoup

link = "https://www.warandpeace.ru/ru/news/_/_/page=1/"

content = requests.get(link).text
soup = BeautifulSoup(content, 'lxml') # получение кода страницы

pages = soup.findAll("a", class_ = "menu_1") # получение числа страниц новостей
lastPage = "1"
prevTag = "0"
for tag in pages:
    if tag.text == ">":
        lastPage = prevTag # получение номера последней страницы
        break
    prevTag = tag.text

listName = list()
listTime = list()
listHref = list()
listArticles = list()

with open ("file.html", "w", encoding="utf-8") as file:
    for i in range(1, int(lastPage)+1):
        link = "https://www.warandpeace.ru/ru/news/_/_/page=" + str(i) + "/"
        content = requests.get(link).text
        soup = BeautifulSoup(content, 'lxml')
        block = soup.findAll("a", class_ = "a_header_article") # получение ссылок и названий статей
        date = soup.findAll("td", class_ = "topic_info_top") # получение времени публикации статьи
        for i in range(15):
            href = soup.find_all('a',  class_ = "a_header_article")[i].get('href') # получение ссылки на статью
            listHref.append(href) # запись ссылки на статью в список
        for tag in block:
            listName.append(tag.text) # запись названий статей в список
        for time in date:
            listTime.append(time.text) # запись времени публикации статьи в список

    for i in range(len(listHref)):
        linkArt = listHref[i]
        contentArt = requests.get(linkArt).text
        soupArt = BeautifulSoup(contentArt, 'lxml')  # получение кода страницы статьи
        blockArt = soupArt.findAll(class_="topic_text")  # получение текста статей
        for article in blockArt:
            listArticles.append(article.text) # запись текста статей в список

    for i in range(len(listName)):
        file.write(listName[i]) # запись названий статей в файл
        file.write("\n")
        file.write(listTime[i]) # запись даты публикации статьи в файл
        file.write("\n")
        file.write(listArticles[i]) # запись текста статьи в файл
        file.write("\n")
        file.write(listHref[i]) # запись ссылки на статью в файл
        file.write("\n")
        file.write("\n")
