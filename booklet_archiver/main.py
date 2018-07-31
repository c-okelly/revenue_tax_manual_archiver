
from pdfScraper import downloadRevenuePDFSForSingleManualSection
from CompareFiles import compareOldestTwoFilesTrees

def main():

    print("Running download section.\n")
    defaultSaveDir = "pdf/"
    downloadRevenuePDFSForSingleManualSection()

    # TODO Give rought comparison of PDF documents
    print("Running comparison.\n")
    compareOldestTwoFilesTrees(defaultSaveDir)

if __name__ == "__main__":
    main()