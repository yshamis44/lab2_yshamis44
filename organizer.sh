#!/bin/bash
# organizer.sh -archives the grades file, resets it and logs each run,
# makes a fresh empty grades.csv and writes what it did to organizer.log

SOURCE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# make the archive folder if it's not there yet
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created the $ARCHIVE_DIR folder."
fi

# stop if there's no grades.csv to archive
if [ ! -f "$SOURCE" ]; then
    echo "Error: $SOURCE was not found in this folder. Nothing to archive."
    exit 1
fi

# date and time for the new filename (YYYYMMDD-HHMMSS)
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
NEW_NAME="grades_${TIMESTAMP}.csv"

# move it to the archive with the new name, then make a new empty one
mv "$SOURCE" "$ARCHIVE_DIR/$NEW_NAME"
touch "$SOURCE"

# >> adds to the end of the log, so old runs stay in it
echo "$TIMESTAMP | original: $SOURCE | archived as: $ARCHIVE_DIR/$NEW_NAME" >> "$LOG_FILE"

echo "Archived $SOURCE as $ARCHIVE_DIR/$NEW_NAME"
echo "Created a new empty $SOURCE"
echo "Logged in $LOG_FILE"