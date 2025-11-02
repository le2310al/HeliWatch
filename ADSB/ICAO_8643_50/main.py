import csv
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import nodriver as nd
import os

keys = [
    'ICAO Code',
    'Classification',
    'Category',
    'Wing Span(m)',
    'Length(m)',
    'Height(m)',
    'MTOW(t)',
    'Fuel Capacity(ltr)',
    'Maximum Range(Nm)',
    'Persons On Board',
    'Take Off Distance(m)',
    'Landing Distance(m)',
    'Absolute Ceiling(x100ft)',
    'Optimum Ceiling(x100ft)',
    'Maximum Speed(kts / M)',
    'Optimum Speed(kts / M)',
    'Maximum Climb Rate(ft / min)',
    'List of Manufacturers',
]
icao = []

# I got a cloudflare error, despite robots.txt allowing webcrawling, so I saved the sitemap manually
def getSitemap():
    url = 'https://doc8643.com/static/sitemap.xml'
    r = requests.get(url)
    with open('.\output\sitemap.xml', 'wb') as f:
        f.write(r.content)

# Had to remove 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' from the root tag for it to parse
def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    endpoints = []

    for url in root.findall('url'):
        loc=url.find('loc').text
        if '/aircraft/' in loc:
            endpoints.append(loc)
    return endpoints

async def scrapeAircrafts(browser, endpoint):
    values = []
    data = {}
    tab = await browser.get(endpoint)
    await tab.sleep(3)
    await tab.get_content()
    code_class_cat = await tab.select_all("h1")
    for each in code_class_cat:
        values.append(each.text)
    tech = await tab.select_all(".tech-data")
    tech_values= await tech[0].query_selector_all(".pe-0")
    for each in tech_values:
        values.append(each.text)
    manufacturers = await tech[1].query_selector_all(".pe-1")
    temp = []
    for each in manufacturers:
        temp.append(each.text)
    values.append(temp)
    for each in values:
        data.update({keys[values.index(each)]: each})
    return [data]

async def main():
    #getSitemap()
    endpoints = parseXML('.\output\sitemap.xml')
    browser = await nd.start(headless=True)
    with open('output/icao.csv', 'w', newline='',  encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        index = 0
        for each in endpoints:
            writer.writerows(await scrapeAircrafts(browser, each))
            print(index)
            index += 1

if __name__ == "__main__":
    nd.loop().run_until_complete(main())
