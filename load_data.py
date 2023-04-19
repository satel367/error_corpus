import os
import sqlite3
import re
import os
import shutil

def main():

    d = os.path.join("data", "to_load")
    files = os.listdir(d)

    if not files:
        print("There're no texts to upload")
        return

    for filename in files:
        print(f"parsing {filename}...")
        text, student_id = load_text(os.path.join(d, filename))
        parse_text(text, student_id)
        shutil.move(os.path.join(d, filename), os.path.join("data", "loaded", filename))

    print("upload completed") # TODO: check spelling
    


def load_text(filename):

    with open(filename) as f:
        lines = f.readlines()

    name = lines[0].rstrip()
    level = lines[1].rstrip()
    sim_num = int(lines[2]) if lines[2].rstrip() else None
    text = "".join(lines[3:])

    con = sqlite3.connect("error_corpus.db")
    cur = con.cursor()

    t = cur.execute(
        "INSERT INTO student (name, level, simulation, text) VALUES (?, ?, ?, ?)",
        (name, level, sim_num, text),
    )
    student_id = t.lastrowid
    con.commit()

    con.close()

    return text, student_id


def parse_text(text, student_id):
    """
    TODO

    phrase: (?:<((?:[A-z-]*? ?)*?)>)
    [tag];[error_type]_[comment(option)]: (?:(?:\[(?:\w*(?: \w)*)\](?: ?; ?\[(?:\w*(?: \w)*)\](?: ?_ ?\[(?:\w*(?: \w)*)\])?)?))
    error_type:
    comment:
    all: ((?:<(?:(?:[A-z-]*? ?)*?)>) ?(?:(?:\[(?:\w*(?: \w)*)\](?: ?; ?\[(?:\w*(?: \w)*)\](?: ?_ ?\[(?:\w*(?: \w)*)\])?)?))(?: ?\/ ?(?:(?:\[(?:\w*(?: \w)*)\](?: ?; ?\[(?:\w*(?: \w)*)\](?: ?_ ?\[(?:\w*(?: \w)*)\])?)?)))?)
    """

    phrases = re.findall(
        r"((?:<(?:(?:[A-z-',!?.:—;%\d*]*? ?)*?)>) ?(?:(?:\[(?:[\w\\]*(?: \w*)*)\](?: ?; ?\[(?:[\w\\]*(?: [\w\\]*)*)\](?: ?_ ?\[(?:\w*(?: \w*)*)\])?)?)(?:\{[1-3]\})?)(?: ?\/ ?(?:(?:\[(?:\w*(?: \w*)*)\](?: ?; ?\[(?:\w*(?: \w*)*)\](?: ?_ ?\[(?:\w*(?: \w*)*)\])?)?))(?:\{[1-3]\})?)*)",
        text,
    )

    for ph in phrases:
        phrase = re.findall(r"(?:<(?:(?:[A-z-',!?.:—;%\d*]*? ?)*?)>)", ph)[0]

        arr = re.findall(
            r"((?:(?:\[(?:[\w\/]*(?: \w*)*)\](?: ?; ?\[(?:[\w\\]*(?: [\w\\]*)*)\](?: ?_ ?\[(?:\w*(?: \w*)*)\])?)?)(?:\{[1-3]\})?)(?: ?\/ ?(?:(?:\[(?:\w*(?: \w*)*)\](?: ?; ?\[(?:\w*(?: \w*)*)\](?: ?_ ?\[(?:\w*(?: \w*)*)\])?)?))(?:\{[1-3]\})?)*)",
            ph,
        )[0].split("/")

        for el in arr:

            tag, err_type, comment, weight = re.findall(
                r"(?:(?:\[([\w\/]*(?: \w*)*)\](?: ?; ?\[([\w\\]*(?: [\w\\]*)*)\](?: ?_ ?\[(\w*(?: \w*)*)\])?)?)(?:\{([1-3])\})?)",
                el
            )[0]
            

            write_phrase(student_id, phrase, tag, err_type, comment, weight)


def write_phrase(student_id, phrase, tag, err_type, comment, weight):
    con = sqlite3.connect("error_corpus.db")
    cur = con.cursor()

    cur_tag = cur.execute("SELECT id FROM tag WHERE tag = ?", (tag,)).fetchall()

    if cur_tag:
        (tag_id,) = cur_tag[0]
    else:
        t = cur.execute("INSERT INTO tag (tag) VALUES (?)", (tag,))
        tag_id = t.lastrowid

    cur_type = cur.execute(
        "SELECT id FROM type WHERE error_type = ?", (err_type,)
    ).fetchall()
    if cur_type:
        (type_id,) = cur_type[0]
    else:
        t = cur.execute(
            "INSERT INTO type (error_type, tag_id) VALUES (?, ?)", (err_type, tag_id)
        )
        type_id = t.lastrowid

    t = cur.execute(
        "INSERT INTO phrase (phrase, student_id) VALUES (?, ?)", (phrase, student_id)
    )
    phrase_id = t.lastrowid

    t = cur.execute(
        "INSERT INTO error (phrase_id, tag_id, type_id, comment, weight) VALUES (?, ?, ?, ?, ?)",
        (phrase_id, tag_id, type_id, comment, weight),
    )

    con.commit()
    con.close()


if __name__ == "__main__":
    main()
