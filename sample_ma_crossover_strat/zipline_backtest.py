# from zipline.api import order_target, record, symbol
# from zipline import run_algorithm
import pandas as pd
import pandas_datareader.data as web


def initialize(context):
    context.sym = symbol("AAPL")
    context.i = 0


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return

    # Compute averages
    # history() has to be called with the same params
    # from above and returns a pandas dataframe.
    short_mavg = data.history(context.sym, "price", 100, "1d").mean()
    long_mavg = data.history(context.sym, "price", 300, "1d").mean()

    # Trading logic
    if short_mavg > long_mavg:
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order_target(context.sym, 100)
    elif short_mavg < long_mavg:
        order_target(context.sym, 0)

    # Save values for later inspection
    record(
        AAPL=data.current(context.sym, "price"),
        short_mavg=short_mavg,
        long_mavg=long_mavg,
    )


if __name__ == "__main__":
    start = pd.Timestamp("2014")
    end = pd.Timestamp("2018")

    sp500 = web.DataReader("SP500", "fred", start, end).SP500
    benchmark_returns = sp500.pct_change()

    result = run_algorithm(
        start=start.tz_localize("UTC"),
        end=end.tz_localize("UTC"),
        initialize=initialize,
        handle_data=handle_data,
        capital_base=100000,
        benchmark_returns=benchmark_returns,
        bundle="quandl",
        data_frequency="daily",
    )
