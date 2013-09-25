#!/usr/bin/env python
import sys, csv, os
import numpy as np
sys.path.insert(0, 'amueller_word_cloud')
import wordcloud

# PARAMETERS
csv_dataset_path = "data/et_deficiency_prop.csv"
width = 800
height = 600
ext = ".png"
font_path = "/Library/Fonts/Palatino.ttc"
output_dir_cols = "amueller/chemicals/"
output_dir_rows = "amueller/woredas/"

for d in [output_dir_cols, output_dir_rows]:
    if not os.path.exists(d): os.makedirs(d)

# UTILITY FUNCTIONS
def isfloat(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True

# READ CSV
ifile  = open(csv_dataset_path, "r")
reader = csv.reader(ifile)
table = []
num_columns = -1
r_count = 0
c_count = 0
line_count = 0
for row in reader:
    r = []
    if 0 == line_count:
        num_columns = len(row)
        header = row
    else:
        c_count = 0
        for col in row:
            c_count += 1
            if isfloat(col):
                col = float(col)
            r.append(col)
        print r
        if c_count != num_columns:
            print "Warning: Line #%d has only %d columns. Ignoring it." % (line_count, c_count)
            continue
        else:   
            r_count += 1
            table.append(r)
    line_count += 1
ifile.close()
print "Matrix shape: %d rows, %d columns" % (r_count, num_columns)
print "Header: " + str(header)

# CHECK THAT ALL ROWS HAVE SAME NUMBER OF COLUMNS
if not all(map(lambda x: x == num_columns,map(len,table))):
    sys.exit("ERROR: Not all rows have the same number of columns. Aborting.")

# TRANSPOSE
table_t = map(list,zip(*table))


# GENERATE WORDCLOUDS
# columns
words = np.asarray(table_t[0])
for j in xrange(1,num_columns): 
    print "Processing column cloud #%d (%s)..." % (j,header[j])
    counts = np.asarray(table_t[j])
    fname = output_dir_cols + header[j] + "_wordcloud" + ext
    wordcloud.make_wordcloud(words, counts, fname, font_path, width, height)
# rows
words = np.asarray(header[1:])
for i in xrange(1,r_count): 
    row_label = table[i][0]
    row_data = table[i][1:]
    print "Processing row cloud #%d (%s)..." % (i,row_label)
    counts = np.asarray(row_data)
    fname = output_dir_rows + row_label + "_wordcloud" + ext
    wordcloud.make_wordcloud(words, counts, fname, font_path, width, height)
