#!/usr/bin/env python


# imports
import datetime as dt
# start = dt.datetime.now()
# from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv
from pathlib import Path
# import logging as log
# import pandas as pd
import shutil
import csv
import sys
import os


# init context vars
load_dotenv()
TESTING     = True
PROJ_NAME   = 'nrccua_aos'
PROJECT_DIR = Path(os.getenv('PROJECT_DIR'))
QUERIES_DIR = PROJECT_DIR / 'queries/prod'
DATA_DIR    = PROJECT_DIR / 'data'
date_stamp  = dt.datetime.today().strftime('%Y%m%d')


# init logging
#logging_filepath = PROJECT_DIR / 'logs/main'
#file_handler = TimedRotatingFileHandler(logging_filepath, when='midnight', encoding='utf-8', backupCount=7) 
#stdout_handler = log.StreamHandler(sys.stdout)
#log.basicConfig(
#    level=log.DEBUG,
#    format="[{asctime}] -- file:{filename:<15} -- fn:{funcName:<30} -- ln:{lineno:<4d} ->  {message}",
#    datefmt='%Y%m%d_%H:%M.%S',
#    style='{',
#    handlers=[file_handler, stdout_handler]
#    )
#log.getLogger(__name__)
#log.debug(F'exec started: {start}')


# CODE
#Take files in NRCCUA_AOS dropbox folder and put them in the main folder for informatica
informaticaFile = os.getenv('TGX_DROPBOX') + '/NRCCUA_AOS.csv'
with open(informaticaFile, 'w', newline='') as output:
    header = [
        'Data Source',	'Encoura ID',	'Student PIN',	'First Name',	'Middle Name',	'Last Name',	'Suffix',	'Address 1',	'Address 2',	'City',	'State Province',	'State Abbreviation',	'Zip Code',	'ZIP 4',	'Country',	'Country Code',	'Country Code Alpha',	'County Code',	'County Name',	'International Postal Code',	'Carrier Route',	'Check Digit',	'Delivery Point',	'Email',	'Home Phone Country Code',	'Home Phone',	'Mobile Phone Country Code',	'Mobile Phone',	'Birth Date',	'Gender',	'Race Ethnicity',	'Race Details',	'First Generation',	'GPA',	'Class Rank',	'Graduation Year',	'High School Code',	'High School MDR',	'High School Name',	'High School Type',	'College Type 1',	'College Type 2',	'College Type 3',	'College Type 4',	'Campus Environment',	'Specialized College 1',	'Specialized College 2',	'Specialized College 3',	'Denominational College 1',	'Denominational College 2',	'HS Course Track 1',	'HS Course Track 2',	'HS Course Track 3',	'HS Course Track 4',	'HS Course Track 5',	'HS Course Track 6',	'HS Course Track 7',	'HS Course Track 8',	'College Activity 1',	'College Activity 2',	'College Activity 3',	'College Activity 4',	'College Activity 5',	'College Activity 6',	'College Activity 7',	'College Activity 8',	'College Activity 9',	'College Activity 10',	'College Activity 11',	'College Activity 12',	'College Activity 13',	'College Activity 14',	'College Sport 1',	'College Sport 2',	'College Sport 3',	'College Sport 4',	'College Sport 5',	'College Sport 6',	'College Sport 7',	'College Sport 8',	'College Sport 9',	'College Sport 10',	'Academic Interest 1',	'Academic Interest 2',	'Academic Interest 3',	'Academic Interest 4',	'ACT Major Code 1',	'ACT Major Code 2',	'ACT Major Code 3',	'ACT Major Code 4',	'CIP Code 1',	'CIP Code 2',	'CIP Code 3',	'CIP Code 4',	'Career Interest 1',	'Career Interest 2',	'Career Interest 3',	'Enrollment Predictor',	'Mindset',	'AOS Inquiry',	'AOS Application',	'AOS Schedule Visit',	'Visited Campus',	'AOS Is Updated',	'Parent 1 First Name',	'Parent 1 Last Name',	'Parent 1 Email Address',	'Parent 2 First Name',	'Parent 2 Last Name',	'Parent 2 Email Address',	'Alumni Unique ID',	'Alumni Last Name',	'Alumni Primary Address',	'Alumni 5-digit ZIP code',	'Search Name',	'Order Number',	'Tag 1',	'Tag 2',	'Tag 3'
        ]
    writer = csv.DictWriter(output, header, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    
    for file in os.listdir(os.getenv('TGX_DROPBOX') + '/NRCCUA_AOS/'):
        # for all the files in that directory, check if they are csvs
        if file.endswith(".csv"):
            # importing the data from the file
            csvFile = open(os.getenv('TGX_DROPBOX') + '/NRCCUA_AOS/' + file)
            AOS = csv.reader(csvFile)
            for row in AOS:
                if row[0] == 'AOS': #this just filters out the headers
                    writer.writerow({
                        'Data Source': row[0],	
                        'Encoura ID': row[1],	
                        'Student PIN': row[2],	
                        'First Name': row[3],	
                        'Middle Name': row[4],	
                        'Last Name': row[5],	
                        'Suffix': row[6],	
                        'Address 1': row[7],	
                        'Address 2': row[8],	
                        'City': row[9],	
                        'State Province': row[10],	
                        'State Abbreviation': row[11],	
                        'Zip Code': row[12],	
                        'ZIP 4': row[13],	
                        'Country': row[14],	
                        'Country Code': row[15],	
                        'Country Code Alpha': row[16],	
                        'County Code': row[17],	
                        'County Name': row[18],	
                        'International Postal Code': row[19],	
                        'Carrier Route': row[20],	
                        'Check Digit': row[21],	
                        'Delivery Point': row[22],	
                        'Email': row[23],	
                        'Home Phone Country Code': row[24],	
                        'Home Phone': row[25],	
                        'Mobile Phone Country Code': row[26],	
                        'Mobile Phone': row[27],	
                        'Birth Date': row[28],	
                        'Gender': row[29],	
                        'Race Ethnicity': row[30],	
                        'Race Details': row[31],	
                        'First Generation': row[32],	
                        'GPA': row[33],	
                        'Class Rank': row[34],	
                        'Graduation Year': row[35],	
                        'High School Code': row[36],	
                        'High School MDR': row[37],	
                        'High School Name': row[38],	
                        'High School Type': row[39],	
                        'College Type 1': row[40],	
                        'College Type 2': row[41],	
                        'College Type 3': row[42],	
                        'College Type 4': row[43],	
                        'Campus Environment': row[44],	
                        'Specialized College 1': row[45],	
                        'Specialized College 2': row[46],	
                        'Specialized College 3': row[47],	
                        'Denominational College 1': row[48],	
                        'Denominational College 2': row[49],	
                        'HS Course Track 1': row[50],	
                        'HS Course Track 2': row[51],	
                        'HS Course Track 3': row[52],	
                        'HS Course Track 4': row[53],	
                        'HS Course Track 5': row[54],	
                        'HS Course Track 6': row[55],	
                        'HS Course Track 7': row[56],	
                        'HS Course Track 8': row[57],	
                        'College Activity 1': row[58],	
                        'College Activity 2': row[59],	
                        'College Activity 3': row[60],	
                        'College Activity 4': row[61],	
                        'College Activity 5': row[62],	
                        'College Activity 6': row[63],	
                        'College Activity 7': row[64],	
                        'College Activity 8': row[65],	
                        'College Activity 9': row[66],	
                        'College Activity 10': row[67],	
                        'College Activity 11': row[68],	
                        'College Activity 12': row[69],	
                        'College Activity 13': row[70],	
                        'College Activity 14': row[71],	
                        'College Sport 1': row[72],	
                        'College Sport 2': row[73],	
                        'College Sport 3': row[74],	
                        'College Sport 4': row[75],	
                        'College Sport 5': row[76],	
                        'College Sport 6': row[77],	
                        'College Sport 7': row[78],	
                        'College Sport 8': row[79],	
                        'College Sport 9': row[80],	
                        'College Sport 10': row[81],	
                        'Academic Interest 1': row[82],	
                        'Academic Interest 2': row[83],	
                        'Academic Interest 3': row[84],	
                        'Academic Interest 4': row[85],	
                        'ACT Major Code 1': row[86],	
                        'ACT Major Code 2': row[87],	
                        'ACT Major Code 3': row[88],	
                        'ACT Major Code 4': row[89],	
                        'CIP Code 1': row[90],	
                        'CIP Code 2': row[91],	
                        'CIP Code 3': row[92],	
                        'CIP Code 4': row[93],	
                        'Career Interest 1': row[94],	
                        'Career Interest 2': row[95],	
                        'Career Interest 3': row[96],	
                        'Enrollment Predictor': row[97],	
                        'Mindset': row[98],	
                        'AOS Inquiry': row[99],	
                        'AOS Application': row[100],	
                        'AOS Schedule Visit': row[101],	
                        'Visited Campus': row[102],	
                        'AOS Is Updated': row[103],	
                        'Parent 1 First Name': row[104],	
                        'Parent 1 Last Name': row[105],	
                        'Parent 1 Email Address': row[106],	
                        'Parent 2 First Name': row[107],	
                        'Parent 2 Last Name': row[108],	
                        'Parent 2 Email Address': row[109],	
                        'Alumni Unique ID': row[110],	
                        'Alumni Last Name': row[111],	
                        'Alumni Primary Address': row[112],	
                        'Alumni 5-digit ZIP code': row[113],	
                        'Search Name': row[114],	
                        'Order Number': row[115],	
                        'Tag 1': row[116],	
                        'Tag 2': row[117],	
                        'Tag 3': row[118]
                        })
            csvFile.close()

for file in os.listdir(os.getenv('TGX_DROPBOX') + '/NRCCUA_AOS/'):
    if file.endswith(".csv"):
        shutil.move(str(os.getenv('TGX_DROPBOX') + '/NRCCUA_AOS/' + file), str(os.getenv('ARCHIVE')))

# log.debug(F"exec time: {(dt.datetime.now() - start).total_seconds()} seconds")
