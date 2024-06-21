import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import customtkinter as ctk
from PIL import Image, ImageTk
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

# Adjust column configurations for better alignment
for i in range(4):
    frame.grid_columnconfigure(i, weight=1)

# Path ke file gambar logo hotel
logo_path = "images/hotel.png"

# Buat frame untuk gambar
image_frame = ctk.CTkFrame(frame, width=150, height=150)
image_frame.grid(row=0, column=3, rowspan=2, padx=10, pady=10)

# Muat gambar menggunakan PIL
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((150, 150), Image.ANTIALIAS)
logo_image = ImageTk.PhotoImage(logo_image)

# Tampilkan gambar di frame
logo_label = tk.Label(image_frame, image=logo_image)
logo_label.pack()


label_guest_name = ctk.CTkLabel(frame, text='Guest Name:')
label_guest_name.grid(row=0, column=0, sticky=tk.W, pady=5, padx=10)
entry_guest_name = ctk.CTkEntry(frame, width=250)
entry_guest_name.grid(row=0, column=1, sticky=tk.W, pady=5, padx=10, columnspan=2)

label_room_number = ctk.CTkLabel(frame, text='Room Number:')
label_room_number.grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)
entry_room_number = ctk.CTkEntry(frame, width=250)
entry_room_number.grid(row=1, column=1, sticky=tk.W, pady=5, padx=10, columnspan=2)

label_check_in_date = ctk.CTkLabel(frame, text='Check-in Date:')
label_check_in_date.grid(row=2, column=0, sticky=tk.W, pady=5, padx=10)
entry_check_in_date = DateEntry(frame, width=38, background='darkblue', foreground='white', borderwidth=2)
entry_check_in_date.grid(row=2, column=1, sticky=tk.W, pady=5, padx=10)

# Frame waktu check-in
entry_check_in_time = ctk.CTkFrame(frame)
entry_check_in_time.grid(row=2, column=2, sticky=tk.W, pady=5, padx=10)
hour_in = tk.Spinbox(entry_check_in_time, from_=0, to=23, width=2, format="%02.0f")
minute_in = tk.Spinbox(entry_check_in_time, from_=0, to=59, width=2, format="%02.0f")
second_in = tk.Spinbox(entry_check_in_time, from_=0, to=59, width=2, format="%02.0f")
hour_in.pack(side='left')
minute_in.pack(side='left')
second_in.pack(side='left')

label_check_out_date = ctk.CTkLabel(frame, text='Check-out Date:')
label_check_out_date.grid(row=3, column=0, sticky=tk.W, pady=5, padx=10)
entry_check_out_date = DateEntry(frame, width=38, background='darkblue', foreground='white', borderwidth=2)
entry_check_out_date.grid(row=3, column=1, sticky=tk.W, pady=5, padx=10)

# Frame waktu check-out
entry_check_out_time = ctk.CTkFrame(frame)
entry_check_out_time.grid(row=3, column=2, sticky=tk.W, pady=5, padx=10)
hour_out = tk.Spinbox(entry_check_out_time, from_=0, to=23, width=2, format="%02.0f")
minute_out = tk.Spinbox(entry_check_out_time, from_=0, to=59, width=2, format="%02.0f")
second_out = tk.Spinbox(entry_check_out_time, from_=0, to=59, width=2, format="%02.0f")
hour_out.pack(side='left')
minute_out.pack(side='left')
second_out.pack(side='left')

label_price = ctk.CTkLabel(frame, text='Price:')
label_price.grid(row=4, column=0, sticky=tk.W, pady=5, padx=10)
entry_price = ctk.CTkEntry(frame, width=250)
entry_price.grid(row=4, column=1, sticky=tk.W, pady=5, padx=10, columnspan=2)

# Tambahkan entri pencarian dan tombol di bawah entry_guest_name
label_search = ctk.CTkLabel(frame, text='Search:')
label_search.grid(row=5, column=0, sticky=tk.W, pady=5, padx=10)

entry_search = ctk.CTkEntry(frame, width=250)
entry_search.grid(row=5, column=1, sticky=tk.W, pady=5, padx=10)

# Tambahkan dropdown untuk memilih jenis pencarian
search_options = ['Guest Name', 'Room Number']
search_var = tk.StringVar(value=search_options[0])
search_dropdown = ctk.CTkOptionMenu(frame, variable=search_var, values=search_options)
search_dropdown.grid(row=5, column=2, pady=5, padx=10, sticky='ew')

button_search = ctk.CTkButton(frame, text='Search', command=lambda: search_reservation())
button_search.grid(row=5, column=3, pady=10, padx=10, sticky='ew')

