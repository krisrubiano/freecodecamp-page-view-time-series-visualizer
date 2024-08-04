import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import calendar
from calendar import month_name

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025)) & ((df["value"] <= df["value"].quantile(0.975)))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.plot(df["value"], color="#d62728")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    months = month_name[1:]
    df_bar["months"] = pd.Categorical(df_bar.index.strftime("%B"), categories=months)
    df_bar_plot = pd.pivot_table(data=df_bar, values="value", index=df_bar.index.year, columns="months")

    # Draw bar plot
    fig = df_bar_plot.plot.bar(figsize=(10,10))
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    months = list(calendar.month_abbr)[1:]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(20,10))
    sns.boxplot(data=df_box, x="year", y="value", hue="year", palette="tab10", ax=axes[0]).set(xlabel="Year", ylabel="Page Views", title="Year-wise Box Plot (Trend)")
    sns.boxplot(data=df_box, x="month", y="value", hue="month", palette="husl", order=months, ax=axes[1]).set(xlabel="Month", ylabel="Page Views", title="Month-wise Box Plot (Seasonality)");

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig