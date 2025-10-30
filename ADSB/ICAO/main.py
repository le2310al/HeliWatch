import camelot, pandas as pd, csv

types = {'landplane':[], 'amphibian':[], 'seaplane':[], 'gyroplane':[], 'helicopter':[], 'powered_lift':[]}

def csv_by_type():
    for aircraft_class, designator in types.items():
        with open('output/' + aircraft_class + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for icao in designator:
                writer.writerow([icao])

def main():
    tables = camelot.read_pdf('input/FAA.pdf', flavor='stream', pages='10-121')
    for table in tables:
        df = table.df
        for index, row in df.iterrows():
            if row[1] == 'Fixed-wing':
                types.get('landplane').append(row[0])
            elif row[1] == '@Fixed-wing':
                types.get('amphibian').append(row[0])
            elif row[1] == '$Fixed-wing':
                types.get('seaplane').append(row[0])
            elif row[1] == 'Gyroplane':
                types.get('gyroplane').append(row[0])
            elif row[1] == 'Helicopter':
                types.get('helicopter').append(row[0])
            elif row[1] == 'Powered-lift':
                types.get('powered_lift').append(row[0])
    csv_by_type()

if __name__ == '__main__':
    main()