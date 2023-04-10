<<<<<<< HEAD
program CreateTableScriptGenerator;
{$APPTYPE CONSOLE}
uses
  SysUtils, Windows, Classes;
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
  ColNamesList, ColTypesList: TStringArray;
  i: integer;
  j: integer;
  ErrFlag: boolean;
  CreateTableScript, LoadDataScript: TStrings;
  Param: TStrings;
  tableName, tableSpaceName: String;
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
  writeln('Specify the data types of the columns of the table being created. Example: ');
  writeln('integer - key [i]');
  writeln('date - key [d]');
  writeln('number - key [n]');
  writeln('varchar2[N] - vN, N - field size in characters');
  writeln;

  j:=0;

  inputLoop:
  for i:= j to Length(ColNamesList) - 1 do
  begin
    ErrFlag := false;
    write(ColNamesList[i]+': ');
    readln(str);
    str := UpperCase(str);

    if (Length(Str) > 1) or (Str = 'V' ) then
    try
      StrToInt(copy(Str, 2, Length(Str)));
    except
      ErrFlag := true;
    end;

    if (str[1] in ['I', 'N', 'D']) and (Length(str) > 1) then
      ErrFlag := true;
   
    if not (str[1] in ['I', 'N', 'D', 'V']) or ErrFlag then
    begin
      writeln('invalid value');
      j:=i;
      goto inputLoop;
    end;

    SetLength(ColTypesList, i + 1);
    ColTypesList[i] := str;

  end;

  try
    AssignFile(F, '..\tableName.txt');
    Reset(F);
    readln(F, tableName);
    CloseFile(F);
  except
    Writeln('File ' + '..\tableName.txt' + ' not found');
    Writeln('Press Enter to exit...');
    Readln;
    Exit;
  end;

  CreateTableScript := TStringList.Create;
  CreateTableScript.Add('DROP TABLE ' + tableName + ';');
  CreateTableScript.Add('CREATE TABLE ' + tableName + '(');

  for i:=0 to Length(ColNamesList) - 1 do
  begin
    if i = Length(ColNamesList) - 1 then
      str := ''
    else
      str := ',';

    case ColTypesList[i][1] of
      'I': CreateTableScript.Add('  ' + ColNamesList[i] + ' INTEGER' + str);
      'D': CreateTableScript.Add('  ' + ColNamesList[i] + ' DATE' + str);
      'N': CreateTableScript.Add('  ' + ColNamesList[i] + ' NUMBER' + str);
      'V': CreateTableScript.Add('  ' + ColNamesList[i] + ' VARCHAR2(' +
             copy(ColTypesList[i], 2, Length(ColTypesList[i])) + ' )' + str
           );
    end;
  end;

  try
    AssignFile(F, '..\TABLESPACE.txt');
    Reset(F);
    readln(F, tableSpaceName);
    CloseFile(F);
  except
    Writeln('File ' + '..\TABLESPACE.txt' + ' not found');
    Writeln('Press Enter to exit...');
    Readln;
    Exit;
  end;

  CreateTableScript.Add(') TABLESPACE ' + tableSpaceName +';');
  CreateTableScript.Add('Exit;');
  CreateTableScript.SaveToFile('../CreateTable.SQL');

  LoadDataScript := TStringList.Create;
  LoadDataScript.LoadFromFile('../LoadData.ctl');
  for i := LoadDataScript.Count - 1 downto 0 do
  if upperCase(LoadDataScript[i]) <> UpperCase('fields terminated by ";"') then
    LoadDataScript.Delete(i)
  else
  begin
    LoadDataScript[i-1] := 'INTO TABLE ' + tableName;
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
=======
program CreateTableScriptGenerator;
{$APPTYPE CONSOLE}
uses
  SysUtils, Windows, Classes;
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
  ColNamesList, ColTypesList: TStringArray;
  i: integer;
  j: integer;
  ErrFlag: boolean;
  CreateTableScript, LoadDataScript: TStrings;
  Param: TStrings;
  tableName, tableSpaceName: String;
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
  writeln('Specify the data types of the columns of the table being created. Example: ');
  writeln('integer - key [i]');
  writeln('date - key [d]');
  writeln('number - key [n]');
  writeln('varchar2[N] - vN, N - field size in characters');
  writeln;

  j:=0;

  inputLoop:
  for i:= j to Length(ColNamesList) - 1 do
  begin
    ErrFlag := false;
    write(ColNamesList[i]+': ');
    readln(str);
    str := UpperCase(str);

    if (Length(Str) > 1) or (Str = 'V' ) then
    try
      StrToInt(copy(Str, 2, Length(Str)));
    except
      ErrFlag := true;
    end;

    if (str[1] in ['I', 'N', 'D']) and (Length(str) > 1) then
      ErrFlag := true;
   
    if not (str[1] in ['I', 'N', 'D', 'V']) or ErrFlag then
    begin
      writeln('invalid value');
      j:=i;
      goto inputLoop;
    end;

    SetLength(ColTypesList, i + 1);
    ColTypesList[i] := str;

  end;

  try
    AssignFile(F, '..\tableName.txt');
    Reset(F);
    readln(F, tableName);
    CloseFile(F);
  except
    Writeln('File ' + '..\tableName.txt' + ' not found');
    Writeln('Press Enter to exit...');
    Readln;
    Exit;
  end;

  CreateTableScript := TStringList.Create;
  CreateTableScript.Add('DROP TABLE ' + tableName + ';');
  CreateTableScript.Add('CREATE TABLE ' + tableName + '(');

  for i:=0 to Length(ColNamesList) - 1 do
  begin
    if i = Length(ColNamesList) - 1 then
      str := ''
    else
      str := ',';

    case ColTypesList[i][1] of
      'I': CreateTableScript.Add('  ' + ColNamesList[i] + ' INTEGER' + str);
      'D': CreateTableScript.Add('  ' + ColNamesList[i] + ' DATE' + str);
      'N': CreateTableScript.Add('  ' + ColNamesList[i] + ' NUMBER' + str);
      'V': CreateTableScript.Add('  ' + ColNamesList[i] + ' VARCHAR2(' +
             copy(ColTypesList[i], 2, Length(ColTypesList[i])) + ' )' + str
           );
    end;
  end;

  try
    AssignFile(F, '..\TABLESPACE.txt');
    Reset(F);
    readln(F, tableSpaceName);
    CloseFile(F);
  except
    Writeln('File ' + '..\TABLESPACE.txt' + ' not found');
    Writeln('Press Enter to exit...');
    Readln;
    Exit;
  end;

  CreateTableScript.Add(') TABLESPACE ' + tableSpaceName +';');
  CreateTableScript.Add('Exit;');
  CreateTableScript.SaveToFile('../CreateTable.SQL');

  LoadDataScript := TStringList.Create;
  LoadDataScript.LoadFromFile('../LoadData.ctl');
  for i := LoadDataScript.Count - 1 downto 0 do
  if upperCase(LoadDataScript[i]) <> UpperCase('fields terminated by ";"') then
    LoadDataScript.Delete(i)
  else
  begin
    LoadDataScript[i-1] := 'INTO TABLE ' + tableName;
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
>>>>>>> ce7bde083186c37ac612a0f0c9218c3e0f6fe889
