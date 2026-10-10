import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
import pandas as pd

import data_visualization


# ============================================================
# DATA
# ============================================================

data = data_visualization.load_data()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def save_data():
    """Save the current DataFrame to the CSV file."""

    data.to_csv(
        data_visualization.FILE_PATH,
        index=False
    )


def refresh_data():
    """Reload the dataset from the CSV file."""

    global data

    data = data_visualization.load_data()


# ============================================================
# VIEW DATA
# ============================================================

def view_data():
    """Open the dataset window."""

    view_window = tk.Toplevel(root)
    view_window.title("Dataset")
    view_window.geometry("900x600")

    search_frame = tk.Frame(view_window)
    search_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    tk.Label(
        search_frame,
        text="Search:"
    ).pack(
        side="left",
        padx=5
    )

    search_entry = tk.Entry(
        search_frame,
        width=40
    )

    search_entry.pack(
        side="left",
        padx=5
    )

    table_frame = tk.Frame(view_window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    vertical_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical"
    )

    horizontal_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="horizontal"
    )

    table = ttk.Treeview(
        table_frame,
        columns=list(data.columns),
        show="headings",
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set
    )

    vertical_scrollbar.config(
        command=table.yview
    )

    horizontal_scrollbar.config(
        command=table.xview
    )

    for column in data.columns:

        table.heading(
            column,
            text=column
        )

        table.column(
            column,
            width=180
        )

    table.pack(
        side="left",
        fill="both",
        expand=True
    )

    vertical_scrollbar.pack(
        side="right",
        fill="y"
    )

    horizontal_scrollbar.pack(
        side="bottom",
        fill="x"
    )

    def display_data(dataset):
        """Display a DataFrame inside the table."""

        for item in table.get_children():
            table.delete(item)

        for index, row in dataset.iterrows():

            table.insert(
                "",
                tk.END,
                iid=str(index),
                values=list(row)
            )

    def search_data():
        """Search across all columns."""

        search_text = (
            search_entry
            .get()
            .strip()
            .lower()
        )

        if not search_text:
            display_data(data)
            return

        filtered_data = data[
            data.astype(str)
            .apply(
                lambda row:
                row.str.lower()
                .str.contains(
                    search_text,
                    na=False
                )
                .any(),
                axis=1
            )
        ]

        display_data(filtered_data)

    def clear_search():
        """Clear the search."""

        search_entry.delete(
            0,
            tk.END
        )

        display_data(data)

    search_button = tk.Button(
        search_frame,
        text="Search",
        command=search_data
    )

    search_button.pack(
        side="left",
        padx=5
    )

    clear_button = tk.Button(
        search_frame,
        text="Clear",
        command=clear_search
    )

    clear_button.pack(
        side="left",
        padx=5
    )

    display_data(data)


# ============================================================
# ADD DATA
# ============================================================

