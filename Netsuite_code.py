#!/usr/bin/env python
# coding: utf-8

# In[1]:




class Netsuite_integration:
    def __init__(self):
        pass
    
    def convert_date(self, x):
        datetime_obj = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
        formatted_date = datetime_obj.strftime('%m/%d/%Y')
        return formatted_date
    def to_camel_case(self,s):
        words = s.split(' ')
        camel_case = ' '.join(word.capitalize() for word in words)
        return camel_case

    def category_coa_map(self,COA,input_df):
        coa_mapping = dict(zip(COA['Name'], COA['Number.1']))
        name_change = {'Pipe Tobacco 8oz':'Pipe Tobacco 8Oz', 'T-shirts':'T-Shirts', 'Pipe Tobacco 16oz':'Pipe Tobacco 16Oz',
               'Pipe Tobacco 0.7oz':'Pipe Tobacco 0.7Oz', '3d Piils':'3D Pills'}
        input_df['category'] = input_df['category'].replace(name_change)

        # Create a new column in exp1 using the mapping
        input_df['COA_values'] = input_df['category'].map(coa_mapping)
        return input_df

    

    # Converts cutsomer JSONs to netsuite template for customer. account_id is the most important one in this
    # table as it will be coming up in all other files like invoices, payments etc. Without the addition of a 
    # customer, netsuite does not accept any invoices or payments for that customer. This is a common error that
    # occurs from time to time. Need to think of a way to check this.
    def customer_template_csv(self, input_folder,is_sbt):
        files = os.listdir(input_folder)
        cust_dict = {
                "ExternalID": 'account_id',
                "Customer ID": 'account_id',
                "Individual": 'Yes',
                "Mr./Ms": np.nan,
                "First Name": 'firstname',
                "Middle Name": np.nan,
                "Last Name": 'lastname',
                "Job Title": np.nan,
                "Company Name": 'company',
                "Child Of": np.nan,
                "Status": 'Customer-Closed Won',
                "Subsidiary": 2,
                "Sales Rep": np.nan,
                "Partner": np.nan,
                "Web Address": np.nan,
                "Category": np.nan,
                "Default Order Priority": np.nan,
                "Comments": np.nan,
                "Email": 'email',
                "Alt. Email": np.nan,
                "Phone": 'storetelephone',
                "Alt. Phone": np.nan,
                "Mobile Phone": 'cellphonenumber',
                "Home Phone": np.nan,
                "Fax": np.nan,
                "Territory": np.nan,
                "Lead Source": np.nan,
                "Account": np.nan,
                "Default Receivables Account": np.nan,
                "Start Date": np.nan,
                "End Date": np.nan,
                "Reminder Days": np.nan,
                "Price Level": np.nan,
                "Primary Currency": 'USD',
                "Terms": np.nan,
                "Credit Limit": np.nan,
                "Hold": np.nan,
                "Pref. CC Processor": np.nan,
                "Tax Reg. Number": np.nan,
                "Taxable": np.nan,
                "Tax Item": np.nan,
                "Resale Number": np.nan,
                "Opening Balance": np.nan,
                "Opening Balance Date": np.nan,
                "Opening Balance Account": np.nan,
                "Language": np.nan,
                "Number Format": np.nan,
                "Negative Number Format": np.nan,
                "Email Preference": np.nan,
                "Print on Check As": np.nan,
                "Send Transaction Via Email": np.nan,
                "Send Transaction Via Fax": np.nan,
                "Send Transaction Via Print": np.nan,
                "Ship Complete": np.nan,
                "Shipping Carrier": np.nan,
                "Shipping Method": np.nan,
                "Give Access": np.nan,
                "Role": np.nan,
                "Send Notification Email": np.nan,
                "Password": np.nan,
                "Confirm Password": np.nan,
                "Inactive": np.nan,
                "CI VIA: Email": np.nan
            }
        file_num=0
        columns = list(cust_dict.keys())

        custdf = pd.DataFrame(columns=columns)

        for file in files:
            if file!='.DS_Store':
                custdata = json.load(open(input_folder + '/' + file))

                row_values = []
                for column, key in cust_dict.items():
                    if column == 'Individual':

                        if custdata['company'] != None:
                            value = 'No'
                        else:
                            value = 'Yes'


                    else:
                        try:
                            value = custdata[key]
                        except KeyError as e:
                            value = key
                        except Exception as e:
                            print(f"An exception occurred: {e}")
                            value = key

                    row_values.append(value)
                custdf.loc[file_num] = row_values
                print(file.split('.')[0] + 'added')
                file_num+=1
            # create output folder if it doesnot exist
            if is_sbt:
                custdf['Customer ID'] = custdf['Customer ID'].replace(100001, 100004)
                custdf['ExternalID'] = custdf['ExternalID'].replace(100001, 100004)

        #custdf.to_csv(output_folder + '/'+'customer_data.csv', index=False)
        return custdf   
            
# Converts Customer JSON to customer address file for netsuite. Stores the addresses of the customers created
# by the above function
    def customer_address_csv(self, input_folder,is_sbt):
        files = os.listdir(input_folder)
        
        address_dict = {
                "Customer_External_ID": 'account_id',
                'Address_External_ID': np.nan,
                'Label': np.nan,
                "Attention": np.nan,
                "Addressee": np.nan,
                "Address_1": 'street',
                "Address_2": np.nan,
                "City": 'city',
                "Province/State": 'state',
                "Postal_Code/Zip": 'postcode',
                "Country": 'country_id',
                "Default_Billing": 'Yes',
                "Default_Shipping": 'Yes'
            }
        columns = list(address_dict.keys())
        addressdf = pd.DataFrame(columns=columns)

        file_num=0
        for file in files:
          if file!='.DS_Store':
            custdata = json.load(open(input_folder + '/' + file))
            
            row_values = []
            for column, key in address_dict.items():
                if column == "Address_1":
                    value = custdata[key][0]
                else:  
                    try:
                        value = custdata[key]
                    except:
                        value = key
                row_values.append(value)

            addressdf.loc[file_num] = row_values
#             addressdf.loc[file_num, 'Label'] = 'Bill-To'
#             addressdf.loc[file_num+1] = row_values
#             addressdf.loc[file_num+1, 'Label'] = 'Ship-To'
            
            print(file.split('.')[0] + ' added')
            file_num+=1
            # address ids are just created by the index number. is this right?
        if is_sbt:
            addressdf['Customer_External_ID'] = addressdf['Customer_External_ID'].replace('100001', '100004')
            
        addressdf['Address_External_ID'] = 'ADD00' + addressdf['Customer_External_ID']
        
        
