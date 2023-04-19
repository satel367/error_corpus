import sqlite3
import csv

def main():

    try:
        con = sqlite3.connect('error_corpus.db')
        cur = con.cursor()
    except e:
        print("not opened")

    print("Opened database successfully")

    with open("Phrases.csv") as f:
        # Create D(f)ictReader
        reader = csv.DictReader(f)

        # Iterate over CSV file, printing each favorite
        for row in reader:
            cur.execute(f"INSERT INTO phrases (id, phrase, tag_id) VALUES ({row['id']}, \"{row['phrase']}\", (SELECT id FROM tags WHERE tag = \"{row['tag']}\"));")
        con.commit()
        
    
    res = cur.execute("SELECT * FROM tags;")
    res.fetchall()

    con.close()



if __name__ == "__main__":
    main()