#!/usr/bin/env python
import os, bs4, errno, csv, requests

from newspaper import Article

inFile = 'rfsitemap.txt'
outFile = 'rfscrap.csv'

urls = [line.rstrip('\n') for line in open(inFile)]

someUrls = urls[5:10]
pdfUrls = []

outputFile = open(outFile, 'w')
outputWriter = csv.writer(outputFile)

outputWriter.writerow(['url', 'title', 'text'])

for url in someUrls:

    if '.pdf' in url:
        pdfUrls.append(url)

    else:
        article = Article(url)
        article.download()
        article.parse()

        print(article.title)

        outputWriter.writerow([url, article.title.encode('utf-8'), article.text.encode('utf-8')])

for i, url in enumerate(pdfUrls):
    print "downloading with requests"
    r = requests.get(url)
    with open(str(i) + ".pdf", "wb") as pdf:
        pdf.write(r.content)
