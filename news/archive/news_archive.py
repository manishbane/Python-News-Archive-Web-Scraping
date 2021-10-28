import requests
from bs4 import BeautifulSoup
from news.archive.config import NEWS_ARCHIVE_ATTRS
import datetime
import pymongo
from pymongo import UpdateOne
import schedule
import time

class NewsArchive(object):

    def __init__(self, newsUrl="https://www.spiegel.de/international/"):
        """
        :param newsUrl: URL of the news website to scrape the data
        """
        markup = requests.get(newsUrl).text
        self.soup = BeautifulSoup(markup, 'html.parser')

    def news_archive_data(self, category):
        """
        Common function to web scrape news website and extract data for archival
        :param category:
        :return:
        """
        news_archive_data = []

        # Crawl International news URL and extract news entries
        titleSpans = self.soup.findAll('span',
                                       attrs={'class': NEWS_ARCHIVE_ATTRS[category]['title_span_class_attrs']})
        subTitleSpans = self.soup.findAll('span', attrs={
            'class': NEWS_ARCHIVE_ATTRS[category]['sub_title_span_class_attrs']})
        abstractSpans = self.soup.findAll('span', attrs={
            'class': NEWS_ARCHIVE_ATTRS[category]['abstract_span_class_attrs']})

        for title, sub_title, abstract in zip(self.extractTextFromSpans(titleSpans),
                                              self.extractTextFromSpans(subTitleSpans),
                                              self.extractTextFromSpans(abstractSpans)):
            news_archive = {}
            news_archive['title'] = title
            news_archive['sub_title'] = sub_title
            news_archive['abstract'] = abstract
            news_archive['download_time'] = datetime.datetime.now()
            news_archive_data.append(news_archive)

        return news_archive_data

    def extractTextFromSpans(self, spans):
        """
        Extract news text from the html span tag
        :param spans:
        :return:
        """
        textData = []

        for span in spans:
            news_data = self.cleanNewsText(span.text)
            textData.append(news_data)

        return textData

    def getNewsTabLinksToScrapeData(self):
        """
        Get the various news tabs available on the website such as World, Europe, Germany etc. to extract all the other news as well
        :return:
        """
        newsTabLinks = []

        for i in self.soup.find_all('li', {'class': 'swiper-slide mr-24 flex-shrink-0'}):
            link = i.find('a', href=True)
            if link is None:
                continue
            if link.get('href') != 'https://www.spiegel.de/international/':
                newsTabLinks.append(link.get('href'))

        return newsTabLinks

    def cleanNewsText(self, newsText):
        newsText = str(newsText)
        newsText = newsText.rstrip()
        newsText = newsText.replace('\n','')
        return newsText

def main():
    #Create news archive to get international news
    news_archive = NewsArchive()
    international_news = news_archive.news_archive_data("International")

    # Create news archive to get other countries news such as World, Europe, Gernamy etc.
    newsTabLinks = news_archive.getNewsTabLinksToScrapeData()
    othersNews = []
    for newsTabLink in newsTabLinks:
        otherNewsArchive = NewsArchive(newsTabLink)
        othersNews.extend(otherNewsArchive.news_archive_data("Others"))

    final_news_archive = international_news + othersNews

    #Create local mongodb client and insert/update news data
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.db.news_archive
    try:
        title = [data.pop("title") for data in final_news_archive]
        operations=[UpdateOne({"title":title}, {'$set': {"update_time": datetime.datetime.now()}, '$setOnInsert': data}, upsert=True) for title ,data in zip(title,final_news_archive)]

        db.bulk_write(operations)
        print(f'Successfully Inserted/Updated News Archiv: {len(final_news_archive)}')
    except Exception as e:
        print('An error occurred news archives were not stored to db: %s' % e)

#Scheduler to run this news archival process every 15 min

schedule.every(15).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
