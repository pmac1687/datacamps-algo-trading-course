from fastquant import get_stock_data, backtest
import csv


df = get_stock_data("JFC", "2018-01-01", "2019-01-01")

# df.dropna()

combos = []
A = range(5, 25, 2)
B = range(25, 60, 2)
for x in A:
    for y in B:
        combos.append([x, y])
results = []

labels = ["fast", "slow", "w/l"]

with open("emac_5-25_25-60.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=labels)
    writer.writeheader()

    for d in combos:
        res = backtest("emac", df, fast_period=d[0], slow_period=d[1])
        print(res["final_value"])
        row = {
            "fast": d[0],
            "slow": d[1],
            "w/l": -1 * (100000 - int(res["final_value"])),
        }
        writer.writerow(row)


# try:
#    res = backtest(
#        "smac", df, fast_period=range(5, 20, 3), slow_period=range(50, 100, 3)
#    )
#    print(res[["fast_period", "slow_period", "final_value"]])
#
# except ValueError:
#    print(1)
#    print(res[["fast_period", "slow_period", "final_value"]])
