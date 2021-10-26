from filter import Data
from nofilter import DataNoFilter
import sys, getopt
import time
if __name__ == "__main__":
    files = sys.argv[1:]
    if(len(files)):
        for file in files:
            print(file)
            comfiltro = Data(file)
            comfiltro.run()
            semfiltro = DataNoFilter(file)
            semfiltro.run()
            sys.exit(0)
    else:
        print("Para rodar o script, favor informar no formato: python main.py -i <nome-elemento-1> python main.py -i <nome-elemento-2>")
        sys.exit(1)
    

