from tkinter import messagebox
import csv

# Fungsi untuk menambahkan reservasi
def add_reservation(cursor, conn, guest_name, room_number, check_in_date, check_out_date, price):
    cursor.execute('''INSERT INTO reservations (guest_name, room_number, check_in_date, check_out_date, price)
                      VALUES (?, ?, ?, ?, ?)''', 
                   (guest_name, int(room_number), check_in_date, check_out_date, int(price)))
    conn.commit()
    messagebox.showinfo('Success', 'Reservation added successfully')

    # Kembalikan True untuk menandakan reservasi berhasil ditambahkan
    return True

# Fungsi untuk menghapus reservasi berdasarkan ID
def delete_reservation(cursor, conn, reservation_id):
    cursor.execute('DELETE FROM reservations WHERE id=?', (reservation_id,))
    conn.commit()
    messagebox.showinfo('Success', 'Reservation deleted successfully')

# Fungsi untuk mengekspor data reservasi ke dalam file CSV
def export_csv(cursor, file_path):
    cursor.execute('SELECT * FROM reservations')
    rows = cursor.fetchall()
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Guest Name', 'Room Number', 'Check-in Date', 'Check-out Date', 'Price'])
        for row in rows:
            writer.writerow(row)
    
    messagebox.showinfo('Success', 'Reservations exported successfully')
