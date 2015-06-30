#! usr/bin/env Python3

import datetime
#import os
import requests
import smtplib
import sys
from bs4 import BeautifulSoup


# Set up email variables
email_user = 'you@yourdomain.com'
email_pwd = 'password'
FROM = 'you@yourdomain.com'
TO = ['youagain@yourdomain.com']
SUBJECT = 'Stuff from craigslist'
TEXT = ''


# Global link-prefix variable and empty list to store results
full_link = 'http://<your city here>.craigslist.org'
results = []
results_final = []


#-- WEB SCRAPER ACTION SECTION -------------------------------------------#


# The 'requests' library goes and gets the html data
# Search term: <make a note for later>
url = 'copy and paste url after making your search on Craigslist'
search_cl = requests.get(url)


# Now parse the requested html data with BeautifulSoup
soup = BeautifulSoup(search_cl.content)


# Loop through html, find all elements with the "hdrlnk" class, which are the posts
for link in soup.find_all(attrs={"class": "hdrlnk"}):
    # Consruct all the links to the posts themselves, append to results list
    results.append(full_link + '%s ; %s' %(link.get('href'), link.text))


# Open the text file in read+write mode, cursor at beginning of file (to check dupes)
link_file = open("C:\\Users\\<your_name>\\Desktop\\links.txt", "r+")


# Creates a list with lines as list elements, used to check for dupes with 'results' list
lines = link_file.read().splitlines()


# Loop through results and check items against file
for item in results:

    # If item not already in file, append to end, on new line
    # Also append to empty 'results_final' list, used to create email body
    if item not in lines:
        results_final.append(item)
        #os.SEEK_END
        link_file.seek(0,2)
        link_file.write(str(datetime.datetime.now()) + '\n\n')
        link_file.write(item + '\n')
        link_file.write('\n-----------------------------------------------------------------\n')

    # If the item is already in the file, move along
    elif item in lines:
        continue

    # In case some crazy thing happens and neither case is met
    else:
        #os.SEEK_END
        link_file.seek(0,2)
        link_file.write(str(datetime.datetime.now()) + '\n\n')
        link_file.write('Something went wrong. Check logs for the time given.' + '\n')
        link_file.write('\n-----------------------------------------------------------------\n')


# Close file when done
link_file.close()


#-- EMAIL THE RESULTS ---------------------------------------------------#


# Send email if there are new listings ('results' list is not empty)
if len(results_final) > 0:
    TEXT = results_final
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("your.mailservers.com", 587)
        # See here for details or if you prefer SSL: http://stackoverflow.com/a/12424439
        server.ehlo()
        server.starttls()
        server.login(email_user, email_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        sys.exit()
        
    except:
        # Mail failed, append info to end of log file
        log_file = open("C:\\Users\\<your_name>\\Desktop\\bs4_log.txt", "a+")
        log_file.write(str(datetime.datetime.now()) + '\n\n')
        log_file.write('Failed to send email' + '\n')
        log_file.write('\n-----------------------------------------------------------------\n')
        log_file.close()
        sys.exit()


else:
    sys.exit()
