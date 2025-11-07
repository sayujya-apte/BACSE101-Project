import pandas as pd

def split_slot_str(slot):
    slots = [p for p in slot.split("+") if p != ""]
    return set(slots)

def build_candidate_from_df(df):
    candidates = []

    df_sorted = df.copy()
    df_sorted['Preference'] = pd.to_numeric(df_sorted['Preference'], errors='coerce').fillna(9999).astype(int)
    df_sorted = df_sorted.sort_values(['Preference'])

    grouped = {}

    for _, row in df_sorted.iterrows():
        key = (row.get("Name", ""), int(row.get("Preference", 9999)))
        grouped.setdefault(key, []).append(row)

    for (name, pref), rows in grouped.items():
        theory_raw = rows[0]["TheorySlot"]
        lab_raw = rows[0]["LabSlot"]
        '''
        if len(rows) < 2:
            r1 = rows[0]
            theory_raw = r1["Slot"]
            lab_raw = r1["Slot"]

            venues = {r1["Venue"]}
        else:
            r1 = rows[0]
            r2  =rows[1]

            theory_raw = r1["Slot"]
            lab_raw = r2["Slot"]
        '''
        cand = {
            "name" : name,
            "preference" : int(pref),
            "theory_raw" : str(theory_raw),
            "lab_raw" : str(lab_raw),
            "theory_slots" : split_slot_str(theory_raw),
            "lab_slots" : split_slot_str(lab_raw),
            "theory_venue" : rows[0]["TheoryVenue"],
            "lab_venue" : rows[0]["LabVenue"]
        }

        candidates.append(cand)

    return candidates

def find_best_assignment(subject_candidates):
    n = len(subject_candidates)
    best = {"score" : float("inf"), "assignment" : None}
    used_slots_global = set()

    order = sorted(range(n), key = lambda x: len(subject_candidates[x][1]) if subject_candidates[x][1] else 0)

    def backtrack(idx, used_slots, current_score, current_assignment):
        if current_score >= best["score"]:
            return

        if idx == n:
            best["score"] = current_score
            best["assignment"] = list(current_assignment)
            return

        subject_index = order[idx]
        subject_name, candidates = subject_candidates[subject_index]

        for cand in candidates:
            cand_slots = cand["theory_slots"] | cand["lab_slots"] # Union

            if used_slots & cand_slots: # Intersection
                continue

            current_assignment.append((subject_name, cand))
            backtrack(idx + 1, used_slots | cand_slots, current_score + cand["preference"], current_assignment)
            current_assignment.pop()

    backtrack(0, set(), 0, [])
    
    if best["assignment"] is None:
        print("No feasible arrangement")
        return

    rows = []
    for subject_name, cands in best["assignment"]:
        rows.append({
            "Subject" : subject_name,
            "Preference" : cands["preference"],
            "Teacher" : cands["name"],
            "TheorySlot" : cands["theory_raw"],
            "LabSlot" : cands["lab_raw"],
            "TheoryVenue" : cands["theory_venue"],
            "LabVenue" : cands["lab_venue"]
            })
    result_df = pd.DataFrame(rows)

    return result_df

def drop_teacher(subjects_candidates, subject, name):
    updated = []
    for sub, cand in subjects_candidates:
        if sub == subject:
            filtered = [c for c in cand if c["name"].upper() != name.upper()]
            updated.append((sub, filtered))
        else:
            updated.append((sub, cand))

    return updated

def cnf_teacher(subjects_candidates, subject, name):
    updated = []
    for sub, cand in subjects_candidates:
        if sub == subject:
            filtered = [c for c in cand if c["name"].upper() == name.upper()]
            updated.append((sub, filtered))
        else:
            updated.append((sub, cand))

    return updated