from bs4 import BeautifulSoup
import requests
import os

# Download single section of Tax Duty manuals
def downloadRevenuePDFSForSingleManualSection():

    baseUrl = "https://www.revenue.ie"
    # TODO Remove hardcode page
    manualSection = "/en/tax-professionals/tdm/income-tax-capital-gains-tax-corporation-tax/index.aspx" 
    url = baseUrl + manualSection

    # Get page
    page = getSoupPage(url)

    allSections = getSections(page)

    # # TODO Remove - Used to shroten section for testing
    # aSections = {}
    # aSections[0] = allSections[1]
    # aSections[1] = allSections[2]

    for subSectionKey in allSections.keys():
        addDocumentsToSection(allSections[subSectionKey])

    print(allSections)

    for key in allSections.keys():
        downloadSectionPdfs(allSections[key])

def downloadSectionPdfs(section):

    baseUrl = "https://www.revenue.ie"
    sectionName = section["title"] + "=>" + section["name"]
    saveDirectory = "pdf/" + sectionName
    documents = section["documents"]

    for docKey in documents.keys():
        doc = documents[docKey]

        url = baseUrl + doc['pdfUrl']
        downloadPdf(url, doc["pdfId"], saveDirectory)

def addDocumentsToSection(pageDict):

    baseUrl = "https://www.revenue.ie"
    url = baseUrl + pageDict["pageUrl"]
    page = getSoupPage(baseUrl + pageDict["pageUrl"])

    documentsList = page.find("ul", {"class": "documents-list"})
    if documentsList != None:
        documentListItems = documentsList.find_all("li")
    else:
        pageDict["documents"] = {}
        return

    pdfLinks = {}
    count = 0
    for item in documentListItems:
        pdfTitle = item.find('span').string
        if item.find('a') == None:
            print("Could not find a link for section: ", pdfTitle)
            continue

        pdfUrl = item.find('a')['href']
        pdfId = item.find('a').string
        pdfLinks[count] = {"pdfUrl" : pdfUrl, "pdfId" : pdfId, "pdfTitle" : pdfTitle}
        count += 1

    pageDict["documents"] = pdfLinks

def getSections(rawPage):
    # Get list documents section
    sections = rawPage.find("div", {"class": "tdm-list-links"}).find_all("li")
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
    
    return subPages

def downloadPdf(url, pdfName, dirName="pdf/"):

    createDirectoryIfDoesNotExist(dirName)
    if dirName[-1] != "/":
        dirName += "/"

    chunkSize = 2000
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers, stream=True)

    fileName = dirName + pdfName + ".pdf"
    with open(fileName, 'wb') as fd:
        for chunk in r.iter_content(chunkSize):
            fd.write(chunk)

def createDirectoryIfDoesNotExist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def getSoupPage(url):
    # Mock chrome and get raw main page
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    print("Status code - ", r.status_code, "for page url: ", url)
    # Prase HTML
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
