import matplotlib.pyplot as plt
from typing import List
from app import arrCoords
fig, ax = plt.subplots()
def show_data(data:List):
    ax.scatter([x[0] for x in data], [x[1] for x in data], s=2, c='r')
    plt.show()

show_data(arrCoords['coords'])