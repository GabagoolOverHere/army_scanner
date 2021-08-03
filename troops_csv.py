"""this script will fill your db with all the troops in the game sorted by name, faction, type, and tier. You'll have to delete a few rows first to make sure you have clean data.

thanks so much to Yasashii Hito for his amazing work!

more infos on https://forums.taleworlds.com/index.php?threads/all-276-unit-spreadsheet-with-all-information-armor-weapons-skills-etc-for-easy-sorting-and-comparison.411636/"""

import mysql.connector
import csv

conn = mysql.connector.connect(
    host='',
    user='',
    password='',
    database='',
    port=1234
)

fname = 'troops.csv'
file = open(fname, 'r')

try:
    reader = csv.reader(file)
    for row in reader:
        c = conn.cursor()
        d = (row[0], row[2], row[3], int(row[14]))
        c.execute(
            """INSERT INTO troops(name, faction, type, tier)
            VALUES (%s, %s, %s, %s)""", d)
        conn.commit()

finally:
    file.close()
    conn.close()
