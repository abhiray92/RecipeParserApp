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
            self.formfactorlist.append(vial_form_factor.upper())
            approved_val = pd.read_csv(self.approved_file,index_col=0,skiprows=1)
            approved_val.reset_index(inplace=True, drop=True)
            approved_val=approved_val.drop(0)
            approved_val.reset_index(inplace=True, drop=True)

            return approved_val
        else:
            return None
    
    def validate_vial_form_factor(self):
        if len(set(self.formfactorlist))!=1:
            showerror(
                title='Illegal Vials Values Selected!',
                message=f"Only one type of vial is allowed! Vials Values Selected are{set(self.formfactorlist)}"
            )
            sys.exit()
    
    def parse_with_spit_file(self):
        vial_form_factor, vial_cc, changedate, changename = self.get_columnname(self.spit_file)
        self.formfactorlist.append(vial_form_factor)
        self.selected_column=vial_cc

        return self.parse_files(self.spit_file)

    def parse_with_filenames(self, filename):
        
        filenames_table = self.parse_files(filename)
        vial_form_factor, vial_cc, changedate, changename = self.get_columnname(filename)
        self.formfactorlist.append(vial_form_factor)
        self.changeDetails[vial_cc] = f"{changename}/{changedate}"
        
        return filenames_table.rename(columns={"name":"Parameter Identity","value":vial_cc})

    def get_columnname(self, filename):
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
                    except ValueError:
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
        # Initialize variables
        rows = []
        headers = None
        with open(filename, 'r') as f:
            inside_param = False
            for line in f:
                line = line.strip()
                if line == "<begin>param":
                    inside_param = True
                elif line == "<end>param":
                    inside_param = False
                elif inside_param:
                    if line.startswith('#header'):
                        headers=line.strip().split(';')
                    elif line.startswith('#data'):
                        data=line.strip().split(';')
                        rows.append(data[1:])              

        table = pd.DataFrame(rows, columns=headers[1:])

        return table[['name', 'value']]

    def combinefile(self):
        dfs = []
        for filename in self.spit_file:
            df = self.parse_with_filenames(filename)
            df.set_index('Parameter Identity', inplace=True)
            dfs.append(df)

   
        self.validate_vial_form_factor()
        self.combined_df = pd.concat(dfs, axis=1, join='outer')
        self.combined_df.reset_index(inplace=True)   
        # Ensure the keys in changeDetails match the columns in combined_df
        change_details_df = pd.DataFrame([self.changeDetails], columns=self.combined_df.columns)
        # Concatenate the changeDetails DataFrame with the existing DataFrame        
        self.combined_df = pd.concat([change_details_df, self.combined_df])
        self.combined_df.reset_index(drop=True, inplace=True)
        #self.combined_df.index.name = 'Index'
             
        header = pd.MultiIndex.from_tuples([(self.formfactorlist[0], col) for col in self.combined_df.columns], names=['', ''])
        # Set the MultiIndex as the column names with centered alignment
        self.combined_df.columns = header      
       
        
        return self.combined_df
    
    def selected_col_approved_val(self, approved_val):
        self.validate_vial_form_factor()
        
        if self.selected_column:
            approved_val = approved_val[['Parameter Identity', self.selected_column]].rename(columns={self.selected_column: 'value'})
            
        return approved_val        
    
    def compare_columns(self, table, approved_val):
        
        df_all = pd.concat(
            [approved_val.set_index('Parameter Identity'), table.set_index('name')], 
            axis='columns', 
            keys=['Approved', 'Actual'],
            join='inner'
        )
        df_flat = df_all.reset_index()
        df_flat.index = df_flat.index+1
        df_flat.columns = ['_'.join(col).strip() for col in df_flat.columns.values]
        
        df_flat=df_flat.rename(columns={'index_':'Parameter Identity'})  
        header = pd.MultiIndex.from_tuples([(f'{self.formfactorlist[0]},{self.selected_column}', col) for col in df_flat.columns], names=['', ''])
        df_flat.columns=header
                
        return df_flat


    def apply_highlighting(self, df_flat):
        styled = df_flat.style.apply(lambda x: (x != df_flat[(f'{self.formfactorlist[0]},{self.selected_column}', 'Approved_value')]).map({True: 'background-color: red; color: white', False: ''}), 
                                     subset=[(f'{self.formfactorlist[0]},{self.selected_column}', 'Actual_value')])
        styled = styled.set_table_styles([
            {'selector': 'tr', 'props': [('border', '1px solid black')]},
            {'selector': 'td, th', 'props': [('border', '1px solid black')]},
        ])
        return styled
    
    
    
