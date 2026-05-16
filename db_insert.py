import sqlite3
# from rows import rows


conn = sqlite3.connect("base.db")
cursor = conn.cursor()



for i, row in enumerate(rows, start=1):
    cursor.execute("""
        INSERT INTO simplemaps_worldcities_basic
        (
            index_no,
            city,
            city_ascii,
            lat,
            lng,
            country,
            iso2,
            iso3,
            admin_name,
            capital,
            population,
            id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)

    if i % 400 == 0:
        conn.commit()
        print(f"Commit po {i} rekordach")

# commit końcowy
conn.commit()

conn.close()
