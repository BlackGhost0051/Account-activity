import sqlite3
import os

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


DATABASE_FILE = 'mails.db' # you can change database file name

# =============================     DataBase menager   ==============================================
def database_menager_menu(cursor,conn):
    while True:
        print("\nDataBase menager")
        print("1 -> Print all emails")
        print("2 -> Add email")
        print("3 -> Delete email by ID")
        print("0 -> Exit\n")

        value = input("Value: ")

        if value == "1":
            result = select_all_data(cursor)
            for row in result:
                print(row)

        elif value == "2":
            email = input("Enter email: ")
            password = input("Enter password: ")
            insert_data(cursor, conn, email, password)

        elif value == "3":
            del_id = input("Enter id: ")
            delete_data_by_id(cursor, conn, int(del_id))

        elif value == "0":
            return
        else:
            print("Enter a valid value!!!")


def check_and_create_database():
    if not os.path.exists(DATABASE_FILE):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        print("Database", DATABASE_FILE , "not found.", DATABASE_FILE , "was created !!!") #
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            );
        ''')

        conn.commit()
        conn.close()


def get_length(cursor):
    cursor.execute("SELECT COUNT(id) FROM emails;")
    length = cursor.fetchone()[0]
    return length # - 1


def select_all_data(cursor):
    cursor.execute("SELECT * FROM emails;")
    rows = cursor.fetchall()
    return rows


def insert_data(cursor, conn, email, password, id=None):
    if id is None:
        id = get_length(cursor)
    cursor.execute(f"INSERT INTO emails (id, email, password) VALUES ({id}, '{email}', '{password}');")
    conn.commit()


def delete_data_by_id(cursor, conn, id):
    cursor.execute("DELETE FROM emails WHERE id=?", (id,))
    cursor.execute("UPDATE emails SET id = id - 1 WHERE id > ?", (id,))
    conn.commit()

#====================================     Activity menager   ==========================================
def activity_menager_menu(cursor,conn):
    while True:
        print("\nActivity menager")
        print("1 -> Email send")
        print("0 -> Exit\n")

        value = input("Value: ")

        if value == "1":
            result = select_all_data(cursor)
            if result:
                for i in range(get_length(cursor)):
                    email_send(result[i][1], result[i][2])
                    print("Email send ", result[i][1])
            else:
                print("No emails in the database.")

        elif value == "0":
            return
        else:
            print("Enter a valid value!!!")


def email_send(mail,password):
    receiver_email = mail  # you can change

    message = MIMEMultipart("alternative")
    message["Subject"] = "My message"
    message["From"] = mail
    message["To"] = receiver_email

    html = """\
    <html>
        <head>
            <style>
                #red { color: red; }
                #yellow { color: yellow; }
                #blue { color: blue; }
                #pink { color: pink; }
                #purple { color: purple; }
            </style>
        </head>
        <body>
            <h2><span id="red">Hi</span> <span id="yellow">it</span> <span id="blue">is</span> <span id="pink">my</span> <span id="purple">message!</span></h2>
        </body>
    </html>
    """

    part = MIMEText(html, "html")
    message.attach(part)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(mail, password)
            server.sendmail(
                mail, receiver_email, message.as_string()
            )
    except Exception as e:
        print(f"Error {mail}: {e}")


def main():
    check_and_create_database()

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    while True:
        print("\nMENU")
        print("1 -> Activity")
        print("2 -> DataBase menager")
        print("0 -> Exit\n")

        value = input("Value: ")
        if value == "1":
            activity_menager_menu(cursor,conn)
        elif value == "2":
            database_menager_menu(cursor,conn)

        elif value == "0":
            return
        else:
            print("Enter a valid value!!!")

    conn.close()

if __name__ == "__main__":
    main()
