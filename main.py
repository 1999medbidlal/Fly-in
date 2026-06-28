from parce_data import Data
from Visualisation import run
from Algo_dijkstra import Graph
import sys

if __name__ == "__main__":
    # try:
        data = Data()
        file = data.read_file(sys.argv[1])
        data.parce_data(file)
        graph = Graph(data)
        graph.refind_path()
        # run(data, path)
        
    # except Exception as e:
    #     print(f"Error: {type(e).__name__}: {e}")   
 