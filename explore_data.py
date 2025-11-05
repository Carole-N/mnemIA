import sqlite3

def explore_database(db_path):
    """
    Explore the SQLite database and display data by source.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # List all tables
            print("\n--- Tables in the database ---")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                print(table["name"])

            # Display data from poetic_inspiration grouped by source
            print("\n--- Data grouped by source (poetic_inspiration) ---")
            cursor.execute("SELECT source, COUNT(*) as count FROM poetic_inspiration GROUP BY source;")
            rows = cursor.fetchall()
            for row in rows:
                print(f"Source: {row['source']}, Count: {row['count']}")

            # Display a sample of data
            print("\n--- Sample data from poetic_inspiration ---")
            cursor.execute("SELECT * FROM poetic_inspiration LIMIT 10;")
            sample_rows = cursor.fetchall()
            for row in sample_rows:
                print(dict(row))

    except sqlite3.Error as e:
        print(f"Error accessing the database: {e}")

if __name__ == "__main__":
    db_path = "storage/mnemia.sqlite"
    print(f"Exploring database at: {db_path}")
    explore_database(db_path)