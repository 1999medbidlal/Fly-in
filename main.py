from parce_data import Data
from visualisation import run
from Algo_dijkstra import Graph
from simulation import Sim
import sys

if __name__ == "__main__":
    # try:
        data = Data()
        file = data.read_file(sys.argv[1])
        data.parce_data(file)
        graph = Graph(data)
        path = graph.refind_path()
        print(path)
        sim = Sim(graph)
        # while not sim.is_finished():
        #     sim.run_simulation()
        run(data, sim)
        
    # except Exception as e:
    #     print(f"Error: {type(e).__name__}: {e}")   
 