def add_data():
    """Open a window to add a new row."""

    add_window = tk.Toplevel(root)

    add_window.title("Add Data")
    add_window.geometry("400x350")

    entries = {}

    for row_number, column in enumerate(data.columns):

        tk.Label(
            add_window,
            text=f"{column}:"
        ).grid(
            row=row_number,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        entry = tk.Entry(
            add_window,
            width=30
        )

        entry.grid(
            row=row_number,
            column=1,
            padx=10,
            pady=10
        )

        entries[column] = entry

    def add_row():
        """Add the entered data to the dataset."""

        global data

        new_row = {}

        for column in data.columns:

            value = entries[column].get().strip()

            if value == "":
                messagebox.showerror(
                    "Error",
                    f"Please enter a value for {column}."
                )
                return

            new_row[column] = value

        try:
            new_row["Sales"] = float(
                new_row["Sales"]
            )

            new_row["Orders"] = int(
                new_row["Orders"]
            )

            new_row["Customers"] = int(
                new_row["Customers"]
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Sales must be a number, and Orders and Customers must be whole numbers."
            )

            return

        new_row_data = pd.DataFrame(
            [new_row]
        )

        data = pd.concat(
            [
                data,
                new_row_data
            ],
            ignore_index=True
        )

        save_data()

        messagebox.showinfo(
            "Success",
            "Data added successfully."
        )

        add_window.destroy()

    add_button = tk.Button(
        add_window,
        text="Add Data",
        width=15,
        command=add_row
    )

    add_button.grid(
        row=len(data.columns),
        column=0,
        columnspan=2,
        pady=20
    )


# ============================================================
# UPDATE DATA
# ============================================================

def update_data():
    """Open a window to update an existing row."""

    update_window = tk.Toplevel(root)

    update_window.title("Update Data")
    update_window.geometry("800x500")

    tk.Label(
        update_window,
        text="Select the row you want to update:"
    ).pack(
        pady=10
    )

    table_frame = tk.Frame(update_window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=10
    )

    table = ttk.Treeview(
        table_frame,
        columns=list(data.columns),
        show="headings"
    )

    for column in data.columns:

        table.heading(
            column,
            text=column
        )

        table.column(
            column,
            width=150
        )

    for index, row in data.iterrows():

        table.insert(
            "",
            tk.END,
            iid=str(index),
            values=list(row)
        )

    table.pack(
        fill="both",
        expand=True
    )

    def edit_selected():

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a row first."
            )

            return

        selected_index = int(
            selected[0]
        )

        edit_window = tk.Toplevel(
            update_window
        )

        edit_window.title(
            "Edit Data"
        )

        edit_window.geometry(
            "400x350"
        )

        entries = {}

        for row_number, column in enumerate(data.columns):

            tk.Label(
                edit_window,
                text=f"{column}:"
            ).grid(
                row=row_number,
                column=0,
                padx=10,
                pady=10,
                sticky="w"
            )

            entry = tk.Entry(
                edit_window,
                width=30
            )

            entry.insert(
                0,
                str(
                    data.iloc[
                        selected_index
                    ][column]
                )
            )

            entry.grid(
                row=row_number,
                column=1,
                padx=10,
                pady=10
            )

            entries[column] = entry

        def save_update():

            global data

            updated_values = {}

            for column in data.columns:

                value = (
                    entries[column]
                    .get()
                    .strip()
                )

                if value == "":

                    messagebox.showerror(
                        "Error",
                        f"Please enter a value for {column}."
                    )

                    return

                updated_values[column] = value

            try:

                updated_values["Sales"] = float(
                    updated_values["Sales"]
                )

                updated_values["Orders"] = int(
                    updated_values["Orders"]
                )

                updated_values["Customers"] = int(
                    updated_values["Customers"]
                )

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Sales must be a number, and Orders and Customers must be whole numbers."
                )

                return

            for column in data.columns:

                data.loc[
                    selected_index,
                    column
                ] = updated_values[column]

            save_data()

            messagebox.showinfo(
                "Success",
                "Data updated successfully."
            )

            edit_window.destroy()
            update_window.destroy()

        save_button = tk.Button(
            edit_window,
            text="Save Changes",
            width=15,
            command=save_update
        )

        save_button.grid(
            row=len(data.columns),
            column=0,
            columnspan=2,
            pady=20
        )

    edit_button = tk.Button(
        update_window,
        text="Edit Selected Row",
        command=edit_selected
    )

    edit_button.pack(
        pady=10
    )


# ============================================================
# DELETE DATA
# ============================================================

def delete_data():
    """Open a window to delete an existing row."""

    delete_window = tk.Toplevel(root)

    delete_window.title("Delete Data")
    delete_window.geometry("800x500")

    tk.Label(
        delete_window,
        text="Select the row you want to delete:"
    ).pack(
        pady=10
    )

    table_frame = tk.Frame(
        delete_window
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=10
    )

    table = ttk.Treeview(
        table_frame,
        columns=list(data.columns),
        show="headings"
    )

    for column in data.columns:

        table.heading(
            column,
            text=column
        )

        table.column(
            column,
            width=150
        )

    for index, row in data.iterrows():

        table.insert(
            "",
            tk.END,
            iid=str(index),
            values=list(row)
        )

    table.pack(
        fill="both",
        expand=True
    )

    def remove_selected():

        global data

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a row first."
            )

            return

        selected_index = int(
            selected[0]
        )

        confirmation = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete the selected row?"
        )

        if not confirmation:
            return

        data = data.drop(
            index=selected_index
        ).reset_index(
            drop=True
        )

        save_data()

        messagebox.showinfo(
            "Success",
            "Data deleted successfully."
        )

        delete_window.destroy()

    delete_button = tk.Button(
        delete_window,
        text="Delete Selected Row",
        command=remove_selected
    )

    delete_button.pack(
        pady=10
    )


