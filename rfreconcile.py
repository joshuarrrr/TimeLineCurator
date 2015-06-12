#!/usr/bin/env python
import os, bs4, errno

inFileScrap = 'rfcrawl.txt'
inFileSitemap = 'rfsitemap.txt'
outDir = 'rfscrap'

scraped = [line.rstrip('\n') for line in open(inFileScrap)]
sitemapped = [line.rstrip('\n') for line in open(inFileSitemap)]

scraped = sorted(scraped)
sitemapped = sorted(sitemapped)
duplicates = []

# print '%d unique scraped urls' % len(set(scraped))
# print '%d unique urls in sitemap' % len(set(sitemapped))

for url in scraped:
    if url in sitemapped:
        sitemapped.remove(url)


print '%d urls found in sitemap not in scrape' % len(sitemapped)

for url in sitemapped:
    if url in scraped:
        duplicates.append(url)
        sitemapped.remove(url)

print '%d of those were duplicates' % len(duplicates)

# # Save the duplicates to output file
# linksFile = open('rfdupes.txt', 'w+')
# for item in duplicates:
#     print>>linksFile, item
# linksFile.close()

# # Save the links to output file
# linksFile = open('rfnotlisted.txt', 'w+')
# for item in sitemapped:
#     print>>linksFile, item
# linksFile.close()