#         addressdf["Default_Billing"] = np.where(addressdf["Label"].str.contains("Bill-To"), 'Yes', '')
#         addressdf["Default_Shipping"] = np.where(addressdf["Label"].str.contains("Ship-To"), 'Yes', '')

        return addressdf
    # Creation of Vendor template for Netsuite from Vendor JSON. Similar to Customer creation, if Vendor ID
    # is not there in netsuite, it doesnot accept POs and vendor payments.
    def vendor_template_csv(self, input_folder):
        files = os.listdir(input_folder)
        vendcols = ['ExternalID', 'VendorID', 'Individual', 'Inactive', 'Represents_Subsidiary', 'FirstName',
                        'MiddleName', 'LastName', 'CompanyName', 'PrintonCheckAs',
                        'Category', 'PrimarySubsidiary', 'Phone', 'Fax', 'Email', 'Comments', 'Email_Preference',
                        'SendTransactionViaEmail', 'SendTransactionViaFax', 'SendTransactionViaPrint',
                        'Legal_Name', 'Account', 'Terms', 'Default_Expense_Account', 'Default_Payables_Account',
                        'Credit_Limit', 'Incoterm', 'TaxID', '1099_Eligible', 'Opening_Balance', 'Opening_Balance_Date',
                        'Opening_Balance_Account', 'VendorBill-Purchase_Order_Quantity_Tolerance',
                        'VendorBill-Purchase_Order_Amount_Tolerance', 'VendorBill-Purcahse_Order_Quantity_Difference',
                        'VendorBill-Item_Receipt_Quantity_Tolerance', 'VendorBill-Item_Receipt_Amount_Tolerance',
                        'VendorBill-Item_Receipt_Quantity_Difference',
                        'Primary_Currency', 'Additional_Currency_1', 'Additional_Currency_2']
        
        vendict = dict.fromkeys(vendcols, np.nan)

        vendict['VendorID'] = 'sup_id'
        vendict['ExternalID'] = 'sup_id'
        vendict['CompanyName'] = 'sup_name'
        vendict['PrimarySubsidiary'] = '2'
        vendict['Phone'] = 'sup_tel'
        vendict['Fax'] = 'sup_fax'
        vendict['Email'] = 'sup_mail'
        vendict['Primary_Currency'] = 'sup_currency'
        
        columns = vendcols
        vendf = pd.DataFrame(columns=columns)
            
        file_num = 0
        for file in files:
         if file!='.DS_Store':
            vendata = json.load(open(input_folder + '/' + file))
            row_values = []
            
            first_name = None
            last_name = None
            middle_name = None

            if vendata['sup_contact']:
                names = vendata['sup_contact'].split(' ')

                if len(names) ==2:
                    first_name = names[0]

                    last_name = names[1]
                elif len(names)==3:
                    first_name = names[0]

                    middle_name = names[1]
                    last_name=names[2]
                elif len(names)>3:
                    first_name = names[0]

                    middle_name = names[1]
                    last_name=' '.join(names[2:])
                
                else:
                    last_name=np.nan
                    first_name = vendata['sup_contact']

                # Assign values to columns
            for column, key in vendict.items():
                if column == 'FirstName':
                    value = first_name
                elif column == 'LastName':
                    value = last_name
                elif column == 'MiddleName':
                    value = middle_name

                elif column == 'Individual':
                    value = 'No'
                elif column == 'Email':
                    if vendata[key]:
                        value = vendata[key].split(';')[0]
                else:
                    try:
                        value = vendata[key]
                    except:
                        value = key
                row_values.append(value)
            
            vendf.loc[file_num] = row_values
            print(file.split('.')[0] + 'added')
            file_num+=1

        return vendf
    
    # Similar to customer address creation, this takes the same vendor JSON and extracts addresses of the vendors
    def vendor_address_csv(self, input_folder):
        files = os.listdir(input_folder)
        vendor_address_dict = {"Vendor_External_ID": 'sup_id', 'Address_External_ID': np.nan,
                                   'Label': np.nan, "Attention": np.nan,
                                   "Addressee": np.nan,
                                   "Address_1": 'sup_address1',
                                   "Address_2": np.nan,
                                   "City": 'sup_city',
                                   "Province/State": 'sup_region',
                                   "Postal_Code/Zip": 'sup_zipcode',
                                   "Country": 'sup_country',
                                   "Default_Billing": 'Yes',
                                   "Default_Shipping": 'Yes'}

        columns = list(vendor_address_dict.keys())
        vendor_addressdf = pd.DataFrame(columns=columns)
        file_num=0
        for file in files:
          if file!='.DS_Store':
            vendata = json.load(open(input_folder + '/' + file))
            
            row_values = []
            for column, key in vendor_address_dict.items():
                try:
                    value = vendata[key]
                    
                except:
                    value = key
                row_values.append(value)

            vendor_addressdf.loc[file_num] = row_values
#             
            file_num+=1
#         
        vendor_addressdf['Address_External_ID'] = 'ADDV00' + vendor_addressdf['Vendor_External_ID']

        return vendor_addressdf 
        
  # Bills that are generated by vendors when we order their product. This is also called PO (Purchase Order)
    # This function converts PO JSONs to a csv storing the required information.
    def Vendor_bill(self, input_folder):
        files = os.listdir(input_folder)
        
        ven_bill_cols = ['External ID','Vendor','Reference_number','Date','Subsidiary','Class','Memo',
                 'Item','Description','Quantity','Rate','Amount','Item level Class','Location']
        ven_bill_df_main = pd.DataFrame(columns=ven_bill_cols)

        file_num=0
        for file in files:
         if file!='.DS_Store':
            ven_bill_df = pd.DataFrame(columns=ven_bill_cols)

            ven_bill_data = json.load(open(input_folder + '/' + file))
            categories_amount = {}
