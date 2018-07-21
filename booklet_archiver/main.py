
from pdfScraper import downloadRevenuePDFSForSingleManualSection
from CompareFiles import compareOldestTwoFilesTrees

def main():

    defaultSaveDir = "pdf/"
    downloadRevenuePDFSForSingleManualSection()

    # TODO Give rought comparison of PDF documents
    compareOldestTwoFilesTrees(defaultSaveDir)

if __name__ == "__main__":
    main()