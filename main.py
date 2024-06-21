import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import customtkinter as ctk
import csv
from database import initialize_database, close_database
from functions import add_reservation, delete_reservation, export_csv

# Inisialisasi koneksi database
conn, cursor = initialize_database()

# GUI menggunakan customtkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light")
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

root = ctk.CTk()
root.title('Hotel Reservations')
root.geometry('900x600')

frame = ctk.CTkFrame(root, width=850, height=550, corner_radius=15)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label_guest_name = ctk.CTkLabel(frame, text='Guest Name:')
label_guest_name.grid(row=0, column=0, sticky=tk.W, pady=5, padx=10)
entry_guest_name = ctk.CTkEntry(frame, width=250)
entry_guest_name.grid(row=0, column=1, sticky=tk.W, pady=5, padx=10)

label_room_number = ctk.CTkLabel(frame, text='Room Number:')
label_room_number.grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)
entry_room_number = ctk.CTkEntry(frame, width=250)
entry_room_number.grid(row=1, column=1, sticky=tk.W, pady=5, padx=10)

label_check_in_date = ctk.CTkLabel(frame, text='Check-in Date:')
label_check_in_date.grid(row=2, column=0, sticky=tk.W, pady=5, padx=10)
entry_check_in_date = DateEntry(frame, width=22, background='darkblue', foreground='white', borderwidth=2)
entry_check_in_date.grid(row=2, column=1, sticky=tk.W, pady=5, padx=10)

label_check_out_date = ctk.CTkLabel(frame, text='Check-out Date:')
label_check_out_date.grid(row=3, column=0, sticky=tk.W, pady=5, padx=10)
entry_check_out_date = DateEntry(frame, width=22, background='darkblue', foreground='white', borderwidth=2)
entry_check_out_date.grid(row=3, column=1, sticky=tk.W, pady=5, padx=10)

# Posisikan tombol check-in dan check-out di kiri dan kanan
button_add = ctk.CTkButton(frame, text='Add Reservation', command=lambda: add_reservation_clicked())
button_add.grid(row=4, column=0, pady=10, padx=10, sticky='ew')

button_delete = ctk.CTkButton(frame, text='Delete Reservation', command=lambda: delete_reservation_clicked())
button_delete.grid(row=4, column=1, pady=10, padx=10, sticky='ew')

# Tombol untuk ekspor CSV
button_export = ctk.CTkButton(frame, text='Export CSV', command=lambda: export_csv_clicked())
button_export.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky='ew')

# Gunakan ttk Treeview untuk menampilkan data reservasi
tree_frame = ctk.CTkFrame(frame)
tree_frame.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

columns = ('ID', 'Guest Name', 'Room Number', 'Check-in Date', 'Check-out Date')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
tree.pack(fill="both", expand=True)

tree.heading('ID', text='ID')
tree.heading('Guest Name', text='Guest Name')
tree.heading('Room Number', text='Room Number')
tree.heading('Check-in Date', text='Check-in Date')
tree.heading('Check-out Date', text='Check-out Date')

tree.column('ID', width=50, anchor='center')
tree.column('Guest Name', width=150, anchor='center')
tree.column('Room Number', width=100, anchor='center')
tree.column('Check-in Date', width=100, anchor='center')
tree.column('Check-out Date', width=100, anchor='center')

# Fungsi untuk menampilkan data reservasi saat aplikasi dimulai
def display_reservations():
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute('SELECT * FROM reservations')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', tk.END, values=row)  # Pastikan ada import 'tk' di atas jika menggunakan 'tk.END'

# Fungsi untuk menangani klik tombol "Add Reservation"
def add_reservation_clicked():
    guest_name = entry_guest_name.get()
    room_number = entry_room_number.get()
    check_in_date = entry_check_in_date.get()
    check_out_date = entry_check_out_date.get()

    # Validasi input (contoh sederhana, sesuaikan dengan kebutuhan Anda)
    if guest_name and room_number and check_in_date and check_out_date:
        if add_reservation(cursor, conn, guest_name, room_number, check_in_date, check_out_date):
            display_reservations()
            # Bersihkan input setelah reservasi ditambahkan
            entry_guest_name.delete(0, tk.END)
            entry_room_number.delete(0, tk.END)
            entry_check_in_date.delete(0, tk.END)
            entry_check_out_date.delete(0, tk.END)
    else:
        messagebox.showwarning('Input Error', 'Please fill in all fields.')

# Fungsi untuk menangani klik tombol "Delete Reservation"
def delete_reservation_clicked():
    selected_item = tree.selection()
    if selected_item:
        reservation_id = tree.item(selected_item)['values'][0]
        delete_reservation(cursor, conn, reservation_id)
        display_reservations()
    else:
        messagebox.showwarning('Selection Error', 'Please select a reservation to delete.')

# Fungsi untuk menangani klik tombol "Export CSV"
def export_csv_clicked():
    export_csv(cursor, 'reservations.csv')

# Panggil fungsi saat aplikasi dimulai
display_reservations()

root.mainloop()

# Tutup koneksi database saat aplikasi ditutup
close_database(conn)