#             date_str = ven_bill_data['po_invoice_date']
#             date_obj = datetime.strptime(date_str, '%Y-%m-%d')
#             if date_obj.month <= 6:
                
            try :
                for item in ven_bill_data['items']:
                    category = item['pop_category_name']
                    if category==None:
                        if item['pop_product_id'] == '6594':
                            category = 'AIRFRESHNER & INCENSE'
                            print(category)
                        elif item['pop_product_id'] == '10283':
                            category = 'HOOKAH & PIPES'
                            print(category)
                        elif item['pop_product_id'] == '2596':
                            category = 'CANDY & GUMS'
                            print(category)
                        
                    if category in categories_amount:
                        categories_amount[category][1] = categories_amount[category][1] + float(item['row_total'])
                        categories_amount[category][0] = categories_amount[category][0] + int(item['pop_qty'])

                    else:
                        categories_amount[category] = [int(item['pop_qty']),float(item['row_total'])]
                ven_bill_df['Item'] = categories_amount.keys()
                ven_bill_df['Quantity'] = [qty for qty, _ in categories_amount.values()]
                ven_bill_df['Amount'] = [Decimal(f"{round(amt,2):.2f}" )for _, amt in categories_amount.values()]
                ven_bill_df['Date'] = ven_bill_data['po_created_at']
                ven_bill_df['External ID'] = ven_bill_data['po_num']
                ven_bill_df['Vendor'] = ven_bill_data['po_sup_num']
                ven_bill_df['Reference_number'] = np.nan
                ven_bill_df['Subsidiary'] = 2
                ven_bill_df['Description'] = np.nan
                ven_bill_df['Rate'] = 1
                ven_bill_df['Location'] = np.nan
                file_num+=1
                ven_bill_df_main = ven_bill_df_main.append(ven_bill_df)
            except:
                continue
                
        ven_bill_df_main['Date'] = pd.to_datetime(ven_bill_df_main['Date'])
        return ven_bill_df_main
        
    # This is for payments done by customers (gas stations) who buy products from us. This converts customer 
    # payment JSONs to csv in the format netsuite requires. Note that every payment needs to have the customer
    # account id and also the invoice it is being paid for. This is a requirement for netsuite, the absence
    # of which throws errors.
    def Customer_payment(self, input_folder):
        cust_payment_cols = ['External_ID','Customer','Date','Account','Class','Memo',
                 'Invoice_ID','Amount']
        cust_payment_df_main = pd.DataFrame(columns=cust_payment_cols)

        files = os.listdir(input_folder)
        for file in files:
            if file!='.DS_Store':
                cust_payment_data = json.load(open(input_folder+'/'+ file))
                for payment in cust_payment_data:
                    cust_pay_dict = dict.fromkeys(cust_payment_cols, np.nan)

                    cust_pay_dict['External_ID'] = payment['transaction_id']
                    cust_pay_dict['Customer'] = payment['account_id']
                    cust_pay_dict['Date'] = payment['created_at']
                    cust_pay_dict['Account'] = np.nan
                    cust_pay_dict['Subsidiary'] = 2
                    cust_pay_dict['Class'] = np.nan
                    cust_pay_dict['Memo'] = np.nan
                    cust_pay_dict['Invoice_ID'] = payment['txn_id']
                    cust_pay_dict['Amount'] = payment['amount']
                    cust_payment_df_main = cust_payment_df_main.append(cust_pay_dict,ignore_index = True)
                    #print(len(cust_payment_df_main))

                #ven_bill_df = ven_bill_df.drop(ven_bill_df.index)
        cust_payment_df_main['Date'] = cust_payment_df_main['Date'].apply(lambda x: self.convert_date(x))
        cust_payment_df_main['Date'] = pd.to_datetime(cust_payment_df_main['Date'])
        return cust_payment_df_main
      
    ## This function is for vendor payments i.e they payments we make to vendor when we buy products in bulk
    # from them. It converts the JSONs in the input_folder to a csv file. 
    def Vendor_transaction(self, input_folder):
        cols = ['transaction_id','supplier_id','amount','created_at']
        df = pd.DataFrame(columns = cols)

        payment_files = os.listdir(input_folder)
        row_num=0
        for file in payment_files:
            if file != '.DS_Store':
                ven_payment = json.load(open(input_folder+'/'+file)) 

                for transaction in ven_payment:
                    row = []
                    for col in cols:
                        value = transaction[col]
                        row.append(value)
                    df.loc[row_num]=row
                    row_num+=1
        df['amount'] = df['amount'].astype(float)
        df['amount'] = df['amount'].apply(lambda x: Decimal(f"{round(x,2):.2f}" ))
        #Decimal(f"{round(df['amount'].astype(float),2):.2f}" )
        df['created_at'] = pd.to_datetime(df['created_at'])
        #ven_bill_df = ven_bill_df[ven_bill_df['Date'].dt.year != 2022]
        
        #df = df[df['created_at'].dt.month <= 6]
        return df

        
    
    
    
    
    def get_invoice_amount(self,invoice_id,balance_invoice_amount_dict,invoice_df):
        try:
            amount = balance_invoice_amount_dict[invoice_id]
        except:
            amount = invoice_df['Amount']
        return amount
    
    # this is an algorithm to connect vendor transactions to their bills. This might not be used in future.

    def vendor_payment_po_link(self,ven_bill_df,transactions_df):
        ven_bill_df['Date'] = ven_bill_df['Date'].astype(str)