# ============================================================
# STATISTICS
# ============================================================

def show_statistics():
    """Display dataset statistics."""

    refresh_data()

    statistics_window = tk.Toplevel(root)

    statistics_window.title(
        "Statistics"
    )

    statistics_window.geometry(
        "600x500"
    )

    text_box = tk.Text(
        statistics_window,
        font=("Arial", 12),
        wrap="word"
    )

    text_box.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    text_box.insert(
        tk.END,
        "===== STATISTICS =====\n\n"
    )

    text_box.insert(
        tk.END,
        "Sales Statistics:\n"
    )

    text_box.insert(
        tk.END,
        f"Mean: {data['Sales'].mean():,.2f}\n"
    )

    text_box.insert(
        tk.END,
        f"Maximum: {data['Sales'].max():,.0f}\n"
    )

    text_box.insert(
        tk.END,
        f"Minimum: {data['Sales'].min():,.0f}\n"
    )

    text_box.insert(
        tk.END,
        f"Median: {data['Sales'].median():,.2f}\n"
    )

    text_box.insert(
        tk.END,
        f"Standard Deviation: {data['Sales'].std():,.2f}\n\n"
    )

    text_box.insert(
        tk.END,
        "Orders Statistics:\n"
    )

    text_box.insert(
        tk.END,
        f"Mean: {data['Orders'].mean():,.2f}\n"
    )

    text_box.insert(
        tk.END,
        f"Maximum: {data['Orders'].max():,.0f}\n"
    )

    text_box.insert(
        tk.END,
        f"Minimum: {data['Orders'].min():,.0f}\n\n"
    )

    text_box.insert(
        tk.END,
        "Customers Statistics:\n"
    )

    text_box.insert(
        tk.END,
        f"Mean: {data['Customers'].mean():,.2f}\n"
    )

    text_box.insert(
        tk.END,
        f"Maximum: {data['Customers'].max():,.0f}\n"
    )

    text_box.insert(
        tk.END,
        f"Minimum: {data['Customers'].min():,.0f}\n"
    )

    text_box.config(
        state="disabled"
    )


# ============================================================
# KEY INSIGHTS
# ============================================================

def show_insights():
    """Display key insights."""

    refresh_data()

    insights_window = tk.Toplevel(root)

    insights_window.title(
        "Key Insights"
    )

    insights_window.geometry(
        "650x450"
    )

    text_box = tk.Text(
        insights_window,
        font=("Arial", 12),
        wrap="word"
    )

    text_box.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    highest_sales_index = int(
        data["Sales"].argmax()
    )

    lowest_sales_index = int(
        data["Sales"].argmin()
    )

    highest_sales = data.iloc[
        highest_sales_index
    ]

    lowest_sales = data.iloc[
        lowest_sales_index
    ]

    sales_growth = (
        (
            highest_sales["Sales"]
            - lowest_sales["Sales"]
        )
        / lowest_sales["Sales"]
    ) * 100

    highest_orders_index = int(
        data["Orders"].argmax()
    )

    lowest_orders_index = int(
        data["Orders"].argmin()
    )

    highest_orders = data.iloc[
        highest_orders_index
    ]

    lowest_orders = data.iloc[
        lowest_orders_index
    ]

    text_box.insert(
        tk.END,
        "===== KEY INSIGHTS =====\n\n"
    )

    text_box.insert(
        tk.END,
        f"• {highest_sales['Month']} recorded "
        f"the highest sales of "
        f"{highest_sales['Sales']:,.0f}.\n\n"
    )

    text_box.insert(
        tk.END,
        f"• {lowest_sales['Month']} recorded "
        f"the lowest sales of "
        f"{lowest_sales['Sales']:,.0f}.\n\n"
    )

    text_box.insert(
        tk.END,
        f"• Sales increased by "
        f"{sales_growth:.1f}% from the "
        f"lowest-sales month to the "
        f"highest-sales month.\n\n"
    )

    text_box.insert(
        tk.END,
        f"• {highest_orders['Month']} had the "
        f"highest number of orders with "
        f"{highest_orders['Orders']} orders.\n\n"
    )

    text_box.insert(
        tk.END,
        f"• {lowest_orders['Month']} had the "
        f"lowest number of orders with "
        f"{lowest_orders['Orders']} orders.\n\n"
    )

    text_box.insert(
        tk.END,
        f"• The average monthly sales were "
        f"{data['Sales'].mean():,.2f}.\n\n"
    )

    text_box.insert(
        tk.END,
        f"• The average number of monthly "
        f"orders was "
        f"{data['Orders'].mean():,.2f}."
    )

    text_box.config(
        state="disabled"
    )


