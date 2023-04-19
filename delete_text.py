import sqlite3

def main():

    name = input("Name: ").strip()

    con = sqlite3.connect("error_corpus.db")
    cur = con.cursor()

    res = cur.execute("SELECT id, name FROM student WHERE name LIKE ?", (name,)).fetchall()
    print(*res)
    if not res: 
        print("Nothing found")
        flag = input("Do you want to continue? (yes/no): ")
        if flag.lower().strip() == "no": 
            return

    try:
        student_id = int(input("Text id: "))
    except ValueError:
        print("id is int")
        return

    err = cur.execute("DELETE FROM error WHERE phrase_id in (SELECT id FROM phrase WHERE student_id = ?);", (student_id,))
    err = cur.execute("DELETE FROM phrase WHERE student_id = ?;", (student_id,))
    err = cur.execute("DELETE FROM student WHERE id = ?;", (student_id,))

    con.commit()
    con.close()


if __name__ == "__main__":
    main()