import sys
import csv
import logging
import os

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format="[%(levelname)s] %(message)s")

if len(sys.argv) <= 1:
    logging.error('Provide a file name as an argument!')
    exit()

# Get the name of the bad file we're fixing which was given as an argument from
# the command line.
bad_file_name = sys.argv[1]
logging.info(f'Fixing {bad_file_name}...')

BAD_SWEDISH_BIG_O = 0xc5
GOOD_SWEDISH_BIG_O = [0xc3, 0x85]

# First we fix the bad characters in the file and store the output in an
# intermediate file that we'll use to redo the TSV from CSV.
fix_char_file_name = 'fixing_' + bad_file_name
with open(bad_file_name, 'rb') as bad_file, \
    open(fix_char_file_name, 'wb') as fix_file:
    bad_line = bad_file.readline()
    line_count = 0

    # Read every line in the bad file until there are no more lines.
    while bad_line:
        fix_line = []

        # Loop through the bad line read from the bad file and replace any of
        # the bad characters.
        for i in range(0, len(bad_line)):
            if bad_line[i] == BAD_SWEDISH_BIG_O:
                logging.warning(f'Found a bad character {hex(bad_line[i])} '
                    'on line {line_count}')
                fix_line += GOOD_SWEDISH_BIG_O
            else:
                fix_line.append(bad_line[i])

        # Write out the (possibly) fixed line to the fixed file.
        fix_file.write(bytes(fix_line))

        # Get the next line from the bad file that may need to be fixed.
        bad_line = bad_file.readline()

        line_count += 1

# Now create a fixed, proper TSV file from the file with the corrected chars.
fixed_file_name = 'fixed_' + bad_file_name
logging.info('Final fixed file name is: "' + fixed_file_name + '"')

# Now read in the file as a CSV (even if it's extension is '.tsv') and output
# it to the new fixed file as a TSV.
logging.info('Converting accidental CSV to TSV...')
with open(fix_char_file_name, 'r') as csv_file, \
    open(fixed_file_name, 'w') as tsv_file:
    csv_reader = csv.reader(csv_file)
    tsv_writer = csv.writer(tsv_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)

    for row in csv_reader:
        tsv_writer.writerow(row)

logging.info('Finished converting, cleaning up files...')

# Delete the fix_char_file_name file - we don't need it anymore.
os.remove(fix_char_file_name)

logging.info('Done!')
