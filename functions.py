import os
from tkinter import messagebox
import csv
import sqlite3
from tkcalendar import DateEntry
from PIL import Image, ImageTk, ImageDraw

# Fungsi untuk inisialisasi dan menutup koneksi database
def initialize_database():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservations
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       guest_name TEXT NOT NULL,
                       room_number INTEGER NOT NULL,
                       check_in_date TEXT NOT NULL,
                       check_out_date TEXT NOT NULL,
                       price INTEGER NOT NULL)''')
    conn.commit()
    return conn, cursor

def close_database(conn):
    conn.close()

# Fungsi untuk menambahkan reservasi
def add_reservation(cursor, conn, guest_name, room_number, check_in_date, check_out_date, price):
    try:
        cursor.execute('''INSERT INTO reservations (guest_name, room_number, check_in_date, check_out_date, price)
                          VALUES (?, ?, ?, ?, ?)''', 
                       (guest_name, int(room_number), check_in_date, check_out_date, int(price)))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding reservation: {e}")
        return False

# Fungsi untuk menghapus reservasi berdasarkan ID
def delete_reservation(cursor, conn, reservation_id):
    try:
        cursor.execute('DELETE FROM reservations WHERE id=?', (reservation_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting reservation: {e}")
        return False

# Fungsi untuk mengekspor data reservasi ke dalam file CSV
def export_csv(cursor, file_path):
    try:
        cursor.execute('SELECT * FROM reservations')
        rows = cursor.fetchall()

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Guest Name', 'Room Number', 'Check-in Date', 'Check-out Date', 'Price'])
            for row in rows:
                writer.writerow(row)

        return True
    except Exception as e:
        print(f"Error exporting CSV: {e}")
        return False

# Fungsi untuk membuat gambar menjadi lingkaran
def create_circle_image(image_path, size):
    try:
        logo_image = Image.open(image_path)
        logo_image = logo_image.resize((size, size))

        circle_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))

        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        circle_image.paste(logo_image, (0, 0), mask)

        return ImageTk.PhotoImage(circle_image)

    except FileNotFoundError:
        messagebox.showerror("Error", f"Logo image not found at {image_path}.")
        return None

# Fungsi untuk menampilkan data reservasi saat aplikasi dimulai
def display_reservations(cursor, tree):
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute('SELECT * FROM reservations')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)

# Fungsi untuk menangani klik tombol "Add Reservation"
def add_reservation_clicked(cursor, conn, tree, entries):
    guest_name = entries['guest_name'].get()
    room_number = entries['room_number'].get()
    check_in_date = entries['check_in_date'].get()
    check_in_time = f"{entries['hour_in'].get()}:{entries['minute_in'].get()}:{entries['second_in'].get()}"
    check_out_date = entries['check_out_date'].get()
    check_out_time = f"{entries['hour_out'].get()}:{entries['minute_out'].get()}:{entries['second_out'].get()}"
    price = entries['price'].get()

    if guest_name and room_number and check_in_date and check_in_time and check_out_date and check_out_time and price:
        full_check_in_date = f"{check_in_date} {check_in_time}"
        full_check_out_date = f"{check_out_date} {check_out_time}"
        
        if add_reservation(cursor, conn, guest_name, room_number, full_check_in_date, full_check_out_date, price):
            display_reservations(cursor, tree)
            messagebox.showinfo("Success", "Reservation added successfully.")
            
            for entry in entries.values():
                entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Failed to add reservation.")
    else:
        messagebox.showerror("Error", "All fields are required.")

# Fungsi untuk menangani klik tombol "Delete Reservation"
def delete_reservation_clicked(cursor, conn, tree):
    selected_item = tree.selection()
    if selected_item:
        reservation_id = tree.item(selected_item)['values'][0]
        if delete_reservation(cursor, conn, reservation_id):
            display_reservations(cursor, tree)
            messagebox.showinfo("Success", "Reservation deleted successfully.")
        else:
            messagebox.showerror("Error", "Failed to delete reservation.")
    else:
        messagebox.showerror("Error", "No reservation selected.")

# Fungsi untuk menangani klik tombol "Export CSV"
def export_csv_clicked(cursor):
    file_path = os.path.join(os.getcwd(), 'reservation.csv')
    if export_csv(cursor, file_path):
        messagebox.showinfo("Success", f"Data exported to {file_path} successfully.")
    else:
        messagebox.showerror("Error", "Failed to export data to CSV.")

# Fungsi untuk menangani pencarian reservasi
def search_reservation(cursor, tree, search_term, search_type):
    query = f"SELECT * FROM reservations WHERE {search_type.lower().replace(' ', '_')} LIKE ?"
    cursor.execute(query, ('%' + search_term + '%',))
    rows = cursor.fetchall()
    
    for i in tree.get_children():
        tree.delete(i)
    for row in rows:
        tree.insert('', 'end', values=row)
