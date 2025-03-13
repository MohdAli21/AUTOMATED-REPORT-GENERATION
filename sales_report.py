import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF, XPos, YPos
from datetime import datetime

# Load Sales Data with User Input
file_path = input("Enter the Excel file path: ")
sales_data = pd.read_excel(file_path)

# Ensure column names are stripped of spaces
sales_data.columns = sales_data.columns.str.strip()

# Define Sales Column
sales_column = "Revenue"
if sales_column not in sales_data.columns:
    print(f"Error: '{sales_column}' column not found! Available columns: {sales_data.columns}")
    exit()

# Calculate Statistics
total_sales = sales_data[sales_column].sum()
average_sales = sales_data[sales_column].mean()
max_sales = sales_data[sales_column].max()
min_sales = sales_data[sales_column].min()

# Generate a simple sales trend graph (if 'Date' column exists)
if 'Date' in sales_data.columns:
    sales_data['Date'] = pd.to_datetime(sales_data['Date'])
    sales_data = sales_data.sort_values(by='Date')
    sales_data.groupby('Date')[sales_column].sum().plot(kind='line', title='Sales Trend')
    plt.xlabel('Date')
    plt.ylabel('Revenue')
    plt.savefig("sales_chart.png")
    plt.close()
    chart_available = True
else:
    chart_available = False

# Create PDF Report
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title
pdf.set_font("Helvetica", style="B", size=16)
pdf.cell(200, 10, "Sales Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

# Report Date
pdf.set_font("Helvetica", size=12)
pdf.cell(200, 10, f"Report Date: {datetime.today().strftime('%Y-%m-%d')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# Sales Statistics Table
pdf.set_font("Helvetica", style="B", size=12)
pdf.cell(100, 10, "Metric", border=1, align="C")
pdf.cell(100, 10, "Value", border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_font("Helvetica", size=12)
pdf.cell(100, 10, "Total Sales", border=1)
pdf.cell(100, 10, f"${total_sales:,.2f}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.cell(100, 10, "Average Sales", border=1)
pdf.cell(100, 10, f"${average_sales:,.2f}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.cell(100, 10, "Max Sales", border=1)
pdf.cell(100, 10, f"${max_sales:,.2f}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.cell(100, 10, "Min Sales", border=1)
pdf.cell(100, 10, f"${min_sales:,.2f}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# Add Sales Chart if Available
if chart_available:
    pdf.add_page()
    pdf.cell(200, 10, "Sales Trend Chart", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.image("sales_chart.png", x=10, y=None, w=180)

# Save PDF
pdf.output("Enhanced_Sales_Report.pdf")
print("Enhanced PDF Report Generated Successfully!")
