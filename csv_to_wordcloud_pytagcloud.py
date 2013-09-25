#!/usr/bin/env python
# W.Wu, 8/7/2013

# MODULES
import sys, csv
from pytagcloud import create_tag_image, make_tags

# PARAMETERS
csv_dataset_path = "data/et_deficiency_prop.csv"
width = 900
height = 600
ext = ".png"

# font_name = "Cuprum"
font_name = "IM Fell DW Pica"
# font_name = "Neuton"
# font_name = "Yanone Kaffeesatz"
output_dir_cols = "pytagcloud/chemicals/"
output_dir_rows = "pytagcloud/woredas/"

# UTILITY FUNCTIONS
def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

# READ CSV:
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
words = table_t[0]
for j in xrange(1,num_columns):
    print "Processing column cloud #%d (%s)..." % (j,header[j])
    weights = table_t[j]
    counts = zip(words,weights)
    tags = make_tags(counts,maxsize=45)
    fname = output_dir_cols + header[j] + "_wordcloud" + ext
    create_tag_image(tags, fname, size=(width, height), fontname=font_name) 
# rows
words = header[1:]
for i in xrange(1,r_count): 
    row_label = table[i][0]
    weights = table[i][1:]
    print "Processing row cloud #%d (%s)..." % (i,row_label)
    counts = zip(words,weights)
    tags = make_tags(counts,maxsize=400)
    fname = output_dir_rows + row_label + "_wordcloud" + ext
    create_tag_image(tags, fname, size=(width, height), fontname=font_name) 