# Filter rows where 'date' starts with "0023" and replace "0023" with "2023"
        ven_bill_df.loc[ven_bill_df['Date'].str.startswith('0023'), 'Date'] = ven_bill_df['Date'].str.replace('0023', '2023')

        carryover_cols = ['Vendor_id','Transaction_id','Invoice_id','Invoice_balance_amount','Transaction_balance_amount']

        next_month_carryover = pd.DataFrame(columns = carryover_cols)
        
        #transactions_df = pd.DataFrame(df)
        ven_bill_df_grouped = ven_bill_df.groupby(['Vendor','External ID','Date'],as_index=False)['Amount'].sum()
        # Convert 'date' column to datetime in both DataFrames
        ven_bill_df_grouped['Date'] = pd.to_datetime(ven_bill_df_grouped['Date'])
        transactions_df['created_at'] = pd.to_datetime(transactions_df['created_at'])

        # Sort both DataFrames by date in ascending order
        invoices_df = ven_bill_df_grouped.sort_values(by='Date', ascending=True)
        transactions_df = transactions_df.sort_values(by='created_at', ascending=True)

        # Create a new DataFrame to store the results
        result_df = pd.DataFrame(columns=[
            'sup_id', 'transac_id', 'po_id', 'po_amount', 'og_transaction_amount','final_transaction_amount',
            'amount_left_in_transaction', 'amount_left_in_invoice','complete_invoice_satisfied'
        ])

        # Group invoices and transactions by supplier
        invoices_grouped = invoices_df.groupby('Vendor')
        transactions_grouped = transactions_df.groupby('supplier_id')

        # Loop through each invoice of each supplier
        is_transaction_available = False
        added_invoices = set()
        balance_invoice_amount = {}

        #this is for carryover dataframe. If transactions are voided then whatever is left in the invoice is carried over
        #and vice versa
        transaction_bool = True
        # for each supplier
        transaction_no_invoice = []
        for supplier, supplier_transactions in transactions_grouped:
            # here we are checking if transactions of that supplier are existing in our transactions df
            try:
                supplier_invoices = invoices_grouped.get_group(int(supplier))
                is_invoice_available= True
            except:
                is_invoice_available= False
                pass
            if is_invoice_available!=True:
                        transaction_no_invoice.append(supplier)

            # if the transaction is available
            else:
                #for each transaction of that supplier
                for transac_index,transaction in supplier_transactions.iterrows():
                   
                    # for each invoice of that supplier
                    for invoice_index,invoice in supplier_invoices.iterrows():
                           
                        # check if invoice data is before transaction date. Because bill is always before the payment
        #                 if invoice['Date']<transaction['created_at']:

                            # if transaction is more than invoice amount then it is straightforward i.e that invoice is 
                            # satisfied by the transaction so update accordingly (subtract invoice amount from transaction
                            #amount and update this transaction amount forever which means this amount is used for that
                            # transaction id from next time)
                            mod_invoice_amount = self.get_invoice_amount(invoice['External ID'],balance_invoice_amount,invoice)
                            if transaction['amount'] >= mod_invoice_amount:
                                #print(1)
                                amount_left_in_transaction = float(transaction['amount']) - float(mod_invoice_amount)
                                if invoice['External ID'] in added_invoices:
                                    continue

                                # Add the invoice ID to the set to mark it as added
                                added_invoices.add(invoice['External ID'])
                                
                                result_df = result_df.append({
                                    'sup_id': supplier,
                                    'transac_id': transaction['transaction_id'],
                                    'po_id': invoice['External ID'],
                                    'po_amount': mod_invoice_amount,
                                    'og_transaction_amount': transaction['amount'],
                                    'final_transaction_amount':float(transaction['amount'])-float(amount_left_in_transaction),
                                    'final_po_amount':float(mod_invoice_amount),
                                    'amount_left_in_transaction': amount_left_in_transaction,
                                    'amount_left_in_invoice':0,
                                    'complete_invoice_satisfied': 'Yes',
                                    'date':transaction['created_at']
                                }, ignore_index=True)
                                supplier_invoices.drop(invoice_index, inplace=True)

                                transaction['amount'] = amount_left_in_transaction
                            # if invoice is more than transaction amount then void the transaction amount forever, subtract
                            # the transaction amount from the invoice amount and update that balance invoice amount to the
                            # invoice forever. So that when it is called next this new amount should be used because the rest
                            # of it was paid by the transaction. This is done using balance invoice dict

                            elif transaction['amount'] < invoice['Amount']:
                                #print(2)
                                mod_invoice_amount = self.get_invoice_amount(invoice['External ID'],balance_invoice_amount,invoice)
                                amount_left_in_invoice =  float(mod_invoice_amount) - float(transaction['amount'])
                                
                                result_df = result_df.append({
                                    'sup_id': supplier,
                                    'transac_id': transaction['transaction_id'],
                                    'po_id': invoice['External ID'],
                                    'po_amount': self.get_invoice_amount(invoice['External ID'],balance_invoice_amount,invoice),
                                    'og_transaction_amount': transaction['amount'],
                                    'final_transaction_amount':float(transaction['amount']),
                                    'final_po_amount':float(mod_invoice_amount) - float(amount_left_in_invoice),
                                    'amount_left_in_transaction': 0,
                                    'amount_left_in_invoice':amount_left_in_invoice,
                                    'complete_invoice_satisfied': 'No',
                                    'date':transaction['created_at']
                                }, ignore_index=True)
                                balance_invoice_amount[invoice['External ID']] = amount_left_in_invoice

                                break
        #print(result_df)
        result_df['date'] = result_df['date'].apply(lambda x: x.normalize())
        result_df['og_transaction_amount'] = result_df['og_transaction_amount'].apply(lambda x: Decimal(f"{round(x,2):.2f}" ))
        result_df['final_transaction_amount'] = result_df['final_transaction_amount'].apply(lambda x: Decimal(f"{round(x,2):.2f}" ))
        result_df['final_po_amount'] = result_df['final_po_amount'].apply(lambda x: Decimal(f"{round(x,2):.2f}" ))
        print(transaction_no_invoice)
        vendor_payment_df_final = result_df.copy()
        vendor_payment_df_final = vendor_payment_df_final[['transac_id','sup_id','po_id','final_po_amount','final_transaction_amount','date']]
        vendor_payment_df_final = vendor_payment_df_final.rename(columns={
            'transac_id': 'Payment_id',
            'sup_id': 'Vendor_id',
            'po_id':'Bill_id',
            'final_po_amount':'Bill_amount',
            'final_transaction_amount': 'Payment_amount',
            'date':'Date'
        })
        vendor_payment_df_final['Vendor_id'] = vendor_payment_df_final['Vendor_id'].astype('int')


        return vendor_payment_df_final,result_df
    def Carry_over(self,result_df):
        unique_suppliers = result_df['sup_id'].unique()

        # Create an empty DataFrame to store the results
        carry_over_df = pd.DataFrame(columns=result_df.columns)

        # Loop through each unique supplier ID
        for supplier_id in unique_suppliers:
            # Filter the DataFrame based on the current supplier ID
            supplier_df = result_df[result_df['sup_id'] == supplier_id]

            # Get the last row for each supplier (latest information)
            last_row = supplier_df.iloc[-1]

            # Append the last row to the result DataFrame
            carry_over_df = carry_over_df.append(last_row, ignore_index=True)
        return carry_over_df
    
    # This function extracts the sales information from the invoice JSONs. Here apart from sales, 3 types of 
    # taxes are being captured ('prepay_tax', 'postpay_tax', 'al_otp_tax'). These are first captured as column
    # values and then melted into rows. This is done for netsuite to ingest it in a certain way. The taxes
    # hit a different account and the sales hit a different account so it is important to segregate these.
    def Invoice_final(self,input_folder,is_sbt):
        req = ['invoice_id','invoice_store_info','invoice_number','invoice_created_at','entity_id', 'product_id', 'sku'
               , 'product', 'qty', 'price', 'cost', 'prepay_tax', 'postpay_tax', 'al_otp_tax', 'row_total', 'profit', 'category','invoice_url']
        files = os.listdir(input_folder)
        counter = 1
        anomaly = []
        df_main = pd.DataFrame(columns = req)
        for file in files:
            #print(file)
            if file != '.DS_Store':
                try:
                    data = json.load(open(input_folder + '/' + file))

                    cat_data = data.pop("items")
                    df_new = pd.DataFrame([data] * len(cat_data))
                    df_new = df_new.assign(**pd.DataFrame(cat_data))

                    df_new=df_new[req]
                    df_new['Customer_id'] = df_new['invoice_store_info'].apply(lambda x: x['account_id'])
                    
                    df_new['Created_at'] = df_new['invoice_created_at'].apply(lambda x: self.convert_date(x))
                    #print(df_new['invoice_id'],' ',df_new['invoice_number'])
                    df_main = df_main.append(df_new)
                    #print(file.split('.')[0] + 'added')
                except:
                    
                    anomaly.append(data['invoice_number'])
                    continue
                 
            else:
                pass
        df_main = df_main.drop(['invoice_created_at','invoice_store_info'],axis=1)
        df_main_exp = df_main.copy()
        df_main_exp = df_main_exp.drop(['entity_id','product_id','sku','product'],axis = 1)
        
        df_main_exp[['qty', 'price', 'cost', 'prepay_tax', 'postpay_tax', 'al_otp_tax',
       'row_total', 'profit']] = df_main_exp[['qty', 'price', 'cost', 'prepay_tax', 'postpay_tax', 'al_otp_tax',
       'row_total', 'profit']].astype('float')
        
        df_main_exp['revenue'] = df_main_exp['price']*df_main_exp['qty']
        df_main_exp['prepay_tax'] = df_main_exp['prepay_tax']*df_main_exp['qty']
        df_main_exp['postpay_tax'] = df_main_exp['postpay_tax']*df_main_exp['qty']
        df_main_exp['al_otp_tax'] = df_main_exp['al_otp_tax']*df_main_exp['qty']
        df_main_exp = df_main_exp.drop(['price'],axis=1)

        print(df_main_exp.columns)

        df_main_exp_grouped = df_main_exp.groupby(['invoice_id', 'invoice_number','invoice_url','Created_at','Customer_id','category']).sum().reset_index()
        
        
        
        df_main_exp_grouped=df_main_exp_grouped.rename(columns = {'prepay_tax':'Prepay Tax', 'postpay_tax': 'Postpay Tax', 'al_otp_tax':'AL_Otp_Tax'})
        
        df_main_exp_grouped['category'] = df_main_exp_grouped['category'].apply(self.to_camel_case)

        columns_to_melt = ['Prepay Tax', 'Postpay Tax', 'AL_Otp_Tax']

        # List of columns that should stay as identifiers
        id_vars = ['invoice_id', 'invoice_number', 'Customer_id','revenue','invoice_url','category','Created_at','qty']

        # Use melt to reshape the dataframe
        melted_df = pd.melt(df_main_exp_grouped, 
                            id_vars=id_vars, 
                            value_vars=columns_to_melt, 
                            var_name='Tax_Type', 
                            value_name='Tax_Value')
        
        invoice_data = df_main_exp_grouped.drop(['cost','Prepay Tax', 'Postpay Tax', 'AL_Otp_Tax', 'row_total', 'profit'],axis=1)
        invoice_data = invoice_data.rename(columns = {'price':'amount'})
        
        invoice_tax = melted_df.copy()

        postpay_taxes = invoice_tax[invoice_tax['Tax_Type'] == 'Postpay Tax'].groupby(['invoice_id','invoice_number','Customer_id','Created_at'])['Tax_Value'].sum().reset_index()

        # Renaming columns for merging and creating additional columns to match original dataframe structure
        #postpay_taxes.rename(columns={'Tax_Value': 'revenue'}, inplace=True)
        postpay_taxes['category'] = 'Total_postpay_taxes'
        postpay_taxes['Tax_Type'] = ' '

        # Appending the summarized postpay taxes to the original dataframe
        invoice_tax = pd.concat([invoice_tax, postpay_taxes], ignore_index=True)


        invoice_tax = invoice_tax[invoice_tax['Tax_Type'] != 'Postpay Tax']
        
        invoice_tax['category'] = invoice_tax['category'] + " " + invoice_tax['Tax_Type']
        
        
        invoice_tax = invoice_tax.drop(['Tax_Type'],axis=1)

        invoice_tax = invoice_tax.rename(columns = {'Tax_Value':'amount'})
        result = pd.concat([invoice_data, invoice_tax], ignore_index=True)
        result['revenue'] = np.where(result['amount'].notna(), result['amount'], result['revenue'])
        result = result.drop('amount',axis=1)
        result = result.rename(columns = {'qty':'quantity'})
        result = result.sort_values(by='invoice_id')
        result = result.reset_index(drop=True)
        result['quantity'] = result['quantity'].fillna(1)
        filtered_invoice = result[result['revenue']!=0]
        
        if is_sbt:
            filtered_invoice['Customer_id'] = filtered_invoice['Customer_id'].replace('100001', '100004')
        return filtered_invoice
    
    # this is a dataframe created from the invoice JSONs. This is not used in production. It is just
    # used to create the next COGS and Preprocess Journal entries. A more efficient way would be to create this
    # while creating the invoice itself.
    
    def preprocess_JE(self,input_folder):
        req = ['invoice_id','invoice_store_info','invoice_number','invoice_created_at','entity_id', 'product_id', 'sku'
               , 'product', 'qty', 'price', 'cost', 'prepay_tax', 'postpay_tax', 'al_otp_tax', 'row_total', 'profit', 'category','invoice_url']
        files = os.listdir(input_folder)
        counter = 1
        anomaly = []
        df_main = pd.DataFrame(columns = req)
        for file in files:
            #print(file)
            if file != '.DS_Store':
                try:
                    data = json.load(open(input_folder + '/' + file))

                    cat_data = data.pop("items")
                    df_new = pd.DataFrame([data] * len(cat_data))
                    df_new = df_new.assign(**pd.DataFrame(cat_data))

                    df_new=df_new[req]
                    df_new['Customer_id'] = df_new['invoice_store_info'].apply(lambda x: x['account_id'])
                    
                    df_new['Created_at'] = df_new['invoice_created_at'].apply(lambda x: self.convert_date(x))
                    #print(df_new['invoice_id'],' ',df_new['invoice_number'])
                    df_main = df_main.append(df_new)
                    #print(file.split('.')[0] + 'added')
                except:
                    
                    anomaly.append(data['invoice_number'])
                    continue
                 
            else:
                pass

        df_main = df_main.drop(['invoice_created_at','invoice_store_info'],axis=1)
        df_main_exp = df_main.copy()
        df_main_exp = df_main_exp.drop(['entity_id','product_id','sku','product'],axis = 1)
        
        df_main_exp[['qty', 'price', 'cost', 'prepay_tax', 'postpay_tax', 'al_otp_tax',
       'row_total', 'profit']] = df_main_exp[['qty', 'price', 'cost', 'prepay_tax', 'postpay_tax', 'al_otp_tax',
       'row_total', 'profit']].astype('float')
        
        df_main_exp['total_cost'] = df_main_exp['cost']*df_main_exp['qty']
        df_main_exp['prepay_tax'] = df_main_exp['prepay_tax']*df_main_exp['qty']
        df_main_exp['postpay_tax'] = df_main_exp['postpay_tax']*df_main_exp['qty']
        df_main_exp['al_otp_tax'] = df_main_exp['al_otp_tax']*df_main_exp['qty']
        df_main_exp = df_main_exp.drop(['price','cost','qty'],axis=1)

        

        df_main_exp_grouped = df_main_exp.groupby(['invoice_id', 'invoice_number','invoice_url','Created_at','Customer_id','category']).sum().reset_index()
        
        
        
        df_main_exp_grouped=df_main_exp_grouped.rename(columns = {'prepay_tax':'Prepay Tax', 'postpay_tax': 'Postpay Tax', 'al_otp_tax':'AL_Otp_Tax'})
        
        df_main_exp_grouped['category'] = df_main_exp_grouped['category'].apply(self.to_camel_case)
        return df_main_exp_grouped
    
    def category_name_correction(self,df):
        corrections_dict = {'3d Pills':'3D Pills',
        'Pipe Tobacco 0.7oz':'Pipe Tobacco 0.7Oz', 'Pipe Tobacco 12oz':'Pipe Tobacco 12Oz',
           'Pipe Tobacco 16oz':'Pipe Tobacco 16Oz', 'Pipe Tobacco 3.5oz':'Pipe Tobacco 3.5Oz', 
        'Pipe Tobacco 3oz':'Pipe Tobacco 3Oz','Pipe Tobacco 5lb':'Pipe Tobacco 5Lb', 'Pipe Tobacco 5oz':'Pipe Tobacco 5Oz', 
           'Pipe Tobacco 6oz': 'Pipe Tobacco 6Oz','Pipe Tobacco 8oz':'Pipe Tobacco 8Oz'}
        df['category'] = df['category'].replace(corrections_dict)
        return df
    
    # Creation of Cost of Goods Sold jounal entry from the invoice JSONs. This basically involves cost  
    def COGS_JE_creation(self,grouped_data_cleaned):
        
        columns_to_remove_v2 = [ 'profit', 'row_total']

    # Removing the specified columns from grouped_data_cleaned
        grouped_data_cleaned_reduced_v2 = grouped_data_cleaned.drop(columns=columns_to_remove_v2)




        columns_to_remove_v3 = [ 'Postpay Tax', 'AL_Otp_Tax', 'Prepay Tax']

        # Removing the specified columns from grouped_data_cleaned_reduced_v2
        grouped_data_cleaned_reduced_v3 = grouped_data_cleaned_reduced_v2.drop(columns=columns_to_remove_v3)




        COA = pd.read_csv('Items with COA.csv')
        #grouped_data_cleaned_reduced_v3['category'] = grouped_data_cleaned_reduced_v3['category'].apply(to_camel_case)
        #grouped_data_cleaned_reduced_v3['category'] = grouped_data_cleaned_reduced_v3['category'].replace('3d Pills', '3D Pills')
        grouped_data_cleaned_reduced_v3 = self.category_name_correction(grouped_data_cleaned_reduced_v3)
        grouped_data_cleaned_reduced_v3 = self.category_coa_map(COA,grouped_data_cleaned_reduced_v3)
        JE_total_cost = grouped_data_cleaned_reduced_v3.copy()

        # Duplicate the rows in JE_total_cost
        JE_total_cost_duplicated = JE_total_cost.loc[JE_total_cost.index.repeat(2)].reset_index(drop=True)

        # Initialize 'debit' and 'credit' columns with NaN
        JE_total_cost_duplicated['debit'] = np.nan
        JE_total_cost_duplicated['credit'] = np.nan

        # Assign 'customer_id' to 'debit' and NaN to 'credit' for every second row (starting from 0)
        JE_total_cost_duplicated.loc[JE_total_cost_duplicated.index % 2 == 0, 'debit'] = JE_total_cost_duplicated['total_cost']
        # Assign 10300 to 'credit' and NaN to 'debit' for every second row (starting from 1)
        JE_total_cost_duplicated.loc[JE_total_cost_duplicated.index % 2 == 1, 'credit'] = JE_total_cost_duplicated['total_cost']

        JE_total_cost_duplicated['COA_values'] = np.where(JE_total_cost_duplicated['credit'].notna(), 10300, JE_total_cost_duplicated['COA_values'])

        JE_total_cost_duplicated = JE_total_cost_duplicated.drop(['invoice_id','category','total_cost','invoice_url','Customer_id'],axis=1)
        JE_total_cost_duplicated[['Approval_Status','Memo','Subsidiary','Class']] = np.nan
        JE_total_cost_duplicated = JE_total_cost_duplicated.rename(columns = {'Created_at':'Date','COA_values':'Account Code','invoice_number':'Line_Memo'
                                    })
        JE_total_cost_duplicated['External_ID'] = 'COGS' + JE_total_cost_duplicated['Line_Memo'].astype(str)

        new_column_order = [
        'External_ID', 'Date', 'Memo', 'Account Code', 'debit', 'credit', 
        'Line_Memo', 'Subsidiary', 'Class', 'Approval_Status'
    ]
        JE_total_cost_duplicated = JE_total_cost_duplicated[new_column_order]
        JE_total_cost_duplicated['Subsidiary'] = 2
        JE_total_cost_duplicated['Approval_Status'] = 'Approved'


        return JE_total_cost_duplicated

    def prepay_JE_creation(self,grouped_data_cleaned,start_id='137882'):
        prepay_data = grouped_data_cleaned[grouped_data_cleaned['Prepay Tax']!=0]

        ##prepay_data['total_prepay_tax'] = prepay_data['Prepay Tax']*prepay_data['qty'] 
        COA = pd.read_csv('Items with COA.csv')
        prepay_data = prepay_data.drop(['invoice_id','invoice_url','Customer_id',
                                       'Postpay Tax','AL_Otp_Tax','row_total','profit','category'],axis=1)


        JE_prepay_tax_duplicated = prepay_data.loc[prepay_data.index.repeat(2)].reset_index(drop=True)

        # Initialize 'debit' and 'credit' columns with NaN
        JE_prepay_tax_duplicated['debit'] = np.nan
        JE_prepay_tax_duplicated['credit'] = np.nan

        # Assign 'customer_id' to 'debit' and NaN to 'credit' for every second row (starting from 0)
        JE_prepay_tax_duplicated.loc[JE_prepay_tax_duplicated.index % 2 == 0, 'debit'] = JE_prepay_tax_duplicated['Prepay Tax']

        # Assign 10300 to 'credit' and NaN to 'debit' for every second row (starting from 1)
        JE_prepay_tax_duplicated.loc[JE_prepay_tax_duplicated.index % 2 == 1, 'credit'] = JE_prepay_tax_duplicated['Prepay Tax']
        JE_prepay_tax_duplicated['Account Code'] = np.where(JE_prepay_tax_duplicated['credit'].isna(), 50600, 10301)


        JE_prepay_tax_duplicated[['Approval_Status','Memo','Subsidiary','Class']] = np.nan
        JE_prepay_tax_duplicated = JE_prepay_tax_duplicated.rename(columns = {'Created_at':'Date','invoice_number':'Line_Memo'
                                    })
        #JE_prepay_tax_duplicated['External_ID'] = 'PT'+JE_prepay_tax_duplicated['Line_Memo'] .astype(str)
        
