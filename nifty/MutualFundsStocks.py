import csv
sector_wise_map = {}
with open('files/stocks_nov_2020.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    count = 0
    for row in csv_reader:
        stock, sector, classification, month, qty, value = row
        if count==0:
            count+=1
            continue

        final_value = "{}:::{}".format(stock,value)
        if sector not in sector_wise_map:
            sector_wise_map[sector] = final_value
        else:
            current_max_value =sector_wise_map[sector].split(":::")[1]
            if float(value)>float(current_max_value):
                sector_wise_map[sector] = final_value

for sector in sector_wise_map.keys():
    print("{} - {}".format(sector,sector_wise_map[sector].split(":::")[0]))