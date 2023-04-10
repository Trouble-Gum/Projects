<<<<<<< HEAD
set colsep ';'    
set pagesize 0  
set trimspool on
set headsep off  
set linesize 300  
set numw 10  

@..\Init_Buf_Data.SQL

SET SERVEROUTPUT ON;
spool ..\ExportedData.csv
=======
set colsep ';'    
set pagesize 0  
set trimspool on
set headsep off  
set linesize 300  
set numw 10  

@..\Init_Buf_Data.SQL

SET SERVEROUTPUT ON;
spool ..\ExportedData.csv
>>>>>>> ce7bde083186c37ac612a0f0c9218c3e0f6fe889
@..\CsvExportCursor.SQL