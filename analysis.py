import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import seaborn as sns
import warnings

# Silence FutureWarnings (like seaborn palette)
warnings.simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv("train.csv", parse_dates=['Date'])
df.set_index('Date', inplace=True)
monthly_sales = df['Weekly_Sales'].resample('ME').sum()


plt.figure(figsize=(12,6))
plt.plot(monthly_sales.index, monthly_sales.values / 1e6, label='Monthly Sales')
plt.title("Monthly Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales (Millions)")
plt.xticks(rotation=45)

# Show one tick every 3 months
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.legend()
plt.tight_layout()
plt.savefig("Monthly_Sales.png")
plt.clf()

rolling_mean = monthly_sales.rolling(window=3).mean()

plt.figure(figsize=(12,6))

# Plot original sales in millions
plt.plot(monthly_sales.index, monthly_sales.values / 1e6, label='Monthly Sales')

# Plot rolling mean in millions
plt.plot(rolling_mean.index, rolling_mean.values / 1e6, label='3-Month Rolling Average', color='red')

plt.title("Monthly Sales with 3-Month Rolling Average")
plt.xlabel("Date")
plt.ylabel("Sales (Millions)")
plt.legend()

# Format x-axis to show only year and month
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Set ticks every 3 months
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("3_Month_Rolling.png")
plt.clf()

store_sales = df.groupby('Store')['Weekly_Sales'].sum().sort_values(ascending=False)

# Top 10 Stores by Total Sales
top_stores = df.groupby('Store')['Weekly_Sales'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=top_stores.index,
            y=top_stores.values / 1e6,  # convert sales to millions
            palette="Set2")

plt.title("Top 10 Stores by Total Sales")
plt.xlabel("Store ID")
plt.ylabel("Total Sales (in Millions)")
plt.tight_layout()
plt.savefig("Top_10_Stores_Sales.png")
plt.clf()


# Top 10 departments by total sales
dept_sales = df.groupby('Dept')['Weekly_Sales'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=dept_sales.index, y=dept_sales.values / 1e6, palette="Set2")  # convert to millions
plt.title("Top 10 Departments by Total Sales")
plt.ylabel("Total Sales (Millions)")
plt.xlabel("Department ID")
plt.tight_layout()
plt.savefig("Top10_Dept_Sales.png")
plt.clf()