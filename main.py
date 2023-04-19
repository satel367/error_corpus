import sqlite3
import json
import matplotlib.pyplot as plt


def main():

    STOPWORDS = {"TenseAgreement", "NegativeForm"}

    with open("groups.json") as f:
        groups = json.load(f)
        
    con = sqlite3.connect("error_corpus.db")
    cur = con.cursor()

    tags = [el[0] for el in cur.execute("SELECT tag FROM tag").fetchall() if not el[0] in STOPWORDS]
    num_tags = []

    for el in tags:
        res = cur.execute(
             f"SELECT count(DISTINCT ph.phrase) FROM phrase as ph WHERE ph.id in (SELECT e.phrase_id FROM error as e WHERE e.tag_id = (SELECT t.id FROM tag as t WHERE t.tag = ?)) ;",
             (el,),
        )
        num_tags.append(res.fetchone()[0])

    fig, ax = plt.subplots()
    ax.hist(num_tags)
    plt.show()

    
    
    # for el, in cur.execute("SELECT tag FROM tag").fetchall():
    #     print(f"{el}: ")

    #     res = cur.execute("SELECT count(DISTINCT ph.phrase) FROM phrase as ph WHERE ph.id in (SELECT e.phrase_id FROM error as e WHERE e.tag_id in (SELECT t.id FROM tag as t WHERE t.tag = ?)) ;", (el,))

    #     print(res.fetchone()[0])

    #     que = """SELECT ph.phrase, ty.error_type, err.comment, err.weight 
    #                FROM phrase AS ph
    #                JOIN error AS err ON ph.id = err.phrase_id
    #                JOIN tag AS t ON t.id = err.tag_id
    #                JOIN type AS ty ON ty.id = err.type_id
    #               WHERE tag = ?;
    #           """
    #     res = cur.execute(que, (el,))
    #     #res = cur.execute("SELECT ph.phrase FROM phrase as ph WHERE ph.id in (SELECT e.phrase_id FROM error as e WHERE e.tag_id = (SELECT t.id FROM tag as t WHERE t.tag = ?));", (el,))
        
    #     #arr = {el for el, in res.fetchall()}
    #     for el in res.fetchall():
    #         phrase, ty, comment, weight = el
    #         print(f"{phrase} \n type: {ty}, \n comment: {comment} \n error weight: {weight}")

    #     print("-" * 70)

    # s = 0

    # for el in groups["Pronunciation mistakes"]:

    #     res = cur.execute(
    #         f"SELECT count(DISTINCT ph.phrase) FROM phrase as ph WHERE ph.id in (SELECT e.phrase_id FROM error as e WHERE e.tag_id = (SELECT t.id FROM tag as t WHERE t.tag = ?)) ;",
    #         (el,),
    #     )

    #     s += res.fetchone()[0]

    # print(f"Number of pronunciation mistakes = {s}")

    con.close()


if __name__ == "__main__":
    main()
