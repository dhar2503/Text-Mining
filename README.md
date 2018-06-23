# Text-Mining
Main code take one parameter, a url for the pdf document to download and parse.
The function extractincidents() takes no parameters and it reads data from the pdf files and extracts the incidents.
The createdb() function creates an SQLite database file named normanpd.db and inserts a table.
The function populatedb(incidents) function takes the rows created in the extractincidents() 
function and adds it to the normanpd.db database
The status() function prints to standard out, first, the total number of rows in the database
