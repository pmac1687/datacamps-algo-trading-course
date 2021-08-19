from main import main as mn
import pandas_datareader as pa_da
import pandas as pd

# import numpy as np
import matplotlib.pyplot as plt


def plot_it(portfolio):
    # Create a figure
    fig = plt.figure()

    ax1 = fig.add_subplot(111, ylabel="Portfolio value in $")

    # Plot the equity curve in dollars
    portfolio["total"].plot(ax=ax1, lw=2.0)

    ax1.plot(
        portfolio.loc[signals.positions == 1.0].index,
        portfolio.total[signals.positions == 1.0],
        "^",
        markersize=10,
        color="m",
    )
    ax1.plot(
        portfolio.loc[signals.positions == -1.0].index,
        portfolio.total[signals.positions == -1.0],
        "v",
        markersize=10,
        color="k",
    )

    # Show the plot
    plt.show()


def main(signals, initial_capital, aapl):
    # Create a DataFrame `positions`
    positions = pd.DataFrame(index=signals.index).fillna(0.0)

    # Buy a 100 shares
    positions["AAPL"] = 100 * signals["signals"]

    # Initialize the portfolio with value owned
    portfolio = positions.multiply(aapl["Adj Close"], axis=0)

    # Store the difference in shares owned
    pos_diff = positions.diff()

    # Add `holdings` to portfolio
    portfolio["holdings"] = (positions.multiply(aapl["Adj Close"], axis=0)).sum(axis=1)

    # Add `cash` to portfolio
    portfolio["cash"] = (
        initial_capital
        - (pos_diff.multiply(aapl["Adj Close"], axis=0)).sum(axis=1).cumsum()
    )

    # Add `total` to portfolio
    portfolio["total"] = portfolio["cash"] + portfolio["holdings"]

    # Add `returns` to portfolio
    portfolio["returns"] = portfolio["total"].pct_change()

    # Print the first lines of `portfolio`
    print(portfolio.iloc[-1])

    plot_it(portfolio)


if __name__ == "__main__":
    initial_capital = float(100000.0)
    signals, aapl = mn()
    main(signals, initial_capital, aapl)
