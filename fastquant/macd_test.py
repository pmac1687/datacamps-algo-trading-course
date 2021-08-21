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

with open("macd.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=labels)
    writer.writeheader()

    for d in combos:
        res = backtest(
            "macd",
            df,
            fast_period=9,
            slow_period=45,
            signal_period=9,
            sma_period=36,
            dir_period=10,
        )
        print(res["final_value"])
        row = {
            "fast": d[0],
            "slow": d[1],
            "w/l": -1 * (100000 - int(res["final_value"])),
        }
        writer.writerow(row)
        break
