import csv

rows =[]
headers = ['squawk', 'function']

with open('input/UK.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if not row[1]:
            rows.append({"squawk": row[0], "function": row[2]})
        else:
            for x in range(int(row[1])-int(row[0])+1):
                rows.append({"squawk": str(int(row[0])+x).zfill(4),"function": row[2]})

print(rows)
with open('output/UK.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
