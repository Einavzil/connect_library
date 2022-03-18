"""
Welcome to MySQL program that connects to the library database!

------------------------------------------------------------------
"""

import mysql.connector

"""A program that connects to the database and doing SELECT, UPDATE,
INSERT and DELETE statements in MySQL -------------------------------"""


"""Connect to the database when running the program"""

dsn = {
    "user": "maria",
    "password": "password",
    "host": "127.0.0.1",
    "port": "3306",
    "database": "library",
    "raise_on_warnings": True,
}

try:
    conn = mysql.connector.connect(**dsn)
    cursor = conn.cursor()

except Exception as err:
    print(err)


def select1():
    """SELECT all borrows that are late to return."""
    try:
        cursor = conn.cursor(prepared=True)
        sql = """
            SELECT
                borrow_id AS 'Borrow ID',
                borrow.borrowdate AS 'Borrow Date',
                borrow.duedate AS 'Due Date',
                borrow.memberid AS 'Member ID',
                CONCAT(member.firstname, " ", member.lastname) AS 'Member Name',
                member.phone AS 'Phone Number',
                borrow.bookid AS 'Book ID'
            FROM borrow
            JOIN member
            ON borrow.memberid = member.id
            WHERE duedate < CURDATE() AND borrow.returneddate IS NULL
            ;
            """

        print(f"\nSQL statement: \n{sql}\n")

        cursor.execute(sql)

        result = cursor.fetchall()

        print("\n{0:<10} | {1:<20} | {2:<20} | {3:<20} | {4:<20} | {5:<20} | {6:<20}".format(*cursor.column_names))
        print("-" * 138)
        for row in result:
            print(f"{row[0]:<10} | {str(row[1]):<20} | {str(row[2]):<20} | {row[3]:<20} | {row[4]:<20} | {row[5]:<20} | {row[6]:<20}")
    except Exception as err:
        print(err)


def select2():
    """SELECT if a book is available (or more than one)."""
    try:
        cursor = conn.cursor(prepared=True)
        sql = """
            SELECT book.id AS 'Book ID',
                book.name AS 'Name',
                book.genre AS 'Book genre'
            FROM book
            LEFT JOIN (SELECT MAX(borrow_id) AS last_borrow_id,
                bookid FROM borrow GROUP BY bookid) AS lastborrows
                ON lastborrows.bookid = book.id
            LEFT JOIN borrow
                ON borrow.borrow_id = lastborrows.last_borrow_id
            WHERE (book.id NOT IN (SELECT bookid FROM borrow) OR
                borrow.returneddate IS NOT NULL) AND book.name LIKE ?
            ;
        """

        print(f"\nSQL statement: \n{sql}\n")
        bookname = input("Keyword (press 'enter' for all) -->  ")
        arg = (f"%{bookname}%",)

        cursor.execute(sql, arg)
        result = cursor.fetchall()

        print("\n{0:<10} | {1:<45} | {2:<20}".format(*cursor.column_names))
        print("-" * 85)
        for row in result:
            print(f"{row[0]:<10} | {str(row[1]):<45} | {str(row[2]):<20}")
    except Exception as err:
        print(err)


def select3():
    """SELECT all books written by an author."""
    try:
        cursor = conn.cursor(prepared=True)

        sql = """
            SELECT
                DISTINCT name AS 'Book Name',
                genre AS 'Genre'
            FROM book
            INNER JOIN writtenby
            ON book.id = writtenby.book_id
            INNER JOIN author
            ON writtenby.author_id = author.id
            WHERE author.lastname LIKE ? AND author.firstname LIKE ?
            ;
        """
        print(f"\nSQL statement: \n{sql}\n")
        author_first = input("Enter first name --> ")
        author_last = input("Enter last name --> ")
        args = (f"%{author_last}%", f"%{author_first}%")

        cursor.execute(sql, args)
        result = cursor.fetchall()

        print("\n{0:<42} | {1:<15} ".format(*cursor.column_names) + "\n" + "-" * 65)
        for row in result:
            print(f"{row[0]:<42} | {str(row[1]):<15}")
    except Exception as err:
        print(err)


def insert():
    """INSERT new study room reservation."""
    try:
        cursor = conn.cursor(prepared=True)

        sql = """
        INSERT INTO reserve (memberid, roomnumber, date, startingtime, endingtime)
        VALUES (? , ? , ? , ? , ?)
        ;
        """
        print(f"\nSQL statement: \n{sql}\n")

        member_id = input("Member ID -->  ")
        room_number = input("Room number -->  ")
        date = input("Date (DD.MM.YYYY) -->  ").split(".")
        starting = input("Starting time (HH) -->  ")
        ending = input("Ending time (HH) -->  ")

        date_format = (f"{date[2]}-{date[1]}-{date[0]}")
        args = (member_id, room_number, date_format, f"{starting}:00:00", f"{ending}:00:00")

        cursor.execute(sql, args)
        print(f"\n{cursor.rowcount} rows affected.")
        conn.commit()

        see_result = input("Do you want to see your input in the table (y/n)? ").lower()
        if (see_result == "yes") or (see_result == "y"):
            sql1 = """
            SELECT *
            FROM reserve
            WHERE memberid = ?
            """

            cursor.execute(sql1, (member_id,))
            result = cursor.fetchone()

            print("\n{0:<5} | {1:<10} | {2:<10} | {3:<12} | {4:<12} | {5:<12}".format(*cursor.column_names) + "\n" + "-" * 65)
            print(f"{str(result[0]):<5} | {str(result[1]):<10} | {str(result[2]):<10} | {str(result[3]):<12}" +
                  f"| {str(result[4]):<12}| {str(result[5]):<12}")
    except Exception as err:
        print(err)


