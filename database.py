import mysql.connector
import pandas as pd

from scheduler import build_candidate_from_df, find_best_assignment, drop_teacher, cnf_teacher

conn = mysql.connector.connect(
        host = "localhost",
        user = "viewer",
        database = "BACSE101_Project"
    )

cursor = conn.cursor()

def get_subject_list():
    cursor.execute("SHOW TABLES")
    lst = []
    for table_name in cursor:
        lst.append(table_name[0])
    return lst

def add_subject(code):
    query = "CREATE TABLE IF NOT EXISTS " + code + " (Preference INT PRIMARY KEY, TheorySlot VARCHAR(50), LabSlot VARCHAR(50), Name VARCHAR(50), TheoryVenue VARCHAR(50), LabVenue VARCHAR(50))"#
    cursor.execute(query)

    trs_list = pd.read_csv("data/"+code+"_list.csv")
    pref_list = pd.read_csv("data/"+code+"_pref.csv")

    final_df = pd.DataFrame()

    for idx, row in pref_list.iterrows():
        preference = row["Preference"]
        name = row["Name"]
        theory_slot = ""
        lab_slot = ""
        theory_venue = ""
        lab_venue = ""

        tr_rows = trs_list[trs_list["Name"] == name]

        for _, r in tr_rows.iterrows():
            if r["Slot"][0] != "L":
                theory_slot = r["Slot"]
                theory_venue = r["Venue"]
            elif r["Slot"][0] == "L":
                lab_slot = r["Slot"]
                lab_venue = r["Venue"]

        new_row = {
            "Preference" : preference,
            "Name" : name,
            "TheorySlot" : theory_slot,
            "LabSlot" : lab_slot,
            "TheoryVenue" : theory_venue,
            "LabVenue" : lab_venue
        }

        if new_row["TheorySlot"] != "":
            new_row_df = pd.DataFrame([new_row])
            final_df = pd.concat([final_df, new_row_df], ignore_index = True)

    insert_query = "INSERT INTO " + code + " (Preference, TheorySlot, LabSlot, Name, TheoryVenue, LabVenue) VALUES (%s, %s, %s, %s, %s, %s)"

    data_to_insert = [
        (
            int(row["Preference"]),
            row["TheorySlot"],
            row["LabSlot"],
            row["Name"],
            row["TheoryVenue"],
            row["LabVenue"]
        )
        for _, row in final_df.iterrows()
    ]

    cursor.executemany(insert_query, data_to_insert)
    conn.commit()

def drop_subject(code):
    query = "DROP TABLE " + code
    print(query)
    cursor.execute(query)

    conn.commit()

def load_subjects_candidates():
    SUBJECTS_LIST = get_subject_list()
    subjects_candidates = []
    
    for i in SUBJECTS_LIST:
        query = "SELECT * FROM " + i
        cursor.execute(query)

        rows = cursor.fetchall()
        columns = cursor.column_names

        df = pd.DataFrame(rows, columns=columns)
        cands = build_candidate_from_df(df)
        cands = sorted(cands, key = lambda x : x["preference"])

        subjects_candidates.append((i.upper(), cands))

    return subjects_candidates