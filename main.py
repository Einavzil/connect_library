import mysql.connector

"""A program that connects to the database and doing SELECT, UPDATE,
INSERT and DELETE statements in MySQL -------------------------------"""


"""Connect to the database when running the program"""    

dsn = {
"user": "maria",
"password": "P@ssw0rd",
"host": "127.0.0.1",
"port": "3306",
"raise_on_warnings": True,
}

try:
    conn = mysql.connector.connect(**dsn)
    cursor = conn.cursor()
        
except Exception as err:
    print(err)


def main():
    print("Welcome to MySQL program to connect to the library database!")
    
    menu = """
    1. SELECT
    2. INSERT
    3. UPDATE
    4. DELETE
    5. EXIT
    """
    
    keep_going = True
    while keep_going:
        print(menu)
        choice = int(input("Choice ->  "))
        match choice:
            case ['1']:
                """select"""
                pass
            case 2:
                """insert"""
                pass
            case 3:
                """update"""
                pass
            case 4:
                """delete"""
                pass
            case 5:
                print("Bye!!")
                cursor.close()
                conn.close()
                keep_going = False

if __name__ == "__main__":
    main()