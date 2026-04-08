import sqlite3

# connect database
conn = sqlite3.connect("assignment.db")
cursor = conn.cursor()

# -----------------------
# CREATE TABLES
# -----------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id TEXT,
    booking_date TEXT,
    room_no TEXT,
    user_id TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    item_id TEXT,
    item_name TEXT,
    item_rate INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS booking_commercials (
    id TEXT,
    booking_id TEXT,
    bill_id TEXT,
    bill_date TEXT,
    item_id TEXT,
    item_quantity REAL
)
""")

# -----------------------
# INSERT SAMPLE DATA
# -----------------------

cursor.execute("DELETE FROM users")
cursor.execute("DELETE FROM bookings")
cursor.execute("DELETE FROM items")
cursor.execute("DELETE FROM booking_commercials")

cursor.execute("INSERT INTO users VALUES ('u1','John')")
cursor.execute("INSERT INTO users VALUES ('u2','Alice')")

cursor.execute("INSERT INTO bookings VALUES ('b1','2021-11-10','101','u1')")
cursor.execute("INSERT INTO bookings VALUES ('b2','2021-10-05','102','u2')")

cursor.execute("INSERT INTO items VALUES ('i1','Paratha',20)")
cursor.execute("INSERT INTO items VALUES ('i2','Veg Curry',80)")

cursor.execute("INSERT INTO booking_commercials VALUES ('c1','b1','bill1','2021-11-10','i1',5)")
cursor.execute("INSERT INTO booking_commercials VALUES ('c2','b2','bill2','2021-10-05','i2',20)")

# -----------------------
# SQL QUERIES (HOTEL)
# -----------------------

# Q1
print("\nQ1: Last booked room:")
for row in cursor.execute("""
SELECT user_id, room_no
FROM bookings
ORDER BY booking_date DESC
LIMIT 1
"""):
    print(row)

# Q2
print("\nQ2: Billing November 2021:")
for row in cursor.execute("""
SELECT booking_id, SUM(item_quantity * item_rate)
FROM booking_commercials bc
JOIN items i ON bc.item_id = i.item_id
WHERE bill_date LIKE '2021-11%'
GROUP BY booking_id
"""):
    print(row)

# Q3
print("\nQ3: Bills >1000 in October 2021:")
for row in cursor.execute("""
SELECT bill_id, SUM(item_quantity * item_rate) as total
FROM booking_commercials bc
JOIN items i ON bc.item_id = i.item_id
WHERE bill_date LIKE '2021-10%'
GROUP BY bill_id
HAVING total > 1000
"""):
    print(row)

# Q4
print("\nQ4: Most ordered item:")
for row in cursor.execute("""
SELECT item_id, SUM(item_quantity) as total_qty
FROM booking_commercials
GROUP BY item_id
ORDER BY total_qty DESC
LIMIT 1
"""):
    print(row)

# Q5
print("\nQ5: Second highest bill:")
for row in cursor.execute("""
SELECT bill_id, total FROM (
    SELECT bill_id, SUM(item_quantity * item_rate) as total
    FROM booking_commercials bc
    JOIN items i ON bc.item_id = i.item_id
    GROUP BY bill_id
    ORDER BY total DESC
    LIMIT 2
) ORDER BY total ASC LIMIT 1
"""):
    print(row)

# -----------------------
# PYTHON TASKS
# -----------------------

# Time Converter (Improved)
print("\nPython Task 1: Time Converter")

def convert_minutes(minutes):
    hours = minutes // 60
    remaining = minutes % 60

    if hours == 1:
        print(f"{hours} hr {remaining} minutes")
    else:
        print(f"{hours} hrs {remaining} minutes")

convert_minutes(130)
convert_minutes(110)

# Remove Duplicates
print("\nPython Task 2: Remove Duplicates")

def remove_duplicates(s):
    result = ""
    for char in s:
        if char not in result:
            result += char
    print(result)

remove_duplicates("programming")

# -----------------------

conn.commit()
conn.close()