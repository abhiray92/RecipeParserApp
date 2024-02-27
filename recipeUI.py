import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter import filedialog
import pandas as pd
import re

class IsValid:
    @staticmethod
    def validate_spit_file(filename):
        with open(filename, 'r') as file:
            content = file.read()
            #print(content)
            pattern = re.compile(r'<begin>recipe.*?<end>recipe', re.DOTALL | re.VERBOSE)
            if pattern.search(content):
                return True
            else:           
                return False
    
    @staticmethod
    def validate_approved_file(filename):
        try:
            approved_data = pd.read_csv(filename, nrows=1, skiprows=1)  # Read only the first row for validation
            # Check if 'Parameter Identity' is in the columns and there are at least 2 columns
            if 'Parameter Identity' in approved_data.columns and approved_data.shape[1] >= 2:
                return True
            else:
                return False
            
        except pd.errors.EmptyDataError:
            showerror(
                title='Invalid File',
                message='The selected Approved file is empty.'
            )
            
            return False


class RecipeUI:
    def __init__(self, parent):
        self.spit_file = ""
        self.approved_file = ""
        self.parent = parent
        self.child_window = tk.Toplevel(parent)
        self.parent.withdraw()
        self.child_window.title('Select Files')
        self.child_window.geometry('300x150')
        self.child_window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.fileValidator = IsValid()

        self.create_widgets()

    def create_widgets(self):
        open_button = ttk.Button(
            self.child_window,
            text='Open the Recipe File from the Line',
            command=self.select_spit_file
        )
        
        open_button.pack(expand=True)

        open_approved_button = ttk.Button(
            self.child_window,
            text='Open the approved Recipe File from vault',
            command=self.select_approved_file
        )
        open_approved_button.pack(expand=True)
        
    

    def select_spit_file(self):
        filetypes = (
            ('CSV files', '*.csv'),
            ('CSV files', '*.csv')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        
        # Perform validation on the spit_file content
        try:
            if self.fileValidator.validate_spit_file(filename):
                self.spit_file = filename
                showinfo(
                    title='Selected File',
                    message=filename
                )
            else:
                showerror(
                    title='Invalid File',
                    message='The selected Spit file does not match the required format.'
                )
        except FileNotFoundError:
            showerror(
                title='No File Selected',
                message='No File Selected!'
            )
       
    
    def select_approved_file(self):
        filetypes = (
            ('CSV files', '*.csv'),
            ('CSV files', '*.csv')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        self.approved_file = filename
        
        # Perform validation on the approved_file content
        try:
            if self.fileValidator.validate_approved_file(filename):
                self.approved_file = filename
                showinfo(
                    title='Selected File',
                    message=filename
                )           
                # Create an instance of ColumnSelector
                #column_selector = ColumnSelector(self.child_window, self.approved_file)
                #self.selected_column = column_selector.run()
                self.child_window.destroy()
            else:
                showerror(
                    title='Invalid File',
                    message='The selected Approved file does not match the required format.'
                )
        except UnicodeDecodeError:
            showerror(
                title='Invalid File',
                message='Error parsing the selected Approved file. Make sure it is in a valid CSV format.'
            )
        except FileNotFoundError:
            showerror(
                title='No File Selected',
                message='No File Selected!'
            )
        
    def on_close(self):
        self.parent.deiconify()  # Bring back the parent window
        self.child_window.destroy()
        
    def run_application(self):
        self.parent.wait_window(self.child_window)
        return self.approved_file, self.spit_file


class CombineUI:
    def __init__(self, parent, filenames):
        self.parent = parent
        self.child_window = tk.Toplevel(parent)
        self.parent.withdraw()
        self.child_window.title('Combine')
        self.child_window.geometry('300x150')
        self.filenames = ""
        self.child_window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.file_validator = IsValid()

        self.create_widgets()

    def create_widgets(self):
        combine_button = ttk.Button(
            self.child_window,
            text='Browse CSV files',
            command=self.browse_files
        )
        combine_button.pack(expand=True)

    def browse_files(self):
        self.filenames = fd.askopenfilenames(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if self.filenames:
            showinfo(
                title='Selected Files',
                message=self.filenames
            )
        try:
            for filename in self.filenames:
                if not self.file_validator.validate_spit_file(filename):
                    showerror(
                    title='Invalid File',
                        message=f'The selected file {filename} does not match the required format.'
                    )
                    return False
                    
            self.child_window.destroy()
            return True
        except InvalidFileError as e:
            showerror(
                title='Invalid File Found',
                message='All the files should be in the specified format.'
            )
            return False
    
    def on_close(self):
        self.parent.deiconify()  # Bring back the parent window
        self.child_window.destroy()

    def run(self):
        self.parent.wait_window(self.child_window)
        return self.filenames
        
class RootUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Select an Option')
        self.root.resizable(False, False)
        self.root.geometry('300x150')
        self.child_window = None
        self.filenames=""
        self.spit_file = ""
        self.approved_file = ""
        self.fileflag=False
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        

        self.create_widgets()

    def create_widgets(self):
        compare_button = ttk.Button(
            self.root,
            text='Compare',
            command=self.open_compare_window
        )
        compare_button.pack(expand=True)

        combine_button = ttk.Button(
            self.root,
            text='Combine',
            command=self.open_combine_window
        )
        combine_button.pack(expand=True)

    def open_compare_window(self):
        compare_window = RecipeUI(self.root)
        self.root.withdraw()  # Hide the main window
        self.approved_file, self.spit_file = compare_window.run_application()
        if self.spit_file or self.approved_file:
            self.root.destroy()
        else:
            self.root.deiconify() 

    def open_combine_window(self):
        combine_window = CombineUI(self.root, self.filenames)
        self.root.withdraw()  # Hide the main window
        self.filenames = combine_window.run()
        if self.filenames:  # Check if files are selected
            self.fileflag = True
            if self.fileflag:  # Check if the combine process was successful
                self.root.destroy()  # Close the root window if both conditions are met
        else:
            self.root.deiconify()  # Show the main window if no files are selected

    def on_close(self):
        self.root.destroy()        

    def run_application(self):
        self.root.mainloop()

class SaveFile:
    def __init__(self, filename):
        self.root = tk.Tk()
        self.root.title('Select an Option')
        self.root.resizable(False, False)
        self.root.geometry('300x150')
        self.filename = filename
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()


    def create_widgets(self):
        save_button_csv = ttk.Button(
            self.root,
            text='Export to CSV',
            command=self.open_save_csv_window
        )
        save_button_csv.pack(expand=True)

        save_button_html = ttk.Button(
            self.root,
            text='Export to HTML',
            command=self.open_save_html_window
        )
        save_button_html.pack(expand=True)
        
    def open_save_html_window(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        filename_html = self.filename.to_html()
        if file_path:
            self.filename.to_html(file_path, justify='center')
            print("HTML file saved successfully.")
            self.root.destroy()
            
    def open_save_csv_window(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.filename.to_csv(file_path)
            print("CSV file saved successfully.")
            self.root.destroy()

    def on_close(self):
        self.root.destroy()        

    def run_application(self):
        self.root.mainloop()
        

    
        
        
        
        


        
    
    