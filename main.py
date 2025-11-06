import pandas as pd
import os

from scheduler import build_candidate_from_df, find_best_assignment, drop_teacher, cnf_teacher
from database import add_subject, drop_subject, get_subject_list, load_subjects_candidates, stow_timetable, retrieve_timetable

def welcome():
    os.system("cls")
    print("---------------------------------")
    print("Welcome to FFCS Helper")
    print("---------------------------------")
    print("Press V to view current timetable")
    print("Press C to confirm a teacher")
    print("Press D to drop a teacher")
    print("Press E to exit")

def main():
    subjects_candidates = load_subjects_candidates()

    if retrieve_timetable() is not None:
        result_df = retrieve_timetable()
    else:
        result_df = find_best_assignment(subjects_candidates)
    
    welcome()

    running = True
    while running:   
        print("---------------------------------")
        i = input("# ").upper()
        if i == "Q":
            stow_timetable(result_df)
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
        elif i == "AS":
            code = input("Enter the subject code")
            add_subject(code)
        elif i == "DS":
            code = input("Enter the subject code")
            drop_subject(code)
        elif i == "LS":
            print(get_subject_list())
        elif i == "RS":
            subjects_candidates = load_subjects_candidates()
            result_df = find_best_assignment(subjects_candidates)
            print(result_df)
        elif i == "CLS":
            welcome()
        else:
            print("Please enter valid input!")
 
if __name__ == "__main__":
    main()



