@mode con cp select=1251
@echo off
echo.

FOR /F "TOKENS= 1,2* DELIMS==,;#/ " %%i IN (Load.ini) DO (
  IF %%i==USERID (
    set vUSER_ID=%%j
  )
  IF %%i==PASSWORD (
    set vPASSWORD=%%j
  )
  IF %%i==SERVER (
    set vSERVER=%%j
  )
  IF %%i==TABLESPACE (
    set vTABLESPACE=%%j
  )
)

FOR /F "TOKENS=1,2 DELIMS=^= " %%i IN (Param.txt) DO (
  IF %%i==USERID (
    echo USERID = %vUSER_ID%@%vSERVER%/%vPASSWORD% >> Param.tmp
  ) ELSE (
    echo %%i = %%j >> Param.tmp
  )
)

type Param.tmp > Param.txt
del Param.tmp

echo %vTABLESPACE% > TABLESPACE.txt

echo Choose the type of action:
echo.
echo 1) Table of csv file does not exist or its structure needs to be changed
echo 2) Table of csv file exists, only need to upload data
echo 3) Upload the data to a csv file
Set /P $input= Input the number corresponding to the selected item and press Enteer ^>

if "%$input%"=="3" (
  echo The data will be uploaded to a file ../ExportedData.csv, near the shortcut of CSVLoader.bat  
  pause  
  sqlplus %vUSER_ID%/%vPASSWORD%@%vSERVER% @ExportToCSV.SQL
  pause
  exit
)

Set /P $tabName= Enter the name of the table ^>


echo %$tabName% > TableName.txt

if "%$input%"=="1" (
  CD CreateTableScriptGenerator
  CreateTableScriptGenerator.exe
  CD ..  
  CD LoadDataScriptGenerator
  LoadDataScriptGenerator.exe
  CD ..
  sqlplus %vUSER_ID%/%vPASSWORD%@%vSERVER% @CreateTable.SQL
)


if "%$input%"=="2" (
  echo.
  echo Choose the type of action:
  echo 1 TRUNCATE - Table needs to be cleared. User must have TRUNCATE grants
  echo 2 APPEND - Records will be added to the table, and existing records, if any, will not be deleted  
  echo.
)  

if "%$input%"=="2" (
  Set /P $LoadOption= Input the number corresponding to the selected item and press Enteer ^>  
)

if "%$input%"=="2" (

  if "%$LoadOption%"=="1" (
    echo TRUNCATE  > LoadOption.txt
  )

  if "%$LoadOption%"=="2" (
    echo APPEND > LoadOption.txt
  )  

  CD LoadDataScriptGenerator
  LoadDataScriptGenerator.exe
  CD ..
)


sqlldr PARFILE = 'Param.txt'
pause
exit