#         JE_prepay_tax_duplicated['External_ID'] = 'PT'+(100000 + ((JE_prepay_tax_duplicated.index+start_num-1) // 2)).astype(str)
        JE_prepay_tax_duplicated['External_ID'] = 'PT'+(start_id + 1 + (JE_prepay_tax_duplicated.index)//2).astype(str)
        new_column_order = [
        'External_ID', 'Date', 'Memo', 'Account Code', 'debit', 'credit', 
        'Line_Memo', 'Subsidiary', 'Class', 'Approval_Status'
    ]
        JE_prepay_tax_duplicated = JE_prepay_tax_duplicated[new_column_order]
        JE_prepay_tax_duplicated['Subsidiary'] = 2
        JE_prepay_tax_duplicated['Approval_Status'] = 'Approved'
        
        return JE_prepay_tax_duplicated
    
    def jul_sep_bank_transactions(start_id,file_path): #106176
      
        bank_transactions = pd.read_excel(file_path)#, sheet_name=sheet
        bank_transactions_out = bank_transactions[bank_transactions['Approval_Status']=='Approved']
        bank_transactions_out = bank_transactions_out[['Post Date','Description', 'Debit','Credit',
                    'Status', 'Account Code', 'Approval_Status',
                      'Bank']]
        expanded_expenses = pd.DataFrame(np.repeat(bank_transactions_out.values, 2, axis=0))


        # 2. Duplicate the dataset to handle the Debit column
        df_duplicates = bank_transactions_out.copy()
        df_duplicates['Credit'] = df_duplicates['Debit']
        df_duplicates['Debit'] = float('NaN')
        df_duplicates['Account Code'] = 10007

        # 3. Duplicate the dataset to handle the Credit column
        df_duplicates_credit = bank_transactions_out.copy()
        df_duplicates_credit['Debit'] = df_duplicates_credit['Credit']
        df_duplicates_credit['Credit'] = float('NaN')
        df_duplicates_credit['Account Code'] = 10007

        #4. Assign a unique ID to the original and the duplicates
        bank_transactions_out['ID'] = range(1, len(bank_transactions_out) + 1)
        df_duplicates['ID'] = bank_transactions_out['ID']
        df_duplicates_credit['ID'] = bank_transactions_out['ID']

        # # 5. Concatenate the original dataframe with the duplicates
        df_combined = pd.concat([bank_transactions_out, df_duplicates, df_duplicates_credit], ignore_index=True)

        # 6. Filter out rows where both Debit and Credit are NaN (extra duplicates)
        df_combined_filtered = df_combined.dropna(subset=['Debit', 'Credit'], how='all')

        # 7. Sort by ID to maintain the order
        df_combined_filtered = df_combined_filtered.sort_values(by='ID').reset_index(drop=True)
        df_combined_filtered = df_combined_filtered.sort_values(by=['ID', 'Debit'], ascending=[True, False]).reset_index(drop=True)

        df_combined_filtered['External_ID'] = 'EXP' + (start_id + 1 + (df_combined_filtered.index)//2).astype(str)
        df_combined_filtered['Line_Memo'] = df_combined_filtered['Bank'] 


        df_combined_filtered['Subsidiary'] = 2
        df_combined_filtered['Class'] = ''
        df_combined_filtered['Approval_Status'] = 'Approved'
        df_combined_filtered = df_combined_filtered.rename(columns={'Description': 'Memo','Debit':'debit','Credit':'credit'})

        new_column_order = [
            'External_ID', 'Post Date', 'Memo', 'Account Code', 'debit', 'credit',
            'Line_Memo', 'Subsidiary', 'Class', 'Approval_Status'
        ]

        df_combined_filtered = df_combined_filtered[new_column_order]

        df_combined_filtered['Account Code'] = df_combined_filtered['Account Code'].astype('int')
        df_combined_filtered['Account Code'] = df_combined_filtered['Account Code'].replace(60664, 60064)
        df_combined_filtered = df_combined_filtered.rename(columns={'Post Date':'Date'})
        # credit_notna_mask = df_combined_filtered['Credit'].notna()
        # df_combined_filtered.loc[credit_notna_mask & (df_combined_filtered['Bank'] == 'Progress Bank'), 'Account Code'] = 10007
        # df_combined_filtered.loc[credit_notna_mask & (df_combined_filtered['Bank'] == 'American Express Platinum '), 'Account Code'] = 20009
        # df_combined_filtered.loc[credit_notna_mask & (df_combined_filtered['Bank'] == 'American Express Plum'), 'Account Code'] = 20008
        return df_combined_filtered
    
    
    def bank_JE_creation(self,file_path,start_id):
        xls = pd.ExcelFile(file_path)
        sheets = xls.sheet_names
        #file_path = '/Users/preetham7/Downloads/Jan - June 2023 - Code 10020.xlsx'

        bank_je_list = {sheet: pd.read_excel(file_path, sheet_name=sheet) for sheet in sheets}
        original_df = pd.concat(bank_je_list.values())

        # Reload the original Excel file
        original_df = original_df.reset_index(drop=True)
        # Create an additional 'sort_index' column in the original dataframe to later enable consecutive sorting
        original_df['sort_index'] = original_df.index

        # Initialize an empty DataFrame for duplicates with the same columns including 'sort_index'
        duplicated_rows = pd.DataFrame(columns=original_df.columns)

        # Iterate over the original dataframe to create duplicate rows
        for index, row in original_df.iterrows():
            # Create a copy of the current row to modify for the duplicate
            new_row = row.copy()
            if pd.notna(row['Credit']):
                new_row['Debit'] = new_row['Credit']  # Move 'Credit' to 'Debit'
                new_row['Credit'] = pd.NA  # Set 'Credit' to NaN
                new_row['Account Code'] = 10007  # Change 'Account Code' to 10007
            elif pd.notna(row['Debit']):  # If there's a value in 'Debit', this assumes such a case exists
                new_row['Credit'] = new_row['Debit']  # Move 'Debit' to 'Credit'
                new_row['Debit'] = pd.NA  # Set 'Debit' to NaN
                new_row['Account Code'] = 10007  # Change 'Account Code' to 10007
            # Append the new row to the duplicates DataFrame without changing the 'sort_index'
            duplicated_rows = duplicated_rows.append(new_row, ignore_index=True)

        # Now combine the original dataframe with the duplicated rows
        df_combined = pd.concat([original_df, duplicated_rows])


        column_order = ['Account Number', 'Post Date', 'Description', 'Debit', 'Credit', 'Account Code', 'Approval_Status', 'sort_index']
        df_reordered = df_combined[column_order]

        df_reordered.sort_values(by=['sort_index', 'Debit'], ascending=[True, False], inplace=True)

        # Drop the 'sort_index' column as it is no longer needed
        df_final = df_reordered.drop('sort_index', axis=1)
        df_final.reset_index(drop=True, inplace=True)

        df_final['External_ID'] = 'EXP' + (start_id + 1 + (df_final.index//2)).astype(str)
        # Reset the index to finalize the DataFrame
        #df_final = df_final.drop('Account Number',axis=1)
        df_final = df_final.rename(columns = {'Description':'Memo'})
        df_final['Line_Memo'] = np.nan
        df_final['Subsidiary']=2
        df_final['Class']=''
        column_order = ['External_ID', 'Post Date', 'Memo', 'Account Code', 'Debit', 'Credit', 'Approval_Status', 'Line_Memo','Class','Subsidiary']
        df_final = df_final[column_order]
        return df_final
    
    def save_file(self,folder_path,file_name,file):
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        file_path = folder_path + file_name
        file.to_csv(file_path+'.csv')
        
        



# Create an instance of the DataConverter class
converter = Netsuite_integration()


# In[ ]:


def output_dict_creation(date,master_folder):
    output_folder_dict = {'customer':master_folder+'/'+date+'/'+'customer/','invoice':master_folder+'/'+date+'/'+'invoice/','po':master_folder+'/'+date+'/'+'po/'
                     ,'vendor_txn':master_folder+'/'+date+'/'+'vendor_payments/','customer_balance':master_folder+'/'+date+'/'+'customer_payments/','vendor':master_folder+'/'+date+'/'+'vendor/'
                     ,'sbt_invoice':master_folder+'/'+date+'/'+'sbt_invoice/'}
    return output_folder_dict


# In[ ]:



def netsuite_functions_run(input_folder,output_folder_dict,date,prepay_start_id):
    folders = os.listdir(input_folder)
    for folder in folders:
            if folder == 'customer':
                filename = 'customers_'+date
                cust = converter.customer_template_csv(input_folder+folder, False)
                converter.save_file(output_folder_dict[folder],filename,cust)
                
                filename = 'customer_adresses_'+date
                cust_add = converter.customer_address_csv(input_folder+folder, False)
                converter.save_file(output_folder_dict[folder],filename,cust_add)
                
            elif folder == 'vendor':
                filename = 'vendor_'+date
                ven = converter.vendor_template_csv(input_folder+folder)
                converter.save_file(output_folder_dict[folder],filename,ven)
                
                filename = 'vendor_adresses_'+date
                ven_add = converter.vendor_address_csv(input_folder+folder)
                converter.save_file(output_folder_dict[folder],filename,ven_add)
                
            elif folder == 'invoice':
                invoices = converter.Invoice_final(input_folder+folder,False)
                filename = 'invoices_'+date
                converter.save_file(output_folder_dict[folder],filename,invoices)
                
                preprocess = converter.preprocess_JE(input_folder+folder)
                #prepay_JE
                prepay = converter.prepay_JE_creation(preprocess,prepay_start_id)
                filename = 'prepay_JE_'+date
                converter.save_file(output_folder_dict[folder],filename,prepay)
                #COGS_JE
                COGS = converter.COGS_JE_creation(preprocess)
                filename = 'COGS_JE_'+date
                converter.save_file(output_folder_dict[folder],filename,COGS)
                
            elif folder == 'sbt_invoice':
                print('y')
                invoices = converter.Invoice_final(input_folder+folder,True)
                filename = 'invoices_'+date
                converter.save_file(output_folder_dict[folder],filename,invoices)
                
                preprocess = converter.preprocess_JE(input_folder+folder)
# #                 #prepay_JE
# #                 prepay = converter.prepay_JE_creation(preprocess,prepay_start_id)
# #                 filename = 'prepay_JE_'+date
# #                 converter.save_file(output_folder_dict[folder],filename,prepay)
#                 #COGS_JE
                COGS = converter.COGS_JE_creation(preprocess)
                filename = 'COGS_JE_'+date
                converter.save_file(output_folder_dict[folder],filename,COGS)
                
            elif folder == 'po':
                filename = 'vendor_bills_'+date
                venbill = converter.Vendor_bill(input_folder+folder)
                converter.save_file(output_folder_dict[folder],filename,venbill)
            
            elif folder == 'customer_balance':
                filename = 'customer_payments_'+date
                custpay = converter.Customer_payment(input_folder+folder)
                adjustments = custpay[custpay['Invoice_ID']=='']
                payments = custpay[~(custpay['Invoice_ID']=='')]

                converter.save_file(output_folder_dict[folder],filename,payments)
                converter.save_file(output_folder_dict[folder],'adjustments_'+date,adjustments)

                
            elif folder == 'vendor_txn':
                
                filename = 'vendor_bills_'+date
                venbill = converter.Vendor_bill(input_folder+'po')
                converter.save_file(output_folder_dict['po'],filename,venbill)
                
                
                filename = 'vendor_payments_'+date
                transactions_df = converter.Vendor_transaction( input_folder+folder)
                transactions_df['supplier_id']=transactions_df['supplier_id'].astype(int)
                ven_bill_df= pd.read_csv('November/po/vendor_bills_November.csv')

                vendor_payment_df = converter.vendor_payment_po_link(ven_bill_df,transactions_df)
                converter.save_file(output_folder_dict[folder],filename,vendor_payment_df)
                
                

