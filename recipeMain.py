from recipeUI import RootUI
from recipeParser import RecipeParser
from recipeUI import SaveFile
import webbrowser

def main():
    # Create UI instance
    ui = RootUI()

    # Run UI to get file paths
    ui.run_application()

    if ui.fileflag:
        if not ui.filenames:
            return
        comparser = RecipeParser(ui.filenames)
        combiner = comparser.combinefile()
        save_file = SaveFile(combiner)
        save_file.run_application()
    elif ui.spit_file or ui.approved_file:
        # Create parser instance
        parser = RecipeParser(ui.spit_file, ui.approved_file)
        # Parse files
        table = parser.parse_with_spit_file()
        approved_val = parser.get_approvedfile()
        #Get the Column selected from UI
        selected_column = parser.selected_column
        #Modified Approved_val for comparison with the Spit File from the Line
        approved_val = parser.selected_col_approved_val(approved_val)

        # Additional operations and comparisons as needed
        combined_df = parser.compare_columns(table,approved_val)

        print(combined_df)
    
        # Apply highlighting
        styled_result = parser.apply_highlighting(combined_df)

        name = 'RecipeComparison.html'
        styled_result.to_html(name)
        webbrowser.open(name)
    else:
        return

    
    

if __name__ == "__main__":
   
    main()
