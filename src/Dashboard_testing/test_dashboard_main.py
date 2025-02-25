
import pandas as pd
import sys
import os

# Add the root directory of your project to sys.path
# This assumes that your 'model_deployment' folder is the root of the project
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tests'))
test_file_path = os.path.join(tests_dir, 'test_data_raw_data.csv')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now re-import the class and test again

from Dashboard_testing.Dashboard import Dashboard_creator
from plotting import SharesPlotter
from dataframe_manager import shares_analysis

def main() -> None:

    test_df = pd.read_csv(test_file_path)
    test = shares_analysis(shares_df = test_df,get_cache_df = False)
    test.calc_rsi(window = 4, min_periods = 3)
    Plotter = SharesPlotter(test, plot_website = True)
    app = Dashboard_creator(codes = ["CBA", "LIV","TLS"],Plotter = Plotter)
    app.run()
    


if __name__ == "__main__":
    main()
