# 1. ABOUT THE PROGRAM

CSVLoader is designed for the convenience of exporting and importing csv files to the Oracle database.
This tool is a set of commands, executable and configuration files that are a wrapper over SQLPlus and SQLLoader utilities,
which allows you to minimize multiple input of the same commands when you work with these utilities.



# 2. DESCRIPTION OF THE FILES

The root folder stores shortcuts to the executable batch file, shortcuts to files with settings, csv files with data
The CSVLoader folder contains all the main files with the functionality of this utility


  2.1. CSVLoader.bat - Main batch file.


  2.2. Load.ini - File with settings for connecting to the database and loading options

  The content of ini-file is following (example):

  CSVFILE = DataForImportToDB.csv
  USERID = usrName
  PASSWORD = pswd
  SERVER = srv
  TABLESPACE = tblsps

    2.2.1. The CSVFILE parameter contains the name of the file for importing data into the Oracle database. By default, this is the DataForImportToDB.csv file.
    The file specified in this parameter must be stored in the root folder of the program. Thus, you can change the contents of CSVFILE
    to a new value and place matched file to the root folder, or do not change the parameter value, but change the contents of DataForImportToDB.csv
    every time you use the utility

    2.2.2. The USERID parameter contains the name of the database user. You need to replace the usrName value with the user's real login name

    2.2.3. The PASSWORD parameter contains the password of the user specified in the item above. Similar to 2.2.2. the pswd value must be replaced with the actual one

    2.2.4. The SERVER parameter contains the alias of the database to which the connection will be made. It must match the name
    stored in the TnsNames.ora file.

    For example, if TnsNames.ora includes:

    ORCL.TEST.OURCOMPANY.ORG=
     (DESCRIPTION=
       (ADDRESS=
         (PROTOCOL=TCP)
         (HOST=oracle)
         (PORT=1521)
       )
       (CONNECT_DATA=
         (SERVICE_NAME=ORCL)
       )
    )

    then SERVER = ORCL.TEST.OURCOMPANY.ORG should be written in the Load.ini file
   
    2.2.5. The TABLESPACE parameter contains the name of the tablespace in which (if necessary, see the description of the program menu below)
    a table will be created into which the data from the csv file will be loaded


  2.3. DataForImportToDB.csv (or another filename specified in CSVFILE parameter of Load.ini, see above) - a file for importing data into the Oracle database.
  Its first line must contain the names of the columns that refer to an existing table, or will be created
  along with the table. The default column separator is ";"


  2.4. Init_Buf_Data.SQL - refers to the task of uploading data from the database to a csv file. It contains a script that will be executed
  before uploading the data. It is useful for cases where, for example, you need to load something into buffer/temporary tables, and/or process
  and save some data using a certain algorithm before launching the main export cursor (CsvExportCursor.SQL file).
  Note! This file will be executed in the same session as CsvExportCursor.SQL


  2.5. CsvExportCursor.SQL - File with an SQL query to export data.
  It contains a constant declaration section:

  --################################################ #########################
  -- Constant declaration block
   
  ...
   
  -- End of Constant declaration block
  --################################################ #########################

  and Request Placement Block:

  --################################################ #########################
  -- SQL query declaration block to open the cursor
  -- Replace the following query text with the actual one
  -------------------------------------------------- -----------------------
   
  select ...

  ;
  -------------------------------------------------- -----------------------
  -- End of SQL-query declaration to open the cursor
  --################################################ #########################


  2.6. ExportedData.csv - automatically created file with data of CsvExportCursor.SQL results



# 3. WORKING WITH THE PROGRAM

Run CSVLoader.bat. The following menu will appear:
1) Table of csv file does not exist or its structure needs to be changed
2) Table of csv file exists, only need to upload data
3) Upload the data to a csv file
Enter the number matched to the selected item and press Enter>


  3.1. Table of csv file does not exist or its structure needs to be changed.
  This menu item is suitable for the case when the table for loading data does not exist, it needs to be created,
  or it exists, but its structure needs to be changed.
  After entering 1, the screen will prompt you to enter the name of the table to be created. Type it in and press Enter,
  Next, the algorithm will automatically extract all column names from the first line of the input csv file and prompt you to enter data types for them

  Possible data types and their designations:
  i - integer
  n - number
  d - date
  v[N] - varchar2, where N is the size of the string

  After entering the data types of the columns, the program will launch SQLPlus and execute the script to create/modify the table,
  and then load the data into it using the SQLLoader utility.
  Note! If a table is being modified, then programm will DROP the old version and CREATE the new one, i.e. if data was stored in it, then it will not be saved


  
  3.2. Table of csv file exists, only need to upload data.
  This menu item is similar to the previous one, except that the script will only load data into an existing table without DDL
  Also menu will offer
  Select action type:
  1 TRUNCATE - Table needs to be cleared. User must have TRUNCATE grants
  2 APPEND - Records will be added to the table, and existing records, if any, will not be deleted  


  3.3. Upload the data to a csv file
  Uploading data from the database to the ExportedData.csv file.
  First you need to edit Init_Buf_Data.SQL and CsvExportCursor.SQL (see paragraphs 2.4. and 2.5.)
  Note! If preliminary scripts are not provided, then the file Init_Buf_Data.SQL can be left empty
