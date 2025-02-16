
import importlib
import Dashboard
importlib.reload(Dashboard)
import layout

# Now re-import the class and test again
importlib.reload(layout)
from Dashboard import Dashboard_creator

from layout import create_layout
def main() -> None:
    app = Dashboard_creator(codes = ["CBA", "LIV"])
    


if __name__ == "__main__":
    main()
