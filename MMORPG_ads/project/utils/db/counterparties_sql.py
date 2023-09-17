from .connection import *

DB = 'project/db.sqlite3'


def create_table(conn, create_table_sql):

    try:
        c = conn.cursor()
        result = c.execute(create_table_sql)
        return result
    except Error as e:
        print(e)


def exec_command(conn, ins_sql):

    try:
        c = conn.cursor()
        result = c.execute(ins_sql)
        return result
    except Error as e:
        print(e)


def select_all_counterparties(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM COUNTERPARTIES")

    return cur.fetchall()

    # for row in rows:
    #     print(row)


# if __name__ == '__main__':
cn = create_connection(DB)
sql_create_counterparties_table = """ CREATE TABLE IF NOT EXISTS COUNTERPARTIES (
                                        COUNTERPARTY_ID integer PRIMARY KEY,
                                        COUNTERPARTY_NAME text NOT NULL,
                                        begin_date date,
                                        end_date date
                                    ); """
create_table(cn, sql_create_counterparties_table)
exec_command(cn, "DELETE FROM COUNTERPARTIES")
exec_command(cn, "INSERT INTO COUNTERPARTIES values(1, 'AbsolutBank', '01.01.2023', null)")
exec_command(cn, "INSERT INTO COUNTERPARTIES values(2, 'SkillFactory', '01.01.2023', null)")
exec_command(cn, "INSERT INTO COUNTERPARTIES values(3, 'LinkedIn', '01.01.2023', null)")
cn.commit()
# disconnect(cn)
# main()
