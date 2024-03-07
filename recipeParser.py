import pandas as pd
import numpy as np
from tkinter.messagebox import showerror
import sys

class RecipeParser:
    def __init__(self, spit_file, approved_file=None):
        self.spit_file = spit_file
        self.approved_file = approved_file
        self.combined_df = pd.DataFrame()
        self.changeDetails = {'Parameter Identity': "Changed By/Changed Date"}
        self.formfactorlist = []
        self.selected_column=None
        
    class InvalidVialCombinationError(Exception):
        def __init__(self, message):
            super().__init__(message)


    def get_approvedfile(self):
        if self.approved_file:
            df = pd.read_csv(self.approved_file)
            # Access the second column name from the first row
            vial_form_factor = df.columns[1]
            self.formfactorlist.append(vial_form_factor.upper()) #Get the Vial Form Factor from the file
            approved_val = pd.read_csv(self.approved_file,index_col=0,skiprows=1)   #Skip the first row as it contains a header with Vial Form Factor (2R/4R/10R)
            approved_val.reset_index(inplace=True, drop=True)
            approved_val=approved_val.drop(0)
            approved_val.reset_index(inplace=True, drop=True)

            return approved_val
        else:
            return None
    
    def validate_vial_form_factor(self): #Function to check the Recipe/Files have the same Vials
        if len(set(self.formfactorlist))!=1:
            showerror(
                title='Illegal Vials Values Selected!',
                message=f"Only one type of vial is allowed! Vials Values Selected are{set(self.formfactorlist)}"
            )
            sys.exit()
    
    def parse_with_spit_file(self): #To be used for comparing a recipe file with an approved list of recipes
        vial_form_factor, vial_cc, changedate, changename = self.get_columnname(self.spit_file)
        self.formfactorlist.append(vial_form_factor)
        self.selected_column=vial_cc

        return self.parse_files(self.spit_file)

    def parse_with_filenames(self, filename): #To be used for combining multiple files into one CSV or HTML file
        
        filenames_table = self.parse_files(filename)
        vial_form_factor, vial_cc, changedate, changename = self.get_columnname(filename)
        self.formfactorlist.append(vial_form_factor)
        self.changeDetails[vial_cc] = f"{changename}/{changedate}"
        
        return filenames_table.rename(columns={"name":"Parameter Identity","value":vial_cc})

    def get_columnname(self, filename): #Extracts the Values for Vial Form Factor (2R/4R/10R), Vial Recipe (0.43ml pp/0.58ml pp/0.768ml pp etc), Last user to make a change and last modified date for the recipe on SCADA
        count=0
        vial_form_factor, vial_cc, changedate, changename = None, None, None, None
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('#data'):
                    values = line.split(";")
                    changename = values[21].strip()
                    changedate = values[23].strip()                    
                    try:
                        vial_form_factor, vial_cc = map(str.strip, values[2].split(","))
                    except ValueError: #Throw an error if the decimal representation is comma instead of dot in Name of the recipe (example: 2R Vial, 0.43ml pp)
                        showerror(
                            title='Invalid formatting!',
                            message=f'Comma (,) encountered instead of dot (.) in \
                                {filename}. Check "Name" value in {values[2]}'
                        )
                        sys.exit()
                    count+=1
                    break
                if count>0:
                    break
        return vial_form_factor.upper(), vial_cc, changedate, changename
                
    def parse_files(self, filename):
        # Initialize Row list
        rows = []
        headers = None
        with open(filename, 'r') as f:
            inside_param = False
            for line in f:
                line = line.strip()
                if line == "<begin>param":  #check if the line begins with "<begin>param"
                    inside_param = True     #Set inside_param flag as True when inside the <begin>param block
                elif line == "<end>param":  #check if the line begins with "<end>param"
                    inside_param = False    #Set inside_param flag as False as the pointer has exited the recipe block <end>param block
                elif inside_param:          #Actions when inside the <beign>param **** <end>param
                    if line.startswith('#header'):              #If line starts with #header,
                        headers=line.strip().split(';')         #Split the line and append it to header list
                    elif line.startswith('#data'):              #If line starts with #data
                        data=line.strip().split(';')            #split the line and assign it to data variable
                        rows.append(data[1:])                   #Append the data variable after index 1, excluding '#data' from the list and append it to rows list

        table = pd.DataFrame(rows, columns=headers[1:])         #Create a dataframe with values from list 'data' and headers from list 'header'. header is sliced 1: to exclude the value '#header'

        return table[['name', 'value']]

    def combinefile(self):
        dfs = []
        for filename in self.spit_file:
            df = self.parse_with_filenames(filename)        #Parse each file and extract the header and data values
            df.set_index('Parameter Identity', inplace=True)    #Set the index as 'Parameter Identity' column
            dfs.append(df)  #Append all the data as a list to save memory space

   
        self.validate_vial_form_factor()    #Validate if all the files selected have the same vial form factor
        self.combined_df = pd.concat(dfs, axis=1, join='outer') #Create a dataframe from the dfs list
        self.combined_df.reset_index(inplace=True)              
        # Ensure the keys in changeDetails match the columns in combined_df
        change_details_df = pd.DataFrame([self.changeDetails], columns=self.combined_df.columns)
        # Concatenate the changeDetails DataFrame with the existing DataFrame        
        self.combined_df = pd.concat([change_details_df, self.combined_df]) #Add the row containing Changed By/Change Date row just below the header row
        self.combined_df.reset_index(drop=True, inplace=True)

        #Create a multi-index dataframe to add a new row as the header for the dataframe with the vial name             
        header = pd.MultiIndex.from_tuples([(self.formfactorlist[0], col) for col in self.combined_df.columns], names=['', ''])
        # Set the MultiIndex as the column names with centered alignment
        self.combined_df.columns = header      
       
        
        return self.combined_df
    
    def selected_col_approved_val(self, approved_val):
        #Check if both Spit File and the Approved File can be compared and represent the same Vial Form Factor (2R/4R/10R)
        self.validate_vial_form_factor()
        
        if self.selected_column:
            #Alter the approved_val Dataframe to only have Parameter Identity and the selected recipe as the columns
            #The recipe value is selected from the Spit file that the approved file is compared to
            approved_val = approved_val[['Parameter Identity', self.selected_column]].rename(columns={self.selected_column: 'value'})
            
        return approved_val        
    
    def compare_columns(self, table, approved_val):
        
        df_all = pd.concat(
            [approved_val.set_index('Parameter Identity'), table.set_index('name')],    #Create a dataframe with Parameter Identity and a multi-index column (Value,Approved) and (Value, Actual)
            axis='columns', 
            keys=['Approved', 'Actual'],
            join='inner'
        )
        df_flat = df_all.reset_index()
        df_flat.index = df_flat.index+1
        df_flat.columns = ['_'.join(col).strip() for col in df_flat.columns.values] #Flatten the multi-index column to only have 3 single index columns. The column names will be concatenated with its multi-index column name Approved_value/Actual_Value
        
        df_flat=df_flat.rename(columns={'index_':'Parameter Identity'})  
        header = pd.MultiIndex.from_tuples([(f'{self.formfactorlist[0]},{self.selected_column}', col) for col in df_flat.columns], names=['', '']) #Create a multi-index dataframe to add a header for all the columns as the vial name
        df_flat.columns=header
                
        return df_flat


    def apply_highlighting(self, df_flat):
        #Highligh the difference between two columns Approved_value and Actual_value
        styled = df_flat.style.apply(lambda x: (x != df_flat[(f'{self.formfactorlist[0]},{self.selected_column}', 'Approved_value')]).map({True: 'background-color: red; color: white', False: ''}), 
                                     subset=[(f'{self.formfactorlist[0]},{self.selected_column}', 'Actual_value')])
        styled = styled.set_table_styles([
            {'selector': 'tr', 'props': [('border', '1px solid black')]},
            {'selector': 'td, th', 'props': [('border', '1px solid black')]},
        ])
        return styled
    
    
    
