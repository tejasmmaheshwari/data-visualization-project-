from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Find the CSV file in the same folder as this Python file
FILE_PATH = Path(__file__).parent / "data.csv"


def load_data():
    """Load the dataset from the CSV file."""
    return pd.read_csv(FILE_PATH)


def show_statistics(data):
    """Display statistical information about the dataset."""

    print("\n===== STATISTICS =====")

    print("\nSales Statistics:")
    print(f"Mean: {data['Sales'].mean():,.2f}")
    print(f"Maximum: {data['Sales'].max():,.0f}")
    print(f"Minimum: {data['Sales'].min():,.0f}")
    print(f"Median: {data['Sales'].median():,.2f}")
    print(f"Standard Deviation: {data['Sales'].std():,.2f}")

    print("\nOrders Statistics:")
    print(f"Mean: {data['Orders'].mean():,.2f}")
    print(f"Maximum: {data['Orders'].max():,.0f}")
    print(f"Minimum: {data['Orders'].min():,.0f}")

    print("\nCustomers Statistics:")
    print(f"Mean: {data['Customers'].mean():,.2f}")
    print(f"Maximum: {data['Customers'].max():,.0f}")
    print(f"Minimum: {data['Customers'].min():,.0f}")


def show_insights(data):
    """Display important insights from the dataset."""

    highest_sales_index = int(data["Sales"].argmax())
    lowest_sales_index = int(data["Sales"].argmin())

    highest_sales = data.iloc[highest_sales_index]
    lowest_sales = data.iloc[lowest_sales_index]

    sales_growth = (
        (highest_sales["Sales"] - lowest_sales["Sales"])
        / lowest_sales["Sales"]
    ) * 100

    highest_orders_index = int(data["Orders"].argmax())
    lowest_orders_index = int(data["Orders"].argmin())

    highest_orders = data.iloc[highest_orders_index]
    lowest_orders = data.iloc[lowest_orders_index]

    print("\n===== KEY INSIGHTS =====")

    print(
        f"• {highest_sales['Month']} recorded the highest sales "
        f"of {highest_sales['Sales']:,.0f}."
    )

    print(
        f"• {lowest_sales['Month']} recorded the lowest sales "
        f"of {lowest_sales['Sales']:,.0f}."
    )

    print(
        f"• Sales increased by {sales_growth:.1f}% "
        f"from the lowest-sales month to the highest-sales month."
    )

    print(
        f"• {highest_orders['Month']} had the highest number of orders "
        f"with {highest_orders['Orders']} orders."
    )

    print(
        f"• {lowest_orders['Month']} had the lowest number of orders "
        f"with {lowest_orders['Orders']} orders."
    )

    print(
        f"• The average monthly sales were "
        f"{data['Sales'].mean():,.2f}."
    )

    print(
        f"• The average number of monthly orders was "
        f"{data['Orders'].mean():,.2f}."
    )


def create_charts(data):
    """Create line, bar, and pie charts."""

    # Line chart
    plt.figure(figsize=(10, 5))

    plt.plot(
        data["Month"],
        data["Sales"],
        marker="o"
    )

    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)

    plt.tight_layout()


    # Bar chart
    plt.figure(figsize=(10, 5))

    plt.bar(
        data["Month"],
        data["Sales"]
    )

    plt.title("Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)

    plt.tight_layout()


    # Pie chart
    plt.figure(figsize=(8, 8))

    plt.pie(
        data["Orders"],
        labels=data["Month"].tolist(),
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Monthly Distribution of Orders")
    plt.tight_layout()


    # Display all charts
    plt.show()


def main():
    """Run the complete data visualization program."""

    data = load_data()

    print("===== DATASET =====")
    print(data)

    print("\n===== FIRST FIVE ROWS =====")
    print(data.head())

    show_statistics(data)
    show_insights(data)
    create_charts(data)


if __name__ == "__main__":
    main()