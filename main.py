from parce_data import Parce_Data
import sys
if __name__ == "__main__":
    try:
        p = Parce_Data()
        file = p.read_file(sys.argv[1])
        p.parce_data(file)
        print(p.end_hub.max_drones)
    except Exception as e:
        print(e)
