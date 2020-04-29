#!/usr/bin/env python3

import functions
from pprint import pp
import sqlite3

print('************************************************************************')
print()
print('Clubfinder Utility Menu')
print()
print('************************************************************************')
print()
print("1. Export a new clubs.csv file from database")
print("2. Look for a link on a web page")
print("3. Interrogate a csv file of webpages for a link to a particular service")
print("4. Interrogate a database of webpages for a link to a particular service")
print("5. Parse an HTML file for domains")
# print("4. Count the occurrence of None! in a CSV from option 2")

option = input("Pick a Function: ")

if option == '1':
    functions.generateclubcsv()

elif option == '2':
    domain = input("Enter domain (Format: <example.com>): ")
    target = input("Enter a string to match against: ")
    functions.scrapeurl(domain, target)

elif option == '3':
    source = input("Enter input filename (Format: <file.csv>): ")
    outlist = input("Enter output filename (Format: <file.csv>): ")
    target = input("Enter a string to match against: ")

    with open(source) as f:
        for line in f:
            line = line.rstrip('\n')
            functions.writefile(outlist, 'a', (line, functions.scrapeurl(line, target)))

elif option == '4':
    db = input("Enter database name (Format: <name.sqlite>): ")
    target = input("Enter one or more comma separated services to match against: ")
    sourcedata = functions.dbread(db, 'SELECT clubid, cluburl FROM clubs WHERE cluburl IS NOT NULL')
    pp(sourcedata)
    for row in sourcedata:
        scrapedata = functions.scrapeurl(row[1], target)
        if scrapedata:
            print(row, scrapedata)
#            functions.dbwrite(db, f'UPDATE clubs SET {target} = {scrapedata} WHERE cluburl = {row[1]};')
            conn = sqlite3.connect(db)
            print(sqlite3.version)
            c = conn.cursor()
            c.execute(f"UPDATE clubs SET {target} = ? WHERE cluburl = ?", (scrapedata, row[1]))
            conn.commit()
            conn.close()

#        for phrase in target:
#            value = functions.searchsoup(scrapedata, phrase)
#            print(value)
#            functions.dbwrite('clubfinder_copy.sqlite', f'UPDATE clubs SET {value} WHERE cluburl = {i[1]}')

elif option == '5':
    html = input("Enter file (Format: <file.html>): ")

    with open("html") as fp:
        soup = BeautifulSoup(fp, features="html.parser")

    functions.htmlparser(soup)

'''elif option == '4':
    file = input("Enter file (Format: <file.csv>): ")

    with open(file) as fp:
        functions.count(file)
'''

