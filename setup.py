import sqlite3

conn = sqlite3.connect('movies.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS bookings")
c.execute("DROP TABLE IF EXISTS seats")
c.execute("DROP TABLE IF EXISTS showtimes")
c.execute("DROP TABLE IF EXISTS movies")

c.execute("""
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    duration INTEGER,
    description TEXT,
    price REAL NOT NULL
)
""")

c.execute("""
CREATE TABLE showtimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    date TEXT,
    timeslot TEXT,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
)
""")

c.execute("""
CREATE TABLE seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    showtime_id INTEGER,
    seat_number TEXT,
    available INTEGER DEFAULT 1,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id)
)
""")

c.execute("""
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    showtime_id INTEGER,
    seat_number TEXT,
    user_name TEXT,
    user_email TEXT,
    user_phone TEXT,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id)
)
""")

movies = [
    ("Lokah: Chapter 1", "now_showing", 180, "A sci-fi adventure kicking off a new saga.",190),
    ("Vala: Story Of A Bangle", "now_showing", 175, "A fantasy epic filled with battles and betrayals",175),
    ("Balti", "now_showing", 150, "A heartfelt family story set in the mountains.",165),
    ("Vilayath Buddha", "coming_soon", 150, "action drama film",180),
]

c.executemany("INSERT INTO movies (title, status, duration, description, price) VALUES (?,?,?,?,?)", movies)
conn.commit()


showtimes = [
    (1, "2025-10-07", "10:00 AM"),
    (1, "2025-10-07", "1:00 PM"),
    (2, "2025-10-07", "11:00 AM"),
    (2, "2025-10-07", "2:00 PM"),
    (3, "2025-10-07", "10:00 AM"),
    (3, "2025-10-07", "2:00 PM"),
]

c.executemany("INSERT INTO showtimes (movie_id, date, timeslot) VALUES (?,?,?)", showtimes)
conn.commit()

rows = ['A','B','C','D','E','F']  #...
cols = range(1, 9)  # 1 to 8
#for each showtime insert the seats

for st in showtimes:
    show_id = st[0]  # get the first element of the tuple
    for row in rows:
        for col in cols:
            seat_number = f"{row}{col}"
            c.execute("INSERT INTO seats (showtime_id, seat_number, available) VALUES (?,?,1)", (show_id, seat_number))

conn.commit()
conn.close()

print("Database setup completed successfully!")
