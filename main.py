import pandas as pd
import os
from scheduler import build_candidate_from_df, find_best_assignment, drop_teacher

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
    
    print("Welcome to FFCS Helper")
    print("Press V to view current timetable")
    print("Press E to exit")
    print("---------------------------------")    
    
    running = True
    while running:   
        i = input().upper()
        if i == "Q":
            running = False
        elif i == "V":
            print(result_df)
        elif i == "D":
            name = input("Enter name of teacher to drop: ")
            subjects_candidates = drop_teacher(subjects_candidates, name)
            result_df = find_best_assignment(subjects_candidates)
            print(result_df)
 
if __name__ == "__main__":
    main()



