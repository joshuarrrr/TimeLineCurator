#!/usr/bin/env python

import sys, requests, bs4

# import os, errno, optparse

root = 'http://spectrum.ieee.org'
baseUrl = root + '/blog/riskfactor/page/'              # starting url
linkSelector = 'article > a'

sitemap = root + '/sitemap.xml'
sitemapFilter = 'riskfactor'

# outFile = 'rfcrawl.txt'
mode = 'crawl'
links = []


# def mkdir_p(path):
#     try:
#         os.makedirs(path)
#     except OSError as exc:  # Python >2.5
#         if exc.errno == errno.EEXIST and os.path.isdir(path):
#             pass
#         else:
#             raise

# mkdir_p('rfscrap')


def parseSitemap():
    res = requests.get(sitemap)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text)
    potentialLinks = soup.select('loc')

    for link in potentialLinks:
        if sitemapFilter in link.string:
            links.append(link.string)
            print link.string

    saveLinks('rfsitemap.txt')


def crawlHtml():
    page = 0
    while True:
        newLinks = []
        url = baseUrl + str(page)

        # Download the page.
        print('Downloading page %s...' % url)
        res = requests.get(url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text)

        # Find the URLs of the blog posts.
        newLinks = soup.select(linkSelector)
        print '%d links found' % len(newLinks)

        if newLinks == []:
            print 'Could not find links.'
        else:
            for link in newLinks:
                links.append(root + link.get('href'))

        print 'Total links: %d' % len(links)

        if len(newLinks) < 10:
            print 'end'
            print links
            break
        else:
            page += 1

    saveLinks('rfcrawl.txt')


def saveLinks(outFile):
    # Save the links to output file
    linksFile = open(outFile, 'w+')
    uniques = set(links)
    for item in uniques:
        print>>linksFile, item
    linksFile.close()

    print 'Done.'

# Compute location from command line arguments.
if len(sys.argv) > 1:
    mode = str(sys.argv[1])

if mode == 'sitemap':
    parseSitemap()
else:
    crawlHtml()
