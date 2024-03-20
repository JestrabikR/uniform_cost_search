# Uniform Cost Search (UCS) in Python
## Overview
This project implements the Uniform Cost Search (UCS) algorithm in Python using recursion. UCS is a variant of Dijkstra's algorithm, which explores the search space by incrementally expanding paths with the lowest costs.

### Features
**Uniform Cost Search:** Utilizes the UCS algorithm to find the optimal path from the start node to the goal node.\
**Recursive Implementation**: The algorithm is implemented recursively, making it easier to understand and follow the logic.\
**Customizable**: The code can be easily adapted to different problems by modifying the data structures.

## Usage
To use this implementation of UCS, follow these steps:

- **Clone the Repository**: Clone this repository to your local machine using Git

- **Open *ucs.py*** and change the ***map*** string to your map and also change ***start_pos*** and ***end_pos*** to your desired coordinates

- **Run the Code**: ```python ucs.py```

- The program will print the optimal path found by the UCS algorithm, along with the values of lists *open* and *closed* in each iteration