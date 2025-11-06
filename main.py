import pandas as pd
import os
from scheduler import build_candidate_from_df, find_best_assignment, drop_teacher, cnf_teacher

SUBJECT_FILES = ["data/BACSE104.csv", "data/BACSE105.csv", "data/BACSE106.csv"]

def main():
    subjects_candidates = []

    for i in SUBJECT_FILES:
        df = pd.read_csv(i)
        
        subject_label = i[5:13]

        cands = build_candidate_from_df(df)
        cands = sorted(cands, key = lambda x: x["preference"])
        subjects_candidates.append((subject_label, cands))

    result_df = find_best_assignment(subjects_candidates)
    
    print("---------------------------------")
    print("Welcome to FFCS Helper")
    print("---------------------------------")
    print("Press V to view current timetable")
    print("Press C to confirm a teacher")
    print("Press D to drop a teacher")
    print("Press E to exit")

    running = True
    while running:   
        print("---------------------------------")
        i = input("# ").upper()
        if i == "Q":
            running = False
        elif i == "V":
            print(result_df)
        elif i == "D":
            subject = input("Enter the subject code: ")
            name = input("Enter name of teacher to drop: ")
            subjects_candidates = drop_teacher(subjects_candidates, subject, name)
            result_df = find_best_assignment(subjects_candidates)
            print(result_df)
        elif i == "C":
            subject = input("Enter the subject code: ")
            name = input("Enter name of teacher to confirm: ")
            subjects_candidates = cnf_teacher(subjects_candidates, subject, name)
            result_df = find_best_assignment(subjects_candidates)
            print(result_df)
        else:
            print("Please enter valid input!")
 
if __name__ == "__main__":
    main()



