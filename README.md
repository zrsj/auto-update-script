On completion, this project aims to perform an automatic update of CSV files containing ATO data.

This will be performed by a python script that will read in a list of SQL commands from a file
that will be used to retrieve tables of relevant information. These tables will then be exported
as the CSVs required. 

Additionally, this script should be run automatically at 7am every day to ensure that information
worked with in the CSV files is always up to date.

TODO:
  *Read in query.sql files and execute their body of contents
  *Output retrieved data as CSV files into data subdirectories
  *Have script auto-execute on a 7am everyday schedule
  *Connect direclty to database from the app within the code subdirectory 
