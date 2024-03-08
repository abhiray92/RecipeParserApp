</b>This is a simple application to parse raw csv files exported from a SCADA application. Although this application serves a pretty specific use case. It can still be used for various other purposes. This application has two components. </b>

<h3>Combine</h3>
This option will let one combine multiple recipe files in raw csv format and merge them into a tabular format for a particular parameter form factor (assuminng its Vials in this case). The table can be exported in either CSV or HTML file format.

An example of the exported html file - 

![image](https://github.com/abhiray92/RecipeParserApp/assets/42731567/fe51cb54-f062-411d-bfc9-7b20120c0da7)



<h3>Compare</h3>
The compare option lets you compare a raw csv file with the combined CSV file generated above. It automatically selects the recipe (column) from the combined CSV file based on the details in the raw CSV file. The recipe is then transformed into a table and the difference in the values are highlighted. The 'Approved_value' column represents the column from the combined CSV file and the 'Actual_value' column is from the raw CSV file being compared.
