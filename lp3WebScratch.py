import bs4, requests, re
import csv
# import unicodecsv as csv


def getBSObjHTML(url):
    res = requests.get(url)
    return bs4.BeautifulSoup(res.text, 'html.parser')


def findNextUrl(soup, base):
    selected = soup.select(".edition_score_navigation > div > .nav-next")
    tail = selected[0]['href']
    return base + tail


def currentChartInfo(soup):  # returns list with the number and the year of the chart
    numberRegex = re.compile("\d+")
    yearRegex = re.compile("\d\d\d\d")

    chartInfo = soup.select(".notowanie > div > h1 > strong")
    chartNo = int(numberRegex.findall(chartInfo[0].text)[0])
    year = int(yearRegex.findall(chartInfo[1].text)[0])

    return chartNo, year


def getStats(soup, highestPosition):
    def getPosition(entry):
        tags = entry.select(".lp3-position")  # tags with position: tags[0] - current position, tags[1] - change
        return int(tags[0].text)

    def getTitleAndArtist(entry):
        title = entry.select(".song_title > a")[0].text
        artist = entry.select(".song_performer > a")[0].text
        return title, artist

    result = []
    chart = soup.select(".notowanie > ol")[0]  # second one is the "outsiders" list, we don't want it
    listEntriesNodes = chart.select(".chart-list-place")

    position = i = 0  # default value
    while position <= highestPosition \
            and i < len(listEntriesNodes):  # position don't always line up with the number of elements (f.e. ex equo)

        entry = listEntriesNodes[i]

        position = getPosition(entry)
        title, artist = getTitleAndArtist(entry)
        points = highestPosition - position + 1  # for highestPosition == 30, points are computed exactly like on Trójka

        if position <= highestPosition:
            result.append((position, title, artist, points))  # double parenthesis for tuple
        i += 1

    return result


def saveToCSV(columnNames, results):
    with open('data.csv', 'w', newline='', encoding='UTF-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(columnNames)
        for record in results:
            csvwriter.writerow(record)


if __name__ == "__main__":
    baseUrl = "https://www.lp3.pl"
    currUrl = "https://www.lp3.pl/notowanie/1"
    lastUrl = "https://www.lp3.pl/the-end"

    columnNames = ("Nr notowania", "Rok notowania", "Pozycja", "Tytuł", "Artysta", "Punkty")
    resultTable = []  # table with all the tuples

    while currUrl != lastUrl:
        bs = getBSObjHTML(currUrl)  # beautifulSoup object
        chartNumber, chartYear = currentChartInfo(bs)  # information on the currently scrapped chart

        stats = getStats(bs, 30)
        for position, title, artist, points in stats:
            resultTable.append((chartNumber, chartYear, position, title, artist, points))

        print(f'Chart number {chartNumber} completed!')
        currUrl = findNextUrl(bs, baseUrl)

    saveToCSV(columnNames, results=resultTable)
