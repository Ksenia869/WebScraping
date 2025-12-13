import scrapy
from kinoafisha.items import FilmItem
import re

class KinoafishaSpider(scrapy.Spider):
    name = 'simple_kinoafisha'
    allowed_domains = ['kinoafisha.info']
    start_urls = ['https://www.kinoafisha.info/releases/']
    
    def parse(self, response):
        text = response.xpath('//text()').getall()
        
        films_data = []
        current_date = None
        current_film = {}
        
        for line in text:
            line = line.strip()
            if not line:
                continue

            if re.match(r'^\d{1,2}\s\w+\s\d{4}$', line):
                if current_film:
                    films_data.append(current_film)
                current_date = line
                current_film = {'release_date': current_date}
                continue

            if (len(line) > 2 and len(line) < 100 and 
                not re.search(r'\d{4}', line) and
                not any(word in line.lower() for word in ['приключения', 'комедия', 'драма', 'ужасы', 'боевик'])):
                
                if 'title' not in current_film:
                    current_film['title'] = line
                elif 'description' not in current_film and len(line) > 30:
                    current_film['description'] = line

            elif any(genre in line.lower() for genre in ['приключения', 'комедия', 'драма', 'ужасы', 'боевик', 'фэнтези', 'анимация']):
                current_film['genres'] = line

            elif re.search(r'\d{4},\s*\w+', line) or ('Россия' in line and re.search(r'\d{4}', line)):
                current_film['country_year'] = line

        if current_film:
            films_data.append(current_film)

        for film in films_data:
            if 'title' in film and 'release_date' in film:
                item = FilmItem()
                item.update(film)
                item['url'] = response.url
                yield item