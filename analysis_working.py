
import pandas as pd

# importing sales data from CSV file and basic data transformation
sales_data_raw = pd.read_csv(r'<<path>>/sales_data.csv') #replace it with actual path
sales_data_raw['Date'] = pd.to_datetime(sales_data_raw['Date'])
sales_data_raw['Month and Year'] = sales_data_raw['Date'].dt.to_period('M')

sales_data1 = sales_data_raw.drop(['Date', 'Invoice No', 'Sales Rate'], axis=1)
sales_data = sales_data1.groupby(['Product', 'Month and Year']).sum()

# importing purchase data from CSV file and basic data transformation
purchase_data_raw = pd.read_csv(r'<<path>>/purchase_data.csv') #replace it with actual path
purchase_data_raw['Date'] = pd.to_datetime(purchase_data_raw['Date'])
purchase_data_raw['Month and Year'] = purchase_data_raw['Date'].dt.to_period('M')

purchase_data1 = purchase_data_raw.drop(['Date', 'Voucher No', 'Purchase Rate'], axis=1)
purchase_data = purchase_data1.groupby(['Product', 'Month and Year']).sum()

# merging sales and purchase data into a single table for working
consolidated_data = pd.merge(sales_data, purchase_data, left_index=True, right_index=True, how="outer")
consolidated_data.sort_index(ascending=True, inplace=True)

# adding new columns to the merged data
consolidated_data['Average Sales Price'] = consolidated_data['Sales Amount'] \
                                           / consolidated_data['Sales Quantity']

consolidated_data['Average Purchase Price'] = consolidated_data['Purchase Amount'] \
                                              / consolidated_data['Purchase Quantity']

consolidated_data['Opening Quantity'] = ''
consolidated_data['Opening Amount'] = ''
consolidated_data['AFS Quantity'] = ''
consolidated_data['AFS Rate'] = ''
consolidated_data['AFS Amount'] = ''
consolidated_data['COGS Quantity'] = ''
consolidated_data['COGS Rate'] = ''
consolidated_data['COGS Amount'] = ''
consolidated_data['Closing Quantity'] = ''
consolidated_data['Closing Amount'] = ''

# storing the location of the specific columns in the variables for ease of reference and coding
purchase_quantity_location = consolidated_data.columns.get_loc('Purchase Quantity')
purchase_amount_location = consolidated_data.columns.get_loc('Purchase Amount')
sales_quantity_location = consolidated_data.columns.get_loc('Sales Quantity')
sales_amount_location = consolidated_data.columns.get_loc('Sales Amount')
opening_quantity_location = consolidated_data.columns.get_loc('Opening Quantity')
opening_amount_location = consolidated_data.columns.get_loc('Opening Amount')
afs_quantity_location = consolidated_data.columns.get_loc('AFS Quantity')
afs_rate_location = consolidated_data.columns.get_loc('AFS Rate')
afs_amount_location = consolidated_data.columns.get_loc('AFS Amount')
cogs_quantity_location = consolidated_data.columns.get_loc('COGS Quantity')
cogs_rate_location = consolidated_data.columns.get_loc('COGS Rate')
cogs_amount_location = consolidated_data.columns.get_loc('COGS Amount')
closing_quantity_location = consolidated_data.columns.get_loc('Closing Quantity')
closing_amount_location = consolidated_data.columns.get_loc('Closing Amount')

# filling all blanks with zero
consolidated_data.fillna(0, inplace=True)

# creating a list of all products
list_of_products = list(consolidated_data.index.unique('Product'))

# calculation of cost of goods sold and gross profit
for product_ in list_of_products:

    opening_quantity = 0
    opening_amount = 0

    number_of_rows = consolidated_data.loc[product_].shape[0]
    a = consolidated_data.index.get_loc(product_)

    row_numbers = list(range(a.start, a.stop))

    for row_number in row_numbers:

        purchase_quantity = consolidated_data.iat[row_number, purchase_quantity_location]
        purchase_amount = consolidated_data.iat[row_number, purchase_amount_location]
        sales_quantity = consolidated_data.iat[row_number, sales_quantity_location]
        sales_amount = consolidated_data.iat[row_number, sales_amount_location]

        afs_quantity = opening_quantity + purchase_quantity
        afs_amount = opening_amount + purchase_amount
        afs_rate = afs_amount / afs_quantity

        consolidated_data.iloc[row_number, opening_quantity_location] = opening_quantity
        consolidated_data.iloc[row_number, opening_amount_location] = opening_amount

        consolidated_data.iloc[row_number, afs_quantity_location] = afs_quantity
        consolidated_data.iloc[row_number, afs_amount_location] = afs_amount
        consolidated_data.iloc[row_number, afs_rate_location] = afs_rate

        consolidated_data.iloc[row_number, cogs_quantity_location] = sales_quantity
        consolidated_data.iloc[row_number, cogs_amount_location] = sales_quantity * afs_rate
        consolidated_data.iloc[row_number, cogs_rate_location] = afs_rate

        consolidated_data.iloc[row_number, closing_quantity_location] = afs_quantity - sales_quantity
        consolidated_data.iloc[row_number, closing_amount_location] = (afs_quantity - sales_quantity) * afs_rate

        opening_quantity = afs_quantity - sales_quantity
        opening_amount = (afs_quantity - sales_quantity) * afs_rate

consolidated_data['Gross Profit'] = consolidated_data['Sales Amount'] - consolidated_data['COGS Amount']

# creating a summary output table with required columns and dropping extra columns
summary_data = consolidated_data.drop(['AFS Amount', 'AFS Rate', 'AFS Quantity',
                                       'COGS Quantity', 'Opening Quantity', 'Opening Amount',
                                       'Closing Quantity', 'Closing Amount',
                                       'Purchase Quantity', 'Purchase Amount', 'Average Purchase Price'], axis=1)

# exporting to CSV file
summary_data.to_csv('summary_data.csv')

