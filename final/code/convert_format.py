input_file = r"submit.csv"
input_separator = ","
output_file = r"submit2.csv"

with open(input_file, "r") as in_file:
    lines = in_file.readlines()
    lines.sort()
    with open(output_file, "w") as out_file:
        out_file.write("id,x1,y1,x2,y2,score\n")
        for line in lines:
            fields = line.split(input_separator)
            out_file.write("%d,%s,%s,%s,%s,%s" % (int(fields[0][:6]),
                           fields[1],
                           fields[2],
                           fields[3],
                           fields[4],
                           fields[5]))
