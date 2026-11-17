import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    # nothing typed, no point going further
    if filename == "":
        print("Error: no filename was typed. Example: grades.csv")
        sys.exit(1)

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    # this catches an empty CSV (0 bytes) and stops it
    if os.path.getsize(filename) == 0:
        print(f"Error: The file '{filename}' is empty. Add some grades and try again.")
        sys.exit(1)

    assignments = []
    skipped = 0

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # make sure the 4 columns we need are in the header
            header = reader.fieldnames or []
            for column in ['assignment', 'group', 'score', 'weight']:
                if column not in header:
                    print(f"Error: the column '{column}' is missing.")
                    print("The first line must be: assignment,group,score,weight")
                    sys.exit(1)

            line = 1
            for row in reader:
                line += 1
                name = (row['assignment'] or '').strip()
                group = (row['group'] or '').strip().capitalize()
                score_text = (row['score'] or '').strip()
                weight_text = (row['weight'] or '').strip()

                # a row with only commas, skip it
                if name == '' and group == '' and score_text == '' and weight_text == '':
                    print(f"Warning: line {line} is empty, skipping it.")
                    skipped += 1
                    continue

                if name == '':
                    print(f"Warning: line {line} has no assignment name, skipping it.")
                    skipped += 1
                    continue

                if group != 'Formative' and group != 'Summative':
                    print(f"Warning: line {line} ({name}) has group '{row['group']}', it must be Formative or Summative. Skipping it.")
                    skipped += 1
                    continue

                # Convert numeric fields to floats for calculations
                try:
                    score = float(score_text)
                    weight = float(weight_text)
                except ValueError:
                    print(f"Warning: line {line} ({name}) has score '{score_text}' and weight '{weight_text}'. Both must be numbers like 85 and 20. Skipping it.")
                    skipped += 1
                    continue

                assignments.append({
                    'assignment': name,
                    'group': group,
                    'score': score,
                    'weight': weight
                })
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    if skipped > 0:
        print(f"{skipped} bad row(s) were skipped.")

    if len(assignments) == 0:
        print("Error: there are no valid grade rows in the file.")
        sys.exit(1)

    return assignments

def evaluate_grades(data):
    """
    Main Logic: checks the grades, then calculates the GPA and prints results (pass/fail) 
    """
    print("\n--- Processing Grades ---")

    # a) score check - anything below 0 or above 100 is invalid (makes sure no score is out of range)
    bad_scores = []
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            bad_scores.append(item)

    if len(bad_scores) > 0:
        print("Error: every score must be between 0 and 100. These ones are not:")
        for item in bad_scores:
            print(f"  - {item['assignment']}: {item['score']:g}")
        return

    print("Scores OK: all between 0 and 100.")

    # b) sum the weights so we can check them
    total_weight = 0
    formative_weight = 0
    summative_weight = 0
    for item in data:
        total_weight += item['weight']
        if item['group'] == 'Formative':
            formative_weight += item['weight']
        elif item['group'] == 'Summative':
            summative_weight += item['weight']

    # weight rule: total = 100, formative = 60, summative = 40
    weight_errors = []
    if total_weight != 100:
        weight_errors.append(f"Total weight is {total_weight:g}, it must be exactly 100.")
    if formative_weight != 60:
        weight_errors.append(f"Formative weight is {formative_weight:g}, it must be exactly 60.")
    if summative_weight != 40:
        weight_errors.append(f"Summative weight is {summative_weight:g}, it must be exactly 40.")

    if len(weight_errors) > 0:
        print("Error: the weights are wrong:")
        for problem in weight_errors:
            print(f"  - {problem}")
        return

    print("Weights OK: total 100 (Formative 60, Summative 40).")

        # c) score x weight / 100 = points earned for that assignment
    formative_points = 0
    summative_points = 0
    for item in data:
        points = item['score'] * item['weight'] / 100
        if item['group'] == 'Formative':
            formative_points += points
        elif item['group'] == 'Summative':
            summative_points += points

    total_grade = formative_points + summative_points
    gpa = (total_grade / 100) * 5.0

    # turn each group into a percentage so we can compare with 50
    formative_percent = formative_points / formative_weight * 100
    summative_percent = summative_points / summative_weight * 100

    print(f"\nFormative: {formative_points:.2f} / 60 ({formative_percent:.2f}%)")
    print(f"Summative: {summative_points:.2f} / 40 ({summative_percent:.2f}%)")
    print(f"Final grade: {total_grade:.2f} / 100")
    print(f"GPA: {gpa:.2f} / 5.0")

    # d) need 50% or more in BOTH formative and summative to pass
    if formative_percent >= 50 and summative_percent >= 50:
        status = "PASSED"
    else:
        status = "FAILED"

    print(f"\nFinal decision: {status}")

        # e) formatives under 50 are failed
    failed_formatives = []
    for item in data:
        if item['group'] == 'Formative' and item['score'] < 50:
            failed_formatives.append(item)

    # find the biggest weight among the failed ones
    highest_weight = 0
    for item in failed_formatives:
        if item['weight'] > highest_weight:
            highest_weight = item['weight']

    # keep every failed one with that weight, so ties all show up
    resubmit = []
    for item in failed_formatives:
        if item['weight'] == highest_weight:
            resubmit.append(item)

    # f) show the student what they can resubmit 
    if len(resubmit) == 0:
        print("Resubmission: none, no formative assignment was failed.")
    else:
        print("Eligible for resubmission:")
        for item in resubmit:
            print(f"  - {item['assignment']} (score {item['score']:g}, weight {item['weight']:g})")

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)