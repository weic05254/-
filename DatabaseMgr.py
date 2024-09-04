
import sqlite3
import threading

LWork_lock = threading.Lock()
LWork_conn = sqlite3.connect('LWork.db', check_same_thread=False)
LWork_cursor = LWork_conn.cursor()


def CreateTable():
    LWork_conn.execute('''CREATE TABLE IF NOT EXISTS FeedBack (
                    id INTEGER PRIMARY KEY,
                    Name VARCHAR(255) NOT NULL,
                    Email VARCHAR(255) NOT NULL,
                    IssueDesc TEXT NOT NULL
                )''')
    
    LWork_conn.execute('''CREATE TABLE IF NOT EXISTS Members (
                    id INTEGER PRIMARY KEY,
                    UserName VARCHAR(255) NOT NULL,
                    Pwd VARCHAR(255) NOT NULL,
                    Email VARCHAR(255) NOT NULL,
                    PermissionLevel INTEGER DEFAULT 0,
                    IsVerified INTEGER DEFAULT 0,
                    VerificationCode VARCHAR(255),
                    V_ExpirationTime INTEGER,
                    
                    UNIQUE(UserName)
                )''')
    LWork_conn.execute('''CREATE TABLE IF NOT EXISTS ShopItem (
                    id INTEGER PRIMARY KEY,
                    Name NVARCHAR(255) NOT NULL,
                    Desc NVARCHAR(255) NOT NULL,
                    Price INTEGER NOT NULL
                 )''')

    LWork_conn.execute('''CREATE TABLE IF NOT EXISTS Purchases (
                    id INTEGER PRIMARY KEY,
                    Member_id INTEGER,
                    ShopItem_id INTEGER,
                    PurchaseDate INTEGER,
                    FOREIGN KEY (Member_id) REFERENCES Members(id),
                    FOREIGN KEY (ShopItem_id) REFERENCES ShopItem(id)
                 )''')

    LWork_conn.execute('''CREATE TABLE IF NOT EXISTS ActivationCodes (
                    id INTEGER PRIMARY KEY,
                    HWID VARCHAR(255) NOT NULL,
                    ExpiryDate INTEGER,
                    Activated INTEGER DEFAULT 0,
                    UNIQUE(HWID)
                )''')

    LWork_conn.execute('''CREATE TABLE IF NOT EXISTS MemberHWID (
                    id INTEGER PRIMARY KEY,
                    Member_id INTEGER,
                    Item_id INTEGER,
                    HWID VARCHAR(255) NOT NULL,
                    Activated INTEGER DEFAULT 1,
                    FOREIGN KEY (Member_id) REFERENCES Members(id),
                    FOREIGN KEY (Item_id) REFERENCES ShopItem(id),
                    UNIQUE(HWID)
                )''')
CreateTable()


StdData_lock = threading.Lock()
StdData_conn = sqlite3.connect('Global_StdData.db', check_same_thread=False)
StdData_cursor = StdData_conn.cursor()
try:
    StdData_conn.execute(f"""
                CREATE TABLE IF NOT EXISTS StdScoreData (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                StdID VARCHAR(50),
                Term NVARCHAR(50),
                ClassID NVARCHAR(50),
                ClassName NVARCHAR(255),
                Score INTEGER,
                UNIQUE(StdID, Term, ClassID, ClassName, Score)
                );""")
except Exception as e:
    print(e)