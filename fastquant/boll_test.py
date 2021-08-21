from fastquant import get_stock_data, backtest
import csv


df = get_stock_data("JFC", "2018-01-01", "2019-01-01")

# df.dropna()

combos = []
A = range(10, 40, 2)
# B = range(25, 60, 2)
B = [
    1.0,
    1.1,
    1.2,
    1.3,
    1.4,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
    2.0,
    2.1,
    2.2,
    2.3,
    2.4,
    2.5,
    2.6,
    2.7,
    2.8,
    2.9,
    3.0,
]
for x in A:
    for y in B:
        combos.append([x, y])
results = []

labels = ["period", "dev", "w/l"]

with open("boll_10-40_1-3.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=labels)
    writer.writeheader()

    for d in combos:
        res = backtest("bbands", df, period=d[0], devfactor=d[1])
        print(res["final_value"])
        row = {
            "period": d[0],
            "dev": d[1],
            "w/l": -1 * (100000 - int(res["final_value"])),
        }
        writer.writerow(row)
