#!/usr/bin/env python


# imports
from datetime import date,datetime
from unidecode import unidecode
from dotenv import load_dotenv
import shutil
import csv
import os
import re


#phonenumber formatting
def PhonenumberFormatting(phonenumber):
    #This regular expression is stolen from here https://stackoverflow.com/a/17337613
    numbersOnly = re.sub('[^0-9]','', phonenumber)
    if len(numbersOnly) == 7 or (len(numbersOnly) > 9 and len(numbersOnly) <13):
        return numbersOnly
    
#Gender formatting
def GenderFormatting(gender):
    if gender.upper() == "M" or gender.upper() == "F":
        return gender.upper()
    else: return "N"
    
def CeebDetermination(highschoolCeeb, collegeCeeb):
    if len(highschoolCeeb) != 0 and len(collegeCeeb) !=0: return collegeCeeb #Students who have both types of ceeb codes get the college ceeb
    elif len(collegeCeeb) !=0: return collegeCeeb # Students who only have a college ceeb get that one
    else: return highschoolCeeb #Students who only have a highschool ceeb get that one
    
#Just swapping vocabulary
def StudentTypeDetermination(studentType):
    if studentType.lower() == "high school student": return "New First Time"
    elif studentType.lower() == "transfer": return "Transfer"
    else: return "Non Degree Seeking Student"
    
def TermYearAssignment(collegeGradYear, highSchoolGradYear, transferEnrollmentDate, todaysDate, nextReasonableYear):
    if len(transferEnrollmentDate) != 0: #If they've declared a transfer enrollment date, check it to see if its valid and convert to term
        dateAsObject = datetime.strptime(transferEnrollmentDate, "%m/%d/%Y")
        if dateAsObject.year < nextReasonableYear: #if the desired year is unreasonable, set term and year to fall of next reasonable year
            return "Fall", nextReasonableYear
        elif dateAsObject.year == nextReasonableYear:
            if todaysDate.month < 8: #for these two options, the year the student wants to enroll is the current year, meaning we can only slot them for fall
                if dateAsObject.month <= 8: return "Fall", dateAsObject.year
                else: return "Spring", todaysDate.year + 1
            #For these options, we know the student wants to enroll next calendar year, so we can slot them in wherever
            elif dateAsObject.month > 1 and dateAsObject.month < 9:
                return "Fall", dateAsObject.year
            elif dateAsObject.month == 1:
                return "Spring", dateAsObject.year
            else:
                return "Spring", dateAsObject.year + 1 
        #options past here are always past the next reasonable year, so we can slot students in wherever
        elif dateAsObject.month > 1 and dateAsObject.month < 9:
            return "Fall", dateAsObject.year
        elif dateAsObject.month == 1:
            return "Spring", dateAsObject.year
        else:
            return "Spring", dateAsObject.year + 1
    elif len(collegeGradYear) != 0: #If we don't have a transfer enrollment date, assume they want to start the next fall semester after they graduate college
        if collegeGradYear > nextReasonableYear:
            return "Fall", collegeGradYear
        else: return "Fall", nextReasonableYear
    elif len(highSchoolGradYear) != 0 and highSchoolGradYear > nextReasonableYear: #If we don't have a college enrollment date, assume they want to start the next fall semester after they graduate high school
        return "Fall", highSchoolGradYear
    else: #If we don't have any data on when the student graduates, assume they want to start in the fall of the next reasonable year.
        return "Fall", nextReasonableYear
    
def CampusInquiryAssignment(preference):
    if preference.lower() == "online": return "Distance Learning"
    else: return "Main Campus"
        

def main():
    # init context vars
    load_dotenv()
    dropbox = os.getenv('TGX_DROPBOX')
    archives = os.getenv('TGX_ARCHIVES')
    storageDir = os.getenv('STORAGE_DIR')
    header = ["FirstName", "LastName", "Email", "Phone", "Gender", "Birthday", "Address", "City", "State", "Country", "Zip", "Ceeb", "StudentType", "AnticipatedStartTerm", "AnticipatedStartYear", "CampusInquiry"]
    
    #This is logic which is needed in a later loop a whole bunch, so we're just doing it once here to save processing time.
    todaysDate = date.today()
    if todaysDate.month > 7:
        nextReasonableYear = todaysDate.year + 1
    else:
        nextReasonableYear = todaysDate.year
    
    with open(dropbox + '/NicheFormattedDataFile.csv', 'w', newline='') as output:
        writer = csv.DictWriter(output, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
    
        # get all the files in the niche dropbox directory
        for file in os.listdir(dropbox + storageDir):
            # for all the files in that directory, check if they are csv's
            if file.endswith(".csv"):
                # open each csv
                with open(dropbox + storageDir + file) as csvFile:
                    # convert that data to an array for ease of iteration
                    dataAsArray = list(csv.reader(csvFile))
                    # this grabs every i value for every row of the csv except 0, which is the header
                    for i in (n + 1 for n in range(len(dataAsArray) - 1)):
                        if dataAsArray[i][35].lower() != "high school parent": #this is just so we don't write any data about high school parents.
                            startTerm, startYear = TermYearAssignment(dataAsArray[i][19], dataAsArray[i][27], dataAsArray[i][41], todaysDate, nextReasonableYear)#Start term and year are being handled with a lot of the same logic, so we define both at once instead of one by one.
                            writer.writerow({
                                "FirstName": unidecode(dataAsArray[i][4]),
                                "LastName": unidecode(dataAsArray[i][5]), 
                                "Email": dataAsArray[i][3], 
                                "Phone": PhonenumberFormatting(dataAsArray[i][6]), 
                                "Gender": GenderFormatting(dataAsArray[i][24]), 
                                "Birthday": dataAsArray[i][1], 
                                "Address": unidecode(str(dataAsArray[i][0] + " " + dataAsArray[i][14])), 
                                "City": unidecode(dataAsArray[i][2]), 
                                "State": unidecode(dataAsArray[i][7]), 
                                "Country": unidecode(dataAsArray[i][22]), 
                                "Zip": dataAsArray[i][8], 
                                "Ceeb": CeebDetermination(dataAsArray[i][25], dataAsArray[i][17]), 
                                "StudentType": StudentTypeDetermination(dataAsArray[i][35]), 
                                "AnticipatedStartTerm": startTerm, 
                                "AnticipatedStartYear": startYear, 
                                "CampusInquiry": CampusInquiryAssignment(dataAsArray[i][15])
                            })
                shutil.move(str(dropbox + storageDir + file), str(archives + storageDir))

if __name__ == '__main__': main()