# Posisikan tombol check-in dan check-out di kiri dan kanan
button_add = ctk.CTkButton(frame, text='Add Reservation', command=lambda: add_reservation_clicked())
button_add.grid(row=6, column=0, pady=10, padx=10, sticky='ew', columnspan=2)

button_delete = ctk.CTkButton(frame, text='Delete Reservation', command=lambda: delete_reservation_clicked())
button_delete.grid(row=6, column=2, pady=10, padx=10, sticky='ew', columnspan=2)

# Tombol untuk ekspor CSV
button_export = ctk.CTkButton(frame, text='Export CSV', command=lambda: export_csv_clicked())
button_export.grid(row=7, column=0, columnspan=4, pady=10, padx=10, sticky='ew')

# Gunakan ttk Treeview untuk menampilkan data reservasi
tree_frame = ctk.CTkFrame(frame)
tree_frame.grid(row=8, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")

columns = ('ID', 'Guest Name', 'Room Number', 'Check-in Date', 'Check-out Date', 'Price')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
tree.pack(fill="both", expand=True)

tree.heading('ID', text='ID')
tree.heading('Guest Name', text='Guest Name')
tree.heading('Room Number', text='Room Number')
tree.heading('Check-in Date', text='Check-in Date')
tree.heading('Check-out Date', text='Check-out Date')
tree.heading('Price', text='Price')

tree.column('ID', width=50, anchor='center')
tree.column('Guest Name', width=150, anchor='center')
tree.column('Room Number', width=100, anchor='center')
tree.column('Check-in Date', width=150, anchor='center')
tree.column('Check-out Date', width=150, anchor='center')
tree.column('Price', width=100, anchor='center')

# Fungsi untuk menampilkan data reservasi saat aplikasi dimulai
def display_reservations():
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute('SELECT * FROM reservations')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', tk.END, values=row)

# Fungsi untuk menangani klik tombol "Add Reservation"
def add_reservation_clicked():
    guest_name = entry_guest_name.get()
    room_number = entry_room_number.get()
    check_in_date = entry_check_in_date.get()
    check_in_time = f"{hour_in.get()}:{minute_in.get()}:{second_in.get()}"
    check_out_date = entry_check_out_date.get()
    check_out_time = f"{hour_out.get()}:{minute_out.get()}:{second_out.get()}"
    price = entry_price.get()

    # Validasi input (contoh sederhana, sesuaikan dengan kebutuhan Anda)
    if guest_name and room_number and check_in_date and check_in_time and check_out_date and check_out_time and price:
        full_check_in_date = f"{check_in_date} {check_in_time}"
        full_check_out_date = f"{check_out_date} {check_out_time}"
        if add_reservation(cursor, conn, guest_name, room_number, full_check_in_date, full_check_out_date, price):
            display_reservations()
            # Bersihkan input setelah reservasi ditambahkan
            entry_guest_name.delete(0, tk.END)
            entry_room_number.delete(0, tk.END)
            entry_check_in_date.set_date('')
            hour_in.delete(0, tk.END)
            minute_in.delete(0, tk.END)
            second_in.delete(0, tk.END)
            entry_check_out_date.set_date('')
            hour_out.delete(0, tk.END)
            minute_out.delete(0, tk.END)
            second_out.delete(0, tk.END)
            entry_price.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to add reservation.")
    else:
        messagebox.showerror("Error", "All fields are required.")

# Fungsi untuk menangani klik tombol "Delete Reservation"
def delete_reservation_clicked():
    selected_item = tree.selection()
    if selected_item:
        reservation_id = tree.item(selected_item)['values'][0]
        if delete_reservation(cursor, conn, reservation_id):
            display_reservations()
        else:
            messagebox.showerror("Error", "Failed to delete reservation.")
    else:
        messagebox.showerror("Error", "No reservation selected.")

# Fungsi untuk menangani klik tombol "Export CSV"
def export_csv_clicked():
    file_path = os.path.join(os.getcwd(), 'reservation.csv')
    if export_csv(cursor, file_path):
        messagebox.showinfo("Success", f"Data exported to {file_path} successfully.")
    # else:
    #     messagebox.showerror("Error", "Failed to export data to CSV.")

# Fungsi untuk menangani pencarian reservasi
def search_reservation():
    search_term = entry_search.get()
    search_type = search_var.get()
    
    query = f"SELECT * FROM reservations WHERE {search_type.lower().replace(' ', '_')} LIKE ?"
    cursor.execute(query, ('%' + search_term + '%',))
    rows = cursor.fetchall()
    
    for i in tree.get_children():
        tree.delete(i)
    for row in rows:
        tree.insert('', tk.END, values=row)

# Tampilkan data reservasi saat aplikasi dimulai
display_reservations()

# Tutup koneksi database saat aplikasi ditutup
def on_closing():
    close_database(conn)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()