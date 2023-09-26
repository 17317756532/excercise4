import sqlite3

# Create a database connection
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Author TEXT NOT NULL,
        ISBN TEXT NOT NULL,
        Status TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
        BookID INTEGER,
        UserID INTEGER,
        ReservationDate DATE,
        FOREIGN KEY (BookID) REFERENCES Books (BookID),
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')

# Function to add a new book to the Books table
def add_book(title, author, isbn, status):
    cursor.execute('''
        INSERT INTO Books (Title, Author, ISBN, Status)
        VALUES (?, ?, ?, ?)
    ''', (title, author, isbn, status))
    conn.commit()
    print('Book added successfully!')

# Function to find a book's detail based on BookID
def find_book(book_id):
    cursor.execute('''
        SELECT Books.*, Reservations.ReservationDate, Users.Name, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
        WHERE Books.BookID = ?
    ''', (book_id,))
    result = cursor.fetchone()

    if result:
        book_id, title, author, isbn, status, reservation_date, user_name, user_email = result
        print('Book ID:', book_id)
        print('Title:', title)
        print('Author:', author)
        print('ISBN:', isbn)
        print('Status:', status)
        if reservation_date and user_name and user_email:
            print('Reserved by:', user_name)
            print('Reservation Date:', reservation_date)
        else:
            print('Not reserved by anyone.')
    else:
        print('Book not found.')

# Function to find a book's reservation status based on various parameters
def find_reservation_status(text):
    if text.startswith('LB'):
        # Search by BookID
        cursor.execute('''
            SELECT Books.Status, Reservations.ReservationDate, Users.Name, Users.Email
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.BookID = ?
        ''', (text,))
        result = cursor.fetchone()
    elif text.startswith('LU'):
        # Search by UserID
        cursor.execute('''
            SELECT Books.Title, Books.Status, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            WHERE Reservations.UserID = ?
        ''', (text,))
        result = cursor.fetchone()
    elif text.startswith('LR'):
        # Search by ReservationID
        cursor.execute('''
            SELECT Books.Title, Books.Status, Users.Name, Users.Email
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Reservations.ReservationID = ?
        ''', (text,))
        result = cursor.fetchone()
    else:
        # Search by Title
        cursor.execute('''
            SELECT Books.BookID, Books.Status, Users.Name, Users.Email
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.Title = ?
        ''', (text,))
        result = cursor.fetchone()

    if result:
        print('Reservation Status:')
        print('Book:', result[0])
        print('Status:', result[1])
        if result[2]:
            print('Reserved by:', result[2])
            print('Reservation Date:', result[3])
        else:
            print('Not reserved by anyone.')
    else:
        print('No matching reservation found.')

# Function to find all the books in the database
def find_all_books():
    cursor.execute('''
        SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, 
        Reservations.ReservationDate, Users.Name, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
    ''')
    result = cursor.fetchall()

    if result:
        print('All Books in the Database:')
        for row in result:
            book_id, title, author, isbn, status, reservation_date, user_name, user_email = row
            print('Book ID:', book_id)
            print('Title:', title)
            print('Author:', author)
            print('ISBN:', isbn)
            print('Status:', status)
            if reservation_date and user_name and user_email:
                print('Reserved by:', user_name)
                print('Reservation Date:', reservation_date)
            else:
                print('Not reserved by anyone.')
            print('---')
    else:
        print('No books found in the database.')

# Function to modify/update book details based on BookID
def update_book(book_id, new_status):
    cursor.execute('''
        UPDATE Books
        SET Status = ?
        WHERE BookID = ?
    ''', (new_status, book_id))
    conn.commit()
    print('Book details updated successfully!')

# Function to delete a book based on its BookID
def delete_book(book_id):
    cursor.execute('''
        DELETE FROM Books
        WHERE BookID = ?
    ''', (book_id,))
    cursor.execute('''
        DELETE FROM Reservations
        WHERE BookID = ?
    ''', (book_id,))
    conn.commit()
    print('Book deleted successfully!')

# Main program loop
while True:
    print('Library Management System')
    print('1. Add a new book to the database')
    print('2. Find a book\'s detail based on BookID')
    print('3. Find a book\'s reservation status')
    print('4. Find all the books in the database')
    print('5. Modify/update book details based on BookID')
    print('6. Delete a book based on its BookID')
    print('7. Exit')

    choice = input('Enter your choice (1-7): ')

    if choice == '1':
        title = input('Enter the title: ')
        author = input('Enter the author: ')
        isbn = input('Enter the ISBN: ')
        status = input('Enter the status: ')
        add_book(title, author, isbn, status)
    elif choice == '2':
        book_id = input('Enter the BookID: ')
        find_book(book_id)
    elif choice == '3':
        text = input('Enter the BookID, Title, UserID, or ReservationID: ')
        find_reservation_status(text)
    elif choice == '4':
        find_all_books()
    elif choice == '5':
        book_id = input('Enter the BookID: ')
        new_status = input('Enter the new status: ')
        update_book(book_id, new_status)
    elif choice == '6':
        book_id = input('Enter the BookID: ')
        delete_book(book_id)
    elif choice == '7':
        print('Exiting the program...')
        break
    else:
        print('Invalid choice. Please try again.')

# Close the database connection
conn.close()