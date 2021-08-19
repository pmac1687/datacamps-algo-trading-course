import pandas_datareader as pa_da
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def add_mas(names, periods, signals, aapl):
    for i in range(len(names)):
        signals[f"{names[i]}_mavg"] = (
            aapl["Close"].rolling(window=periods[i], min_periods=1, center=False).mean()
        )

    return signals


def create_signals(signals, periods, names):
    # adds 1 to signals where short is greater than long period ma
    signals["signals"][periods[0] :] = np.where(
        signals["short_mavg"][periods[0] :] > signals["long_mavg"][periods[0] :],
        1.0,
        0.0,
    )
    return signals


def plot_it(signals, aapl):
    # Initialize the plot figure
    fig = plt.figure()

    # Add a subplot and label for y-axis
    ax1 = fig.add_subplot(111, ylabel="Price in $")

    # Plot the closing price
    aapl["Close"].plot(ax=ax1, color="r", lw=2.0)

    # Plot the short and long moving averages
    signals[["short_mavg", "long_mavg"]].plot(ax=ax1, lw=2.0)

    # Plot the buy signals
    ax1.plot(
        signals.loc[signals.positions == 1.0].index,
        signals.short_mavg[signals.positions == 1.0],
        "^",
        markersize=10,
        color="m",
    )

    # Plot the sell signals
    ax1.plot(
        signals.loc[signals.positions == -1.0].index,
        signals.short_mavg[signals.positions == -1.0],
        "v",
        markersize=10,
        color="k",
    )

    # Show the plot
    plt.show()


def main():
    periods = [40, 100]
    names = ["short", "long"]
    tick = "aapl"
    dates = ["01-01-2007", "07-09-2012"]

    aapl = pa_da.get_data_yahoo(tick, dates[0], dates[1])
    signals = pd.DataFrame(index=aapl.index)
    signals["signals"] = 0.0
    signals = add_mas(names, periods, signals, aapl)
    signals = create_signals(signals, periods, names)
    # ****important***  when signals swings one way or the other from signals
    # positions == 1 if buy condition
    # positions == 2 if sell condition
    signals["positions"] = signals["signals"].diff()
    plot_it(signals, aapl)

    return signals, aapl


if __name__ == "__main__":
    main()
