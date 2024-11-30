# web-crawler-riws

## Crawling with Scrapy

First, execute spiders to compile documents.

```
cd futgalCrawler/futgalCrawler
scrapy crawl fields_spider
scrapy crawl goalscorers_spider
```

This will generate two .json files: _fields_spider.json_ and _goalscorers_spider.json_.

## Elasticsearch

First, run ElasticSearch on your system.

Now, create index and introduce documents to Elasticsearch.

```
cd futgalCrawler/elasticSearch
python3 create_index.py
python3 insert_docs.py
```

This will have introduced all documents into Elasticsearch, making them avaliable for querying.

## Frontend

To deploy frontend, you will need to have a dependency installer such as yarn or npm

```
cd app-search-reference-ui-react-master
yarn install
yarn start
```
