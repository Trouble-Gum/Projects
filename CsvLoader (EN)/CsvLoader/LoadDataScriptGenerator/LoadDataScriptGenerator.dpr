program LoadDataScriptGenerator;
{$APPTYPE CONSOLE}
uses
  SysUtils,
  Windows,
  Classes;

type
  TStringArray = Array of string;  

  function SplitS(S: String; Delimiter:TSysCharSet = [#9]): TStringArray;
  var
     len, idx1, idx2, idx: integer;
  begin
       Result := nil;
       if Length(S) = 0 then Exit;
       len := Length(S);
       SetLength(Result, len);
       idx2 := 1;
       idx := 0;
       repeat
         idx1 := idx2;
         while (idx2 <= len) and not(S[idx2] in Delimiter) do inc(idx2);
         if idx1 <= idx2 then
         begin
            Result[idx] := (Copy(S, idx1, idx2-idx1));
            inc(idx);
         end;
         if (idx2 <= len) and (S[idx2] in Delimiter) then inc(idx2);
       until idx2 > len;
       SetLength(Result, idx);
  end;
var
  str: string;
  F: TextFile;
  ColNamesList: TStringArray;
  i: integer;
  CreateTableScript, LoadDataScript: TStrings;
  Param: TStrings;
  tableName: String;
  loadOption: String;
  fileName: string = '..\..\Test.csv';
  vPos1, vPos2: integer;
  label inputLoop;
begin
try
  // Insert user code here
  //WinExec('InitFont.bat', 1);

  Param := TStringList.Create;
  Param.LoadFromFile('..\Load.ini');

  for i := 0 to Param.Count - 1 do
  if upperCase(copy(trim(Param.Strings[i]), 1, 7)) = 'CSVFILE' then
  begin
    vPos1 := Pos('=', Param.Strings[i]) + 1;
    vPos2 := Pos('.csv', Param.Strings[i]);
    fileName := trim(copy(Param.Strings[i], vPos1, vPos2));
  end;

  Sleep(500);
  writeln;
  try
    AssignFile(F, '..\..\' + fileName);
    Reset(F);
    readln(F, str);
    CloseFile(F);
  except
    Writeln('File ' + fileName + ' not found');
    Writeln('Press Enter to exit...');
    Readln;
    Exit;
  end;

  ColNamesList := SplitS(str, [';']);

  try
    AssignFile(F, '..\TableName.txt');
    Reset(F);
    readln(F, tableName);
    CloseFile(F);
  except
    Writeln('file ' + '..\TableName.txt' + ' not found');
    Writeln('Press Enter to exit...');
    Readln;
    Exit;
  end;

  try
    AssignFile(F, '..\LoadOption.txt');
    Reset(F);
    readln(F, loadOption);
    CloseFile(F);
  except
    Writeln('File ' + '..\LoadOption.txt' + ' not found');
    Writeln('Press Enter to exit...');
    Readln;
    Exit;
  end;


  LoadDataScript := TStringList.Create;
  LoadDataScript.LoadFromFile('../LoadData.ctl');
  for i := LoadDataScript.Count - 1 downto 0 do
  if upperCase(LoadDataScript[i]) <> UpperCase('fields terminated by ";"') then
    LoadDataScript.Delete(i)
  else
  begin
    LoadDataScript[i-1] := 'INTO TABLE ' + tableName;
    LoadDataScript[i-2] := loadOption;
    LoadDataScript[i-3] := 'INFILE "..\' + fileName + '"';
    break;
  end;

  LoadDataScript.Add('(');

  for i:=0 to Length(ColNamesList) - 1 do
  begin
    if i = Length(ColNamesList) - 1 then
      str := ''
    else
      str := ',';

    LoadDataScript.Add(ColNamesList[i] + str);

  end;

  LoadDataScript.Add(')');

  LoadDataScript.SaveToFile('../LoadData.ctl');
finally
  FreeAndNil(LoadDataScript);
  FreeAndNil(CreateTableScript);
  FreeAndNil(Param);
end
end.
