#This code expects that:
    #you have installed the python module unidecode
    #it is looking for csv files in a folder in the same directory as it, called To_Import
    #and that there is a folder called Output for it to place the output file in

#the files being imported do not need to follow any specific naming scheme, as long as they are csvs in the To_Import folder
#if multiple csvs are in the To_Import, it will combine them into one file


#most of the research for this is being done from here https://docs.python.org/3/library/csv.html
#this code was written to address ticket https://jira.texastech.edu/browse/TAO-1896

import csv
from datetime import date
import unidecode #I'm calling unidecode.unidecode() from this module to clean the first and last names. The implementation is guided by this stack overflow answer https://stackoverflow.com/a/2633310
import os

#this block of code chooses what year is the most reasonable minimum year for a student to have as their entry year
todays_date = date.today()
if todays_date.month >7:
    nextReasonableYear = todays_date.year+1
else:
    nextReasonableYear = todays_date.year

with open('.\Output\generalImportTemplateUsNews.csv', 'w', newline='') as generalImportTemplate: #I'm not exactly sure how the with here opens the file, but whatever it's doing handles exceptions and closes the file for me
    header = ['First Name', 'Middle name', 'Last Name', 'Birthdate', 'Email', 'Mobile Phone', 'Home Phone', 'Mailing Address', 'Address2', 'City', 'State', 'Zip', 'Country', 'Gender', 'Hispanic', 'Ethnicity', 'CEEB', 'student_type', 'student_stage', 'academic_interest', 'anticipated_major', 'Anticipated_Entry_term', 'Entry_year', 'event_code', 'interaction_id', 'source',	'lead_source', 'last_data_input_source', 'RecordType']
    writer = csv.DictWriter(generalImportTemplate, header)
    writer.writeheader()

    for filename in os.listdir('.\To_Import'): #this looks for a folder in the same folder as this code called To_Import
        if filename.endswith(".csv"): #for all the files in that directory, check if they are csvs
            USnews = csv.reader(open('.\To_Import\\'+filename)) #importing the data from the file
            for row in USnews:
                if row[5] == "student": #the US news import gives us data on students, parents, and other. We only want the data on students.
                
                    #this is just to make sure that we don't put enrollment years in that don't make any sense
                    try:
                        if int(row[7])>nextReasonableYear:
                            entryYear=int(row[7])
                        else:
                            entryYear=nextReasonableYear
                    except:
                        entryYear=nextReasonableYear #some intended enrollment fields were left blank, which caused errors. This catches those errors.
                
                    writer.writerow({
                        'First Name': unidecode.unidecode(row[4]), #row 4 of the US news import is the first name
                        #'Middle name', 
                        'Last Name': unidecode.unidecode(row[3]),
                        'Birthdate': row[6],
                        'Email': row[2],
                        #'Mobile Phone',
                        #'Home Phone', 
                        #'Mailing Address', 
                        #'Address2', 
                        #'City', 
                        #'State', 
                        #'Zip', 
                        #'Country', 
                        #'Gender', 
                        #'Hispanic', 
                        #'Ethnicity', 
                        #'CEEB', 
                        'student_type': 'New First Time', 
                        'student_stage': 'Inquiry', 
                        #'academic_interest', 
                        #'anticipated_major', 
                        'Anticipated_Entry_term': 'Fall', 
                        'Entry_year': entryYear, 
                        #'event_code', 
                        #'interaction_id', 
                        'source': 'Ref_USNews',
                        'lead_source': 'Ref_USNews',
                        'last_data_input_source': 'Referral: US News', 
                        #'RecordType'
                        })
