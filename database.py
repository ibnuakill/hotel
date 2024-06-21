import sqlite3

# Fungsi untuk menginisialisasi koneksi ke database SQLite
def initialize_database():
    conn = sqlite3.connect('hotel_reservations.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservations
                      (id INTEGER PRIMARY KEY, guest_name TEXT, room_number INTEGER,
                       check_in_date TEXT, check_out_date TEXT, price INTEGER)''')
    conn.commit()
    
    # Periksa dan tambahkan kolom 'price' jika belum ada
    cursor.execute("PRAGMA table_info(reservations)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'price' not in columns:
        cursor.execute('ALTER TABLE reservations ADD COLUMN price INTEGER')
        conn.commit()

    return conn, cursor

# Fungsi untuk menutup koneksi database
def close_database(conn):
    conn.close()
