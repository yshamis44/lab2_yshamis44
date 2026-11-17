import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

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

    # TODO: c) Calculate the Final Grade and GPA
    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    # TODO: e) Find failed formative(s) with the highest weight
    # TODO: f) Print the resubmission options

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)