# ============================================================
# CHARTS
# ============================================================

def show_line_chart():
    """Display only the line chart."""

    refresh_data()

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        data["Month"],
        data["Sales"],
        marker="o"
    )

    plt.title(
        "Monthly Sales Trend"
    )

    plt.xlabel(
        "Month"
    )

    plt.ylabel(
        "Sales"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    plt.show()


def show_bar_chart():
    """Display only the bar chart."""

    refresh_data()

    plt.figure(
        figsize=(10, 5)
    )

    plt.bar(
        data["Month"],
        data["Sales"]
    )

    plt.title(
        "Monthly Sales"
    )

    plt.xlabel(
        "Month"
    )

    plt.ylabel(
        "Sales"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    plt.show()


def show_pie_chart():
    """Display only the pie chart."""

    refresh_data()

    plt.figure(
        figsize=(8, 8)
    )

    plt.pie(
        data["Orders"],
        labels=data["Month"].tolist(),
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(
        "Monthly Distribution of Orders"
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Data Visualization Tool"
)

root.geometry(
    "900x650"
)


# Title
title_label = tk.Label(
    root,
    text="Data Visualization Tool",
    font=("Arial", 24, "bold")
)

title_label.pack(
    pady=20
)


# Description
description_label = tk.Label(
    root,
    text="Manage your dataset and generate visualizations",
    font=("Arial", 12)
)

description_label.pack(
    pady=5
)


# Main frame
main_frame = tk.Frame(root)

main_frame.pack(
    pady=30
)


# View Data
view_button = tk.Button(
    main_frame,
    text="View Data",
    width=20,
    command=view_data
)

view_button.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)


# Add Data
add_button = tk.Button(
    main_frame,
    text="Add Data",
    width=20,
    command=add_data
)

add_button.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Update Data
update_button = tk.Button(
    main_frame,
    text="Update Data",
    width=20,
    command=update_data
)

update_button.grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)


# Delete Data
delete_button = tk.Button(
    main_frame,
    text="Delete Data",
    width=20,
    command=delete_data
)

delete_button.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Statistics
statistics_button = tk.Button(
    main_frame,
    text="Statistics",
    width=20,
    command=show_statistics
)

statistics_button.grid(
    row=2,
    column=0,
    padx=10,
    pady=10
)


# Key Insights
insights_button = tk.Button(
    main_frame,
    text="Key Insights",
    width=20,
    command=show_insights
)

insights_button.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# Line Chart
line_button = tk.Button(
    main_frame,
    text="Line Chart",
    width=20,
    command=show_line_chart
)

line_button.grid(
    row=3,
    column=0,
    padx=10,
    pady=10
)


# Bar Chart
bar_button = tk.Button(
    main_frame,
    text="Bar Chart",
    width=20,
    command=show_bar_chart
)

bar_button.grid(
    row=3,
    column=1,
    padx=10,
    pady=10
)


# Pie Chart
pie_button = tk.Button(
    main_frame,
    text="Pie Chart",
    width=20,
    command=show_pie_chart
)

pie_button.grid(
    row=4,
    column=0,
    padx=10,
    pady=10
)


# Exit
exit_button = tk.Button(
    main_frame,
    text="Exit",
    width=20,
    command=root.destroy
)

exit_button.grid(
    row=4,
    column=1,
    padx=10,
    pady=10
)


# Start GUI
root.mainloop()