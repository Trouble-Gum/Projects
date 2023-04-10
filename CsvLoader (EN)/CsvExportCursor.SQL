declare
  --########################################################################
  -- Constant declaration block
   
  vConst1 integer := 2;
  vConst2 varchar2(10) := 'RowFactor';
   
  -- End of Constant declaration block
  --########################################################################
   
  v_cursor sys_refcursor;
   
  procedure Open_Cursor is begin open v_cursor for
   
  --########################################################################
  -- SQL query declaration block to open the cursor
  -- Replace the following query text with the actual one
  --------------------------------------------------------------------------
   
  select vConst1 * level || ' ' || vConst2 as value
    from dual
    connect by level <= 10
 
  ;  
  --------------------------------------------------------------------------  
  -- End of SQL-query declaration to open the cursor
  --########################################################################
     
  end Open_Cursor;
   
 
 
  procedure Print_Out_Cursor
  is
    v_cursor_number number;

    v_columns number;
    v_desc_tab dbms_sql.desc_tab;
    v_position number;
    v_typecode number;
     
    v_number_value number;
    v_varchar2_value varchar2(4000);
    v_varchar_value varchar(4000);
    v_date_value date;
     
    vLine varchar2(4000);
     
  begin
    --Convert cursor to DBMS_SQL cursor
    v_cursor_number := dbms_sql.to_cursor_number(rc => v_cursor);
    --Get information on the columns
    dbms_sql.describe_columns(v_cursor_number, v_columns, v_desc_tab);

    --Loop through all the columns, find COLUMN1 position and type
    for i in 1 .. v_desc_tab.count loop

      v_position := i;
      v_typecode := v_desc_tab(i).col_type;

      if v_typecode = dbms_types.typecode_number then
        dbms_sql.define_column(v_cursor_number, i, v_number_value);
      end if;
                 
      if v_typecode = DBMS_TYPES.TYPECODE_CHAR then
        dbms_sql.define_column(v_cursor_number, i, v_varchar2_value, 4000);                
      end if;
     
      if v_typecode = DBMS_TYPES.TYPECODE_VARCHAR then
        dbms_sql.define_column(v_cursor_number, i, v_varchar_value, 4000);                
      end if;
     
      if v_typecode = DBMS_TYPES.TYPECODE_DATE then
        dbms_sql.define_column(v_cursor_number, i, v_date_value);                
      end if;
     
     
      vLine := case when vLine is null then '' else vLine || ';' end || v_desc_tab(i).col_name;
     
    end loop;
     
    DBMS_Output.Put_Line(vLine);
     
    --return;
     
    v_number_value := 1;
     
    --Fetch all the rows, then get the relevant column value and print it
    while dbms_sql.fetch_rows(v_cursor_number) > 0 loop
   
      vLine := '';  
   
      for i in 1 .. v_desc_tab.count loop
        v_position := i;
        v_typecode := v_desc_tab(i).col_type;
       
        if v_typecode = dbms_types.typecode_number then
          dbms_sql.column_value(v_cursor_number, v_position, v_number_value);
          --dbms_output.put_line('Value: '||v_number_value);
          vLine := case when vLine is null then '' else vLine || ';' end || v_number_value;
        end if;
         
        if v_typecode = DBMS_TYPES.TYPECODE_CHAR then
          dbms_sql.column_value(v_cursor_number, v_position, v_varchar2_value);
          --dbms_output.put_line('Value: '||v_varchar2_value);
          vLine := case when vLine is null then '' else vLine || ';' end || v_varchar2_value;
        end if;
       
        if v_typecode in (DBMS_TYPES.TYPECODE_VARCHAR) then
          dbms_sql.column_value(v_cursor_number, v_position, v_varchar_value);
          --dbms_output.put_line('Value: '||v_varchar2_value);
          vLine := case when vLine is null then '' else vLine || ';' end || v_varchar_value;
        end if;
       
        if v_typecode = DBMS_TYPES.TYPECODE_DATE then
          dbms_sql.column_value(v_cursor_number, v_position, v_date_value);
          --dbms_output.put_line('Value: '||v_date_value);
          vLine := case when vLine is null then '' else vLine || ';' end || To_Char(v_date_value, 'dd.mm.yyyy');
        end if;  
      end loop;
     
      DBMS_Output.Put_Line(vLine);
     
    end loop;  
   
  end;
   
   
begin
  --Call procedure to open cursor
  Open_Cursor;
  Print_Out_Cursor;  
end;
/
exit;