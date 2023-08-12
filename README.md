# Monthly Product-wise Gross Profit Analysis

This is a Python script for calculation of monthly product-wise gross profits. The user will need to give the inputs in the form of sales and purchase register, based on which script will calculate Monthly Sales, respective COGS (Cost of Goods Sold) and Gross Profits for each of the products.

The script supports calculation for multiple years and multiple products. 

The user will give the consolidated sales register and consolidated purchase register as the inputs. 

Based on the inputs, the script will evaluate the number of products and number of months, and do the calculations. The output of the script will be in the form of CSV file listing the months and products, the sales and respective COGS and Gross Profits for each of them.

## Monthly Weighted Average Inventory Valuation

The script will calculate COGS on the monthly-weighted average cost basis, i.e. cost per unit of product will be based on cost of opening stock for the respective month and any further purchases during the month.

Calculating the cost for each month separately will give more accurate output and enable better analysis for the decision-makers.

This script will also be particularly useful for those businesses where the prices of goods witness major fluctuations. 

## Business Model

This script is intended basically for trading businesses.

## Input Format

The Sales and Purchase Registers for input should be in CSV Format.

Columns for Sales Register: | Date | Invoice No | Product | Sales Quantity | Sales Rate | Sales Amount

Columns for Purchase Register: | Date | Voucher No | Product | Purchase Quantity | Purchase Rate | Purchase Amount

Date should be in dd mmmm yyyy format.

## Note

Though we have taken adequate care to create this script, however there may have been errors or omissions. The author is not responsible for such errors. This script is provided as-is with no warranties. Use at your own risk. 

Please consult professionals before taking any decisions. 

For any feedback, please contact on hi@darshandudhoria.com
