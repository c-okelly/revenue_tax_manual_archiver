from bs4 import BeautifulSoup
import requests

def main():

    print("Start of main")

    # Start page
    baseUrl = "https://www.revenue.ie"
    url = baseUrl + "/en/tax-professionals/tdm/income-tax-capital-gains-tax-corporation-tax/index.aspx"
    # Get page
    page = getSoupPage(url)

    # Get list documents section
    sections = page.find("div", {"class": "tdm-list-links"}).find_all("li")
    # Build subpages
    subPages = {}
    count = 0
    for i in sections:
        pageUrl = i.find('a')['href']
        title = i.find('a')['title']
        if (i.find('span') != None):
            name = i.find('span').string
        else:
            name = title

        subPages[count] = {"pageUrl" : pageUrl, "title" : title, "name" : name}
        count += 1


    # For each pages get pdf links
    firstFullPage = subPages[1]
    page = getSoupPage(baseUrl + firstFullPage["pageUrl"])
    sections = page.find("ul", {"class": "documents-list"}).find_all("li")

    pdfLinks = {}
    count = 0
    for i in sections:
        pdfUrl = i.find('a')['href']
        pdfId = i.find('a').string
        pdfTitle = i.find('span').string
        pdfLinks[count] = {"pdfUrl" : pdfUrl, "pdfId" : pdfId, "pdfTitle" : pdfTitle}
        count += 1

    print(pdfLinks)

    # Get sinlge pdf
    for i in pdfLinks.keys():
        currentPdfLink = pdfLinks[i]
        downloadPdf(baseUrl + currentPdfLink['pdfUrl'], currentPdfLink["pdfId"])

def downloadPdf(url, pdfName, dirName="pdfs/"):

    chunkSize = 2000
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers, stream=True)

    fileName = dirName + pdfName + ".pdf"
    with open(fileName, 'wb') as fd:
        for chunk in r.iter_content(chunkSize):
            fd.write(chunk)



def getSoupPage(url):
    # Mock chrome and get raw main page
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    print("Status code - ", r.status_code)
    # Prase HTML
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup



if __name__ == "__main__":
    main()