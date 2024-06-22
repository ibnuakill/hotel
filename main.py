import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
from functions import initialize_database, close_database, add_reservation_clicked, delete_reservation_clicked, export_csv_clicked, display_reservations, search_reservation, create_circle_image

# Inisialisasi koneksi database
conn, cursor = initialize_database()

# GUI menggunakan customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title('Hotel Reservations')
root.geometry('900x600')

frame = ctk.CTkFrame(root, width=850, height=550, corner_radius=15)
frame.pack(pady=20, padx=20, fill="both", expand=True)

for i in range(4):
    frame.grid_columnconfigure(i, weight=1)

logo_path = "images/hotel-1.png"
logo_image = create_circle_image(logo_path, 70)

if logo_image:
    logo_label = tk.Label(frame, image=logo_image)
    logo_label.image = logo_image
    logo_label.grid(row=0, column=3, rowspan=2, padx=10, pady=10, sticky='nsew')

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

entry_check_in_time = ctk.CTkFrame(frame)
entry_check_in_time.grid(row=2, column=2, sticky=tk.W, pady=5, padx=10)
hour_in = tk.Spinbox(entry_check_in_time, from_=0, to=23, width=2, format="%02.0f")
minute_in = tk.Spinbox(entry_check_in_time, from_=0, to=59, width=2, format="%02.0f")
second_in = tk.Spinbox(entry_check_in_time, from_=0, to=59, width=2, format="%02.0f")
hour_in.pack(side=tk.LEFT)
minute_in.pack(side=tk.LEFT)
second_in.pack(side=tk.LEFT)

label_check_out_date = ctk.CTkLabel(frame, text='Check-out Date:')
label_check_out_date.grid(row=3, column=0, sticky=tk.W, pady=5, padx=10)
entry_check_out_date = DateEntry(frame, width=38, background='darkblue', foreground='white', borderwidth=2)
entry_check_out_date.grid(row=3, column=1, sticky=tk.W, pady=5, padx=10)

entry_check_out_time = ctk.CTkFrame(frame)
entry_check_out_time.grid(row=3, column=2, sticky=tk.W, pady=5, padx=10)
hour_out = tk.Spinbox(entry_check_out_time, from_=0, to=23, width=2, format="%02.0f")
minute_out = tk.Spinbox(entry_check_out_time, from_=0, to=59, width=2, format="%02.0f")
second_out = tk.Spinbox(entry_check_out_time, from_=0, to=59, width=2, format="%02.0f")
hour_out.pack(side=tk.LEFT)
minute_out.pack(side=tk.LEFT)
second_out.pack(side=tk.LEFT)

label_price = ctk.CTkLabel(frame, text='Price:')
label_price.grid(row=4, column=0, sticky=tk.W, pady=5, padx=10)
entry_price = ctk.CTkEntry(frame, width=250)
entry_price.grid(row=4, column=1, sticky=tk.W, pady=5, padx=10, columnspan=2)

button_add = ctk.CTkButton(frame, text='Add Reservation', command=lambda: add_reservation_clicked(cursor, conn, tree, {
    'guest_name': entry_guest_name,
    'room_number': entry_room_number,
    'check_in_date': entry_check_in_date,
    'hour_in': hour_in,
    'minute_in': minute_in,
    'second_in': second_in,
    'check_out_date': entry_check_out_date,
    'hour_out': hour_out,
    'minute_out': minute_out,
    'second_out': second_out,
    'price': entry_price
}))
button_add.grid(row=5, column=0, pady=10, padx=10)

button_delete = ctk.CTkButton(frame, text='Delete Reservation', command=lambda: delete_reservation_clicked(cursor, conn, tree))
button_delete.grid(row=5, column=1, pady=10, padx=10)

button_export = ctk.CTkButton(frame, text='Export to CSV', command=lambda: export_csv_clicked(cursor))
button_export.grid(row=5, column=2, pady=10, padx=10)

label_search = ctk.CTkLabel(frame, text='Cari Data:')
label_search.grid(row=6, column=0, sticky=tk.W, pady=5, padx=10)
entry_search = ctk.CTkEntry(frame, width=200)
entry_search.grid(row=6, column=1, pady=10, padx=10)
search_criteria = ctk.CTkComboBox(frame, values=['Guest Name', 'Room Number'], state='readonly')
search_criteria.grid(row=6, column=2, pady=10, padx=10)
search_criteria.set('Guest Name')

button_search = ctk.CTkButton(frame, text='Search', command=lambda: search_reservation(cursor, tree, entry_search.get(), search_criteria.get()))
button_search.grid(row=6, column=3, pady=10, padx=10)

# Frame untuk treeview dan scrollbar
tree_frame = ctk.CTkFrame(frame)
tree_frame.grid(row=7, column=0, columnspan=4, pady=20, padx=20, sticky="nsew")

# Scrollbar horizontal
tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

# Scrollbar vertikal
tree_scroll_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

columns = ('ID', 'Guest Name', 'Room Number', 'Check-in Date', 'Check-out Date', 'Price')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor='center')

tree.pack(fill="both", expand=True)

# Konfigurasi scrollbar
tree_scroll_x.config(command=tree.xview)
tree_scroll_y.config(command=tree.yview)

display_reservations(cursor, tree)

def on_closing():
    close_database(conn)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()