#!/usr/bin/env python

# This code expects that:
    # you have installed the python module unidecode
    # it is looking for csv files in a folder in the same directory as it, called To_Import
    # and that there is a folder called Output for it to place the output file in
# the files being imported do not need to follow any specific naming scheme, as long as they are csvs in the To_Import folder
# if multiple csvs are in the To_Import, it will combine them into one file
# most of the research for this is being done from here https://docs.python.org/3/library/csv.html
# this code was written to address ticket https://jira.texastech.edu/browse/TAO-1896

import csv
import os
from datetime import date
# I'm calling unidecode.unidecode() from this module to clean the first and last names. 
# The implementation is guided by this stack overflow answer https://stackoverflow.com/a/2633310
import unidecode
import shutil

# this block of code chooses what year is the most reasonable 
# minimum year for a student to have as their entry year
todaysDate = date.today()
if todaysDate.month > 7:
    nextReasonableYear = todaysDate.year + 1
else:
    nextReasonableYear = todaysDate.year


fileName = 'c:/Informatica/TargetX/dropbox/General_import/generalImportTemplateUsNews' + str(todaysDate.month) + '-' + str(todaysDate.day) + '-' + str(todaysDate.year) + '.csv' #makes a unique filename which will avoid files overwriting one another when moved to the archive
with open(fileName, 'w', newline='') as generalImportTemplate:
    header = [
        'first_name', 'middle_name', 'last_name', 'birthdate', 'email',
        'mobile_phone', 'home_phone', 'mailing_address', 'address2',
        'city', 'state', 'zip', 'country', 'gender', 'hispanic',
        'ethnicity', 'ceeb', 'student_type', 'student_stage',
        'academic_interest', 'anticipated_major', 'anticipated_entry_term',
        'entry_year', 'event_code', 'interaction_id', 'source',	'lead_source',
        'last_data_input_source', 'record_type'
        ]
    # --> I also added the quote all argument for writer objects. This will help you 
    # keep your sanity when some really dirty data comes thru and Informatica
    # decides for you (without asking) to interpret it in the most unintuitive way!
    writer = csv.DictWriter(generalImportTemplate, header, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    # this looks for a folder in the same folder as this code called To_Import
    for file in os.listdir('c:/Informatica/TargetX/dropbox/US_News'):
        # for all the files in that directory, check if they are csvs
        if file.endswith(".csv"):
            # importing the data from the file
            with open('c:/Informatica/TargetX/dropbox/US_News/' + file) as csvFile:
                USnews = csv.reader(csvFile)
                for row in USnews:
                    # the US news import gives us data on students, 
                    # parents, and other. We only want the data on students.
                    if row[5] == "student":
                        # this is just to make sure that we don't put 
                        # enrollment years in that don't make any sense
                        try:
                            if int(row[7]) > nextReasonableYear:
                                entryYear = int(row[7])
                            else:
                                entryYear = nextReasonableYear
                        except:
                            # some intended enrollment fields were left blank,
                            # which caused errors. This catches those errors.
                            entryYear = nextReasonableYear
                    
                        writer.writerow({
                            # row 4 of the US news import is the first name
                            'first_name': unidecode.unidecode(row[4]),
                            #'middle_name', 
                            'last_name': unidecode.unidecode(row[3]),
                            'birthdate': row[6],
                            'email': row[2],
                            #'mobile_phone',
                            #'home_phone', 
                            #'mailing_address', 
                            #'address2', 
                            #'city', 
                            #'state', 
                            #'zip', 
                            #'country', 
                            #'gender', 
                            #'hispanic', 
                            #'ethnicity', 
                            #'ceeb', 
                            'student_type': 'New First Time', 
                            'student_stage': 'Inquiry', 
                            #'academic_interest', 
                            #'anticipated_major', 
                            'anticipated_entry_term': 'Fall', 
                            'entry_year': entryYear, 
                            #'event_code', 
                            #'interaction_id', 
                            'source': 'Ref_USNews',
                            'lead_source': 'Ref_USNews',
                            'last_data_input_source': 'Referral: US News', 
                            #'record_type'
                            })
            shutil.move(str('c:/Informatica/TargetX/dropbox/US_News/' + file), str('c:/Informatica/TargetX/archives/US_News/'))
