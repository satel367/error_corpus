import sqlite3
import csv

def main():

    try:
        con = sqlite3.connect('error_corpus.db')
        cur = con.cursor()
    except e:
        print("not opened")

    print("Opened database successfully")

    with open("Tags.csv") as f:
        # Create D(f)ictReader
        reader = csv.DictReader(f)

        # Iterate over CSV file, printing each favorite
        for row in reader:
            cur.execute(f"INSERT INTO tags (id, tag) VALUES ({row['id']}, \"{row['tag']}\");")
        con.commit()
        
    
    print(cur.execute("SELECT * FROM tags;"))

    con.close()



if __name__ == "__main__":
    main()