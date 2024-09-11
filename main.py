# Нужно парсить страницу со свежими статьями (https://habr.com/ru/all/) и выбирать те статьи, 
# в которых встречается хотя бы одно из ключевых слов. 
# Эти слова определяем в начале скрипта. 
# Поиск вести по всей доступной preview-информации, т. е. по информации, доступной с текущей страницы. 
# Выведите в консоль список подходящих статей в формате: <дата> – <заголовок> – <ссылка>.
import requests
import bs4

def get_url()->str:
    return 'https://habr.com/ru/all/'

def parce(key_word:str, pages:int = 10)->bool:
    url = get_url()
    for n in range(pages):
        page = f'page{n+1}/'
        response = requests.get(url+page)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.text, features='lxml')
            articles = soup.findAll('div', class_='tm-article-snippet tm-article-snippet')
            for article in articles:
                time = article.find('time')['title']
                sub_article = article.find('a', class_ = 'tm-title__link')
                title_url = sub_article['href']
                title_text = sub_article.find('span').text
                hubs_article = article.findAll('span', class_ = 'tm-publication-hub__link-container')
                exist = False
                for hub in hubs_article:
                    sub_title = hub.find('span').text
                    if key_word in sub_title.lower():
                        exist = True
                text = article.find('div', class_ = 'article-formatted-body article-formatted-body article-formatted-body_version-1').text
                if (key_word in title_text.lower() or 
                    exist or 
                    key_word in text.lower()):

                    print(f'{time}-{title_text}-{title_url}')
            return True
        else:
            print('Connection failed')
            return False
    

def main():
    ## Определяем список ключевых слов:
    KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'видео']
    for word in KEYWORDS:
        print('')
        parce(word, 50)

if __name__ == '__main__':
    main()