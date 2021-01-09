import bs4, requests, re


def getBSObjHTML(url):
    res = requests.get(url)
    return bs4.BeautifulSoup(res.text, 'html.parser')

def findNextUrl(soup, base):
    selected = soup.select(".edition_score_navigation > div > .nav-next")
    tail = selected[0]['href']
    return base + tail

def currentChartInfo(soup):  #returns list with the number and the year of the chart
    numberRegex = re.compile("\d+")
    yearRegex = re.compile("\d\d\d\d")

    chartInfo = bs.select(".notowanie > div > h1 > strong")
    chartNo = int(numberRegex.findall(chartInfo[0].text)[0])
    year = int(yearRegex.findall(chartInfo[1].text)[0])

    return [chartNo, year]

def getStats(soup, chartNo, year, numberOfRecords):
    pass

baseUrl = "https://www.lp3.pl"
currUrl = "https://www.lp3.pl/notowanie/1"
lastUrl = "https://www.lp3.pl/the-end"

while currUrl != lastUrl:
    bs = getBSObjHTML(currUrl)
    chartInfo = currentChartInfo(bs)
    print(chartInfo[0])

    currUrl = findNextUrl(bs, baseUrl)
