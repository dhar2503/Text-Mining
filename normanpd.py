import urllib.request
import tempfile
import PyPDF2
import sqlite3
import nltk
import csv
import re
import textwrap
from nltk import sent_tokenize
from nltk import word_tokenize

url = ("http://normanpd.normanok.gov/filebrowser_download/657/2018-02-12%20Daily%20Arrest%20Summary.pdf")

def fetchincidents(url):
    urllib.request.urlretrieve(url, "C:\\TA\\Assignment 2\\normanpd\\arrest_record.pdf")

def extractincidents():

    # Read the PDF
    pdfReader = PyPDF2.PdfFileReader("C:\\TA\\Assignment 2\\normanpd\\arrest_record.pdf")
    pdfReader.getNumPages()

    # Get the first page
    page1 = pdfReader.getPage(0).extractText()

    clean_page = re.compile('(ce)\w+')
    final_page = clean_page.split(page1)
    clean_sent = re.compile('[;]')
    final_sent = clean_sent.split(final_page[2])
    clean_word = re.compile('[\n]')
    # final_words = clean_word.split(final_sent[11].replace(' \n', ' ').replace('-\n','-'))
    # print(len(final_words))
    incidents = []
    for row in range(0,12):

        final_words = clean_word.split(final_sent[row].replace(' \n',' ').replace('-\n','-'))
        incidents.append(final_words)
        # populatedb(final_words)
    return incidents

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except EnvironmentError as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except EnvironmentError as e:
        print(e)


def createdb():
    database = "C:\\sqllite\\normanpd.db"

    sql_create_arrests_table = """ CREATE TABLE arrests (
arrest_time TEXT,
case_number TEXT,
arrest_location TEXT,
offense TEXT,
arrestee_name TEXT,
arrestee_birthday TEXT,
arrestee_address TEXT,
status TEXT,
officer TEXT
); """

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_arrests_table)

    else:
        print("Error! cannot create the database connection.")


def create_arrests(conn, task):
    """
    Create a new arrest record
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO arrests(arrest_time,case_number,arrest_location,offense,arrestee_name,arrestee_birthday,arrestee_address,status,officer)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


def populatedb(incidents):
    database = "C:\\sqllite\\normanpd.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        for i in range(0,12):
            if len(incidents[i]) == 12:
                arrest_record = (incidents[i][1],incidents[i][2],incidents[i][3],incidents[i][4],incidents[i][5],incidents[i][6],incidents[i][7],
                incidents[i][10],incidents[i][11]);
                create_arrests(conn, arrest_record)
            else:
                arrest_record = (incidents[i][1], incidents[i][2], incidents[i][3], incidents[i][4], incidents[i][5], incidents[i][6], incidents[i][7],
                           incidents[i][11], incidents[i][12]);
                create_arrests(conn, arrest_record)

def status():
    database = "C:\\sqllite\\normanpd.db"
    conn = create_connection(database)
    if conn is not None:
        cur = conn.cursor()
        sql = ''' select count(*) from arrests '''

        Total_rows = cur.execute(sql)
        print("\n"+"Total number of rows in the database: "+str(Total_rows.fetchone()[0])+"\n")
        sql1 = ''' select * from arrests LIMIT 5 '''
        fetch_records = cur.execute(sql1)
        display_records = fetch_records.fetchall()
        for i in range(0,5):
            print(str(display_records[i]))

