# Python-News-Archive-Web-Scraping

Develop a news-database that is regularly updated where we can search and filter for certain
article.

Requirements:
• Crawl url: https://www.spiegel.de/international/
• Extract News-Entries from HTML (see image below)
o Title
o Sub-Title
o Abstract
o Download-time
• Store these entries in a suitable database
• The crawler should be triggered to run automatically every 15minutes
• During re-runs, existing entries should be detected and not stored as duplicates, but an additional
timestamp should be stored: update-time

Technologies:
• Python3
• BeautifulSoup
• MongoDB

How to run the script:
1. Run the main script news_archive.py which is scheduled to execute every 15 min.
  - Script scrapes all the news from the website and inserts into the mongo db as a document.
  - News archival is an update-insert process and update_time is updated for existing news.
2. Tested the code locally on local mongo db server instance but faced some issues connecting mongodb cluster.
3. Sample document data stored in mongo db is attached and the same has been shared on mail as a proof of screenshot.
4. Tried to run the process using docker but had some issues on my local docker engine.

Install scripts or dependencies:
1. pip3 install pymongo
2. pip3 install requests beautifulsoup4
3. pip3 install schedule
