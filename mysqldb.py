import pymysql, tkinter

def create_db():
    con=pymysql.connect(user='root', password='TIGER', host='localhost')
    cur=con.cursor()
    try:
        cur.execute("CREATE DATABASE Minesweeper")
    except Exception:
        print("failed to create")
    con.close()

def create_table():
    con=pymysql.connect(user='root', password='TIGER', host='localhost')
    cursor=con.cursor() 
    cursor.execute("USE Minesweeper")
    cursor.execute("CREATE TABLE Highscores (name VARCHAR(25), time INT, grid VARCHAR(25))") 
    con.commit()  
    con.close()

def insert_score(*args):
    name, time, rows, cols, mines = args
    con=pymysql.connect(user = 'root', password = 'TIGER', host = 'localhost', database = "Minesweeper")
    cursor=con.cursor()
    cursor.execute("insert into Highscores values('" + name + "'," + str(time) +",'" + str(rows) + "x" + str(cols) + "x" + str(mines) + "' )")
    con.commit()  
    if cursor.execute(f"select count(time) from highscores where grid = '{rows}x{cols}x{mines}'") > 3:
        #cursor.execute()
        pass
    con.close()

def disp_highscores(*args):
    rows, cols, mines = args
    con=pymysql.connect(user = 'root', password = 'TIGER', host = 'localhost', database = "Minesweeper")
    cursor=con.cursor()
    cursor.execute(f"select name, time from highscores where grid = '{rows}x{cols}x{mines}' order by time")
    highscores = cursor.fetchall()
    k = 1
    result = "Position\tName\t\tTime\n"
    for i in highscores:
        result += f"{k}"
        for j in i:
            result += f"\t{j}"
        result += "\n"
        k += 1 
    tkinter.messagebox.showinfo(f"Highscores for {rows}x{cols} with {mines} mines", result)
    con.close()

#create_db()
#create_table()