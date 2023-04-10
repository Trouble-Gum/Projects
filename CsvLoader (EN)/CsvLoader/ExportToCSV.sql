set colsep ';'    
set pagesize 0  
set trimspool on
set headsep off  
set linesize 300  
set numw 10  

@..\Init_Buf_Data.SQL

SET SERVEROUTPUT ON;
spool ..\ExportedData.csv
@..\CsvExportCursor.SQL