def update():
    """
    UPDATE borrow table after a book is returned.

    First show the borrow table before update,
    Then prompt the user for a borrow to update.
    """
    try:
        cursor = conn.cursor(prepared=True)

        sql_select = """
        SELECT *
        FROM borrow
        ;
        """
        print(f"\nSQL SELECT statement: \n{sql_select}\n")

        cursor.execute(sql_select)
        result = cursor.fetchall()

        print("\n{0:<10} | {1:<10} | {2:<10} | {3:<12} | {4:<10} | {5:<8} | {6:<10}".format(*cursor.column_names) + "\n" + "-" * 120)
        for row in result:
            print(f"{str(row[0]):<10} | {str(row[1]):<10} | {str(row[2]):<10}" +
                  f" | {str(row[3]):<12} | {str(row[4]):<10} | {str(row[5]):<8} | {str(row[6]):<10}")

        cursor = conn.cursor(prepared=True)

        sql = """
        UPDATE borrow
        SET returneddate = CURDATE(), librarianid = ?
        WHERE bookid = ? AND returneddate IS NULL
        ;
        """
        print(f"\nSQL statement: \n{sql}\n")

        lib_id = input("Enter a librarian ID -->  ")
        book_id = input("Enter a book ID -->  ")
        args = (lib_id, book_id)
        cursor.execute(sql, args)

        print(f"\n{cursor.rowcount} rows affected.")
        conn.commit()

    except Exception as err:
        print(err)


def delete():
    """DELETE a member from the member table (and all the borrow records)."""
    try:
        cursor = conn.cursor(prepared=True)

        sql = """
        DELETE FROM member
        WHERE id = ?
        ;
        """
        print(f"\nSQL statement: \n{sql}\n")

        member_id = input("Enter a member ID to delete -->  ")
        args = (member_id,)
        choice = input("This will delete all the member borrow records. \nAre you sure (y/n)? -->  ")
        while choice:
            if (choice.lower() == 'y') or (choice.lower() == 'yes'):
                cursor.execute(sql, args)
                print(f"\n{cursor.rowcount} rows affected.")
                conn.commit()
                break
            elif (choice.lower() == 'n') or (choice.lower() == 'no'):
                break
            else:
                print("Please enter a valid choice.")
                choice = input("This will delete all the member borrow records. \nAre you sure (y/n)? -->  ")
    except Exception as err:
        print(err)


def main():
    """Main function to print the menues and control the user's choices."""
    print(__doc__)

    menu = """
    1. SELECT
    2. INSERT
    3. UPDATE
    4. DELETE
    5. EXIT
    """

    menu_select = """
    1. SELECT all borrows that are late to return
    2. SELECT if a book is available (or more than one)
    3. SELECT all books written by an author
    4. Main menu
    """

    """loop in the menu until the user choose to exit."""
    keep_going = True
    while keep_going:
        print(menu)

        choice = input("Choice ->  ")
        if choice == '1':
            """SELECT"""
            """Print select menu and let the user choose which select to show."""
            while True:
                print(menu_select)
                choice_select = input("Choice ->  ")
                if (choice_select == '1') or (choice_select == '2') or (choice_select == '3'):
                    if choice_select == '1':
                        """Calling select1 function to execute option 1."""
                        select1()
                    elif choice_select == '2':
                        """Calling select1 function to execute option 2."""
                        select2()
                    elif choice_select == '3':
                        """Calling select1 function to execute option 3."""
                        select3()
                    continue_select = input("\nAnother SELECT option (y/n)? ->  ")
                    if (continue_select == 'no') or (continue_select == 'n'):
                        break
                else:
                    if choice_select == '4':
                        """Go back to main menu."""
                        break
                    else:
                        print("Please choose one of the options.")

        elif choice == '2':
            """INSERT"""
            insert()
        elif choice == '3':
            """UPDATE"""
            update()
        elif choice == '4':
            """DELETE"""
            delete()
        elif choice == '5':
            cursor.close()
            conn.close()
            print("\nConnection closed.")
            print("Bye!!\n")
            keep_going = False
        else:
            print("Please choose one of the options.")


if __name__ == "__main__":
    main()
