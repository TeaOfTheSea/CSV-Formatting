#!/usr/bin/env python


# imports
from dotenv import load_dotenv
from pathlib import Path
import shutil
import csv
import os


# init context vars
load_dotenv()

#get the act header
# with open(os.getenv('TGX_DROPBOX') + '/ACT_HeaderFile.csv') as headerFile:
#     headerContent = csv.reader(headerFile)
#     # https://stackoverflow.com/questions/26464567/csv-read-specific-row
#     header = [row for idx, row in enumerate(headerContent) if idx == 0][0]

header = Path(os.getenv('TGX_DROPBOX') + '/ACT_HeaderFile.csv').read_text().splitlines()[0]

with open(os.getenv('TGX_DROPBOX') + '/ACT_NewHeader.csv', 'w', newline='') as output:
    writer = csv.DictWriter(output, header, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    # get all the files in the act dropbox directory
    for file in os.listdir(os.getenv('TGX_DROPBOX') + '/ACTScores/'):
        # for all the files in that directory, check if they are csv's
        if file.endswith(".csv"):
            # open each csv
            with open(os.getenv('TGX_DROPBOX') + '/ACTScores/' + file) as csvFile:
                ACT = csv.reader(csvFile)
                # convert that data to an array for ease of iteration
                dataAsArray = list(ACT)
                # this grabs every i value for every row of the csv except 0, which is the header
                for i in (n + 1 for n in range(len(dataAsArray) - 1)):
                    # blank dictionary to be updated
                    rowToBeWritten = {}
                    # get indexes for all of the headers
                    for j in range(len(header)):
                        # for each header index,  update the main dictionary with the corresponding "header: column,header"
                        rowToBeWritten.update({header[j]: dataAsArray[i][j]})
                    # write that row to the csv file
                    writer.writerow(rowToBeWritten)


for file in os.listdir(os.getenv('TGX_DROPBOX') + '/ACTScores/'):
    if file.endswith(".csv"):
        shutil.move(str(os.getenv('TGX_DROPBOX') + '/ACTScores/' + file), str(os.getenv('ARCHIVE')))
