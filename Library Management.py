import tkinter as tk
import sqlite3
from tkinter import messagebox


class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("400x400")

        self.books = []  # List to store book details
        self.users = []  # List to store user details


        self.label_title = tk.Label(root, text="Library Management", font=("Helvetica", 20, "bold"))
        self.label_title.pack(pady=20)

        self.button_login = tk.Button(root, text="Already Registered", font=("Helvetica", 10, "bold"), command=self.show_book_details)
        self.button_login.pack(pady=20)

        self.button_register = tk.Button(root, text="Register",font=("Helvetica", 10, "bold"), command=self.show_user_details)
        self.button_register.pack(pady=20)

        # Step 1: Setup Database and File
        self.setup_database()
        self.setup_file()

        self.book_window = None
        self.user_window = None


    def show_book_details(self):
        if self.book_window is None:
            self.book_window = tk.Toplevel(self.root)
            self.book_window.title("Book Details")
            self.book_window.geometry("500x500")

            self.label_book_title = tk.Label(self.book_window, text="Book Title:")
            self.label_book_title.pack()

            self.entry_book_title = tk.Entry(self.book_window, width=30, )
            self.entry_book_title.pack()

            self.label_author = tk.Label(self.book_window, text="Author:")
            self.label_author.pack()

            self.entry_author = tk.Entry(self.book_window, width=30)
            self.entry_author.pack()

            self.button_add_book = tk.Button(self.book_window, text="Add Book", command=self.add_book)
            self.button_add_book.pack(pady=20)

            self.listbox_books = tk.Listbox(self.book_window, width=40, height=10)
            self.listbox_books.pack()

            self.button_delete_book = tk.Button(self.book_window, text="Delete Book", command=self.delete_book)
            self.button_delete_book.pack(pady=20)

            self.button_user_details = tk.Button(self.book_window, text="User Details", command=self.show_user_details)
            self.button_user_details.pack(pady=20)

            self.update_books_listbox()



    def close_book_window(self):
        self.book_window.destroy()
        self.book_window = None



    # Step 2: Modify the LibraryManagementApp Class

    def setup_database(self):
        self.conn = sqlite3.connect("library.db")
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        """)

        self.conn.commit()

    def add_book(self):
        title = self.entry_book_title.get()
        author = self.entry_author.get()

        if title and author:
            book_details = f"{title} by {author}"
            self.books.append(book_details)
            self.add_book_to_database(title, author)  # Save book details to database
            self.add_book_to_file(title, author)  # Save book details to file
            self.update_books_listbox()
            self.entry_book_title.delete(0, tk.END)
            self.entry_author.delete(0, tk.END)
            messagebox.showinfo("Success!! ", "Book added successfully!")
        else:
            messagebox.showerror("Error", "Please enter both book title and author.")

    def add_book_to_database(self, title, author):
        self.conn.execute("""
            INSERT INTO books (title, author)
            VALUES (?, ?)
        """, (title, author))
        self.conn.commit()

    def add_book_to_file(self, title, author):
        with open("book_details.txt", "a") as file:
            file.write(f"{title} by {author}\n")

    def delete_book(self):
        selected_index = self.listbox_books.curselection()
        if selected_index:
            book_details = self.books.pop(selected_index[0])
            self.delete_book_from_database(book_details)  # Delete book details from database
            self.update_books_listbox()
            messagebox.showinfo("Success!! ", "Book Deleted successfully!")

    def delete_book_from_database(self, book_details):
        title, author = book_details.split(" by ")
        self.conn.execute("""
            DELETE FROM books
            WHERE title = ? AND author = ?
        """, (title, author))
        self.conn.commit()

    def update_books_listbox(self):
        self.listbox_books.delete(0, tk.END)
        for book in self.books:
            self.listbox_books.insert(tk.END, book)

    # Step 3: Add and Save User Details

    def setup_file(self):
        with open("book_details.txt", "a"):
            pass

    def add_user(self, name, contact):
        user_details = f"Name: {name}, Contact: {contact}"
        self.users.append(user_details)
        self.add_user_to_database(name, contact)  # Save user details to database
        self.add_user_to_file(name, contact)  # Save user details to file
        messagebox.showinfo("Success!! ", "User added successfully!")

    def add_user_to_database(self, name, contact):
        self.conn.execute("""
            INSERT INTO users (name, contact)
            VALUES (?, ?)
        """, (name, contact))
        self.conn.commit()

    def add_user_to_file(self, name, contact):
        with open("user_details.txt", "a") as file:
            file.write(f"Name: {name}, Contact: {contact}\n")

    def delete_user(self):
        selected_index = self.listbox_users.curselection()
        if selected_index:
            user_details = self.users.pop(selected_index[0])
            self.delete_user_from_database(user_details)  # Delete user details from database
            self.update_listbox_users()
            messagebox.showinfo("Success!! ", "User Deleted successfully!")

    def delete_user_from_database(self, user_details):
        name, contact = user_details.split(",")
        self.conn.execute("""
            DELETE FROM users
            WHERE name = ? AND contact = ?
        """, (name.split(": ")[1], contact.split(": ")[1]))
        self.conn.commit()

    def update_users_listbox(self):
        self.listbox_users.delete(0, tk.END)
        for user in self.users:
            self.listbox_users.insert(tk.END, user)


    # Step 3: Display User Details on Separate Window

    def show_user_details(self):
        if self.user_window is None:
            user_window = tk.Toplevel(self.root)
            user_window.title("User Details")
            user_window.geometry("500x500")

            label_user_title = tk.Label(user_window, text="User Details", font=("Helvetica", 16, "bold"))
            label_user_title.pack(pady=20)

            self.label_user_name = tk.Label(user_window, text="Name:")
            self.label_user_name.pack()

            self.entry_user_name = tk.Entry(user_window, width=30)
            self.entry_user_name.pack()

            self.label_user_contact = tk.Label(user_window, text="Contact Details:")
            self.label_user_contact.pack()

            self.entry_user_contact = tk.Entry(user_window, width=30)
            self.entry_user_contact.pack()

            button_add_user = tk.Button(user_window, text="Add User", command=self.add_user_from_details)
            button_add_user.pack(pady=20)

            button_add_user = tk.Button(user_window, text="Delete User", command=self.delete_user)
            button_add_user.pack(pady=20)

            self.listbox_users = tk.Listbox(user_window, width=40, height=8)
            self.listbox_users.pack()

            button_back_to_books = tk.Button(user_window, text="Back to Books", command=user_window.destroy)
            button_back_to_books.pack(pady=10)

            self.update_listbox_users()

    def close_user_window(self):
        self.user_window.destroy()
        self.user_window = None


    def update_listbox_users(self):
        self.listbox_users.delete(0, tk.END)
        for user in self.users:
            if isinstance(user, dict) and 'name' in user and 'contact' in user:
                name = user['name']
                contact = user['contact']
                self.listbox_users.insert(tk.END, f"Name: {name}, Contact: {contact}")
            else:
                print("Invalid user data:", user)


    def is_valid_contact(self, contact):
        # Assuming valid contact has 10 digits
        return contact.isdigit() and len(contact) == 10
    def add_user_from_details(self):
        name = self.entry_user_name.get()
        contact = self.entry_user_contact.get()

        if name and contact:
            if self.is_valid_contact(contact):
               self.add_user(name, contact)
               self.entry_user_name.delete(0, tk.END)
               self.entry_user_contact.delete(0, tk.END)
               self.update_users_listbox()
               messagebox.showinfo("Success!!", "User added Successfully!")
            else:
                 messagebox.showerror("Error", "Please enter a valid 10-digit contact number.")
        else:
             messagebox.showerror("Error", "Please enter both name and contact.")


        self.root.withdraw()



if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()
