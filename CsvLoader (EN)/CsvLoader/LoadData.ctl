LOAD DATA
INFILE "..\DataForImportToDB.csv"
TRUNCATE  
INTO TABLE YOUR_TBL_NAME
fields terminated by ";"
(
FIELD1,
FIELD2
)
