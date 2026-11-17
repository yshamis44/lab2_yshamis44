# lab2_yshamis44 – ALU Transcript Generator

A Python program that reads course grades from `grades.csv`, checks them, and works out the final grade, GPA, pass/fail status and which assignment(s) can be resubmitted. A Bash script (`organizer.sh`) archives the grades file and keeps a log.

## Files
- `grade-evaluator.py` – the grade checker and GPA calculator
- `grades.csv` – the course grades (assignment, group, score, weight)
- `organizer.sh` – archives `grades.csv` with a timestamp and logs it
- `Readme.md` – this file

## How to run the Python program
```
python3 grade-evaluator.py
```
When asked, type the file name, for example `grades.csv`.

What it does:
1. Checks every score is between 0 and 100
2. Checks the weights: 100 in total, Formative = 60, Summative = 40
3. Works out the final grade and GPA (GPA = Total / 100 × 5.0)
4. PASSED only if the student has 50% or more in **both** Formative and Summative
5. Lists the failed formative assignment(s) with the highest weight for resubmission (if several tie, all are shown)

Result with the given `grades.csv`:
```
Final grade: 60.00 / 100
GPA: 3.00 / 5.0
Final decision: PASSED
Eligible for resubmission:
  - Group Exercise (score 40, weight 20)
  - Functions and Debugging Lab (score 45, weight 20)
```

## Error handling
- File not found, empty file, or no filename typed: clear error message, program stops
- Missing columns: tells you the header it expects
- Empty rows, missing names, wrong group, or text where a number should be: the row is skipped with a warning, and the number of bad rows is shown
- Scores outside 0–100 or wrong weights: the program says exactly which ones are wrong

## How to run the shell script
```
chmod +x organizer.sh
./organizer.sh
```
It will:
1. Create an `archive` folder if it doesn't exist
2. Move `grades.csv` into `archive/` renamed with a timestamp (e.g. `grades_20251105-170000.csv`)
3. Create a new empty `grades.csv`
4. Add a line to `organizer.log` with the timestamp, original name and archived name

Note: running it empties `grades.csv`, so run the Python program first.
