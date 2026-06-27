from parce_data import Parce_Data
from visualisation import run
import sys

if __name__ == "__main__":
    # try:
        p = Parce_Data()
        file = p.read_file(sys.argv[1])
        p.parce_data(file)
        run(p)
    # except Exception as e:
    #     print(f"Error: {type(e).__name__}: {e}")   
