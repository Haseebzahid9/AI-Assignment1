# AI Pathfinder - Uninformed Search Algorithms with Dynamic Obstacles
## Assignment: AI2002 

This project implements 6 uninformed search algorithms with real-time GUI visualization and dynamic obstacle handling for AI2002 Assignment 1.

## Features

- 6 Search Algorithms: BFS, DFS, UCS, DLS, IDDFS, Bidirectional Search
- Step-by-Step Visualization: Watch algorithms explore the grid in real-time
- Dynamic Obstacles: Random obstacles spawn during search, forcing re-planning
- Clockwise Movement: All 8 directions including all diagonals
- Interactive GUI: Clean matplotlib-based visualization
- Color-Coded Display: 
  - Blue = Start (S)
  - Green = Goal (T)
  - Black = Static Obstacles
  - Red = Dynamic Obstacles
  - Light Blue = Frontier Nodes
  - Light Gray = Visited Nodes
  - Yellow = Final Path

## Requirements

### System Requirements
- Python 3.7 or higher
- Works on Windows, macOS, or Linux

### Python Libraries
```
matplotlib>=3.3.0
numpy>=1.19.0
```

## Installation

### Step 1: Install Python
If you don't have Python installed:
- Windows: Download from python.org
- macOS: brew install python3
- Linux: sudo apt-get install python3 python3-pip

### Step 2: Install Dependencies

Open terminal or command prompt and run:

```bash
pip install matplotlib numpy
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 3: Download the Code

Download pathfinder.py to your computer.

## How to Run

### Method 1: Command Line

1. Open terminal or command prompt
2. Navigate to the folder containing pathfinder.py:
   ```bash
   cd path/to/your/folder
   ```
3. Run the program:
   ```bash
   python pathfinder.py
   ```

### Method 2: IDE (PyCharm, VS Code, etc.)

1. Open pathfinder.py in your IDE
2. Click the "Run" button or press F5

### Method 3: Direct Execution (Linux/Mac)

```bash
chmod +x pathfinder.py
./pathfinder.py
```

## Usage

When you run the program, you'll see an interactive menu:

1. Select Grid Size: Enter the number of rows and columns (default is 15x15)

2. Choose Scenario:
   - Random obstacles
   - Best case (clear path)
   - Worst case (maze-like)

3. Select Algorithm:
   ```
   1. Breadth-First Search (BFS)
   2. Depth-First Search (DFS)
   3. Uniform Cost Search (UCS)
   4. Depth-Limited Search (DLS)
   5. Iterative Deepening DFS (IDDFS)
   6. Bidirectional Search
   7. Run All Algorithms
   ```

4. Choose Visualization Speed:
   - Slow (0.1s delay)
   - Medium (0.05s delay)
   - Fast (0.01s delay)
   - Very Fast (0.001s delay)

5. Enable Dynamic Obstacles: Choose yes or no

The GUI window will open with the title "GOOD PERFORMANCE TIME APP" and show the algorithm exploring the grid step-by-step.

## Understanding the Output

### Grid Visualization

| Color/Symbol | Meaning |
|--------------|---------|
| Blue with S | Start Position |
| Green with T | Target/Goal Position |
| Black | Static Obstacle (Wall) |
| Red | Dynamic Obstacle |
| Light Blue | Frontier (nodes waiting to be explored) |
| Light Gray | Visited (already explored) |
| Yellow | Final Path |

### Console Output
After the algorithm finishes, you'll see:
- Path found: Yes or No
- Path length: Number of steps
- Nodes explored: Total nodes visited
- Time taken: Execution time in seconds
- Dynamic obstacles: Number spawned

## Algorithm Details

### 1. Breadth-First Search (BFS)
Explores the grid level by level, like ripples in water. Always finds the shortest path.

- Complete: Yes (always finds a solution if one exists)
- Optimal: Yes (finds shortest path)
- Time Complexity: O(b^d)
- Space Complexity: O(b^d)
- Best for: Finding shortest path in unweighted grids

### 2. Depth-First Search (DFS)
Goes as deep as possible down one path before backtracking. Fast but doesn't guarantee shortest path.

- Complete: No (can get stuck in infinite loops)
- Optimal: No (doesn't guarantee shortest path)
- Time Complexity: O(b^m)
- Space Complexity: O(bm)
- Best for: Memory-constrained scenarios

### 3. Uniform Cost Search (UCS)
Always expands the node with the lowest cost. Considers diagonal movements cost more than straight movements.

- Complete: Yes
- Optimal: Yes (finds lowest-cost path)
- Time Complexity: O(b^(C/ε))
- Space Complexity: O(b^(C/ε))
- Best for: Weighted graphs where diagonal moves cost more

### 4. Depth-Limited Search (DLS)
Like DFS but stops at a specific depth limit. Won't find solution if it's deeper than the limit.

- Complete: No (if limit is less than solution depth)
- Optimal: No
- Time Complexity: O(b^l) where l is the limit
- Space Complexity: O(bl)
- Best for: When you know the approximate depth

### 5. Iterative Deepening DFS (IDDFS)
Runs DLS multiple times with increasing depth limits. Combines the best of BFS and DFS.

- Complete: Yes
- Optimal: Yes (for uniform costs)
- Time Complexity: O(b^d)
- Space Complexity: O(bd)
- Best for: Unknown depth with space constraints

### 6. Bidirectional Search
Searches from both start and goal simultaneously, meeting in the middle. Much faster for large grids.

- Complete: Yes
- Optimal: Yes (if both directions use BFS)
- Time Complexity: O(b^(d/2))
- Space Complexity: O(b^(d/2))
- Best for: Known goal state in large search spaces

## Movement Order

The algorithm checks neighbors in clockwise order with all diagonals:

1. Up (-1, 0)
2. Top-Right (-1, 1) - Diagonal
3. Right (0, 1)
4. Bottom-Right (1, 1) - Diagonal
5. Bottom (1, 0)
6. Bottom-Left (1, -1) - Diagonal
7. Left (0, -1)
8. Top-Left (-1, -1) - Diagonal

Movement costs:
- Straight moves: 1.0
- Diagonal moves: 1.414 (square root of 2)

## Dynamic Obstacles

During the search, random empty cells may become obstacles:
- Probability: 1-2% per step (configurable)
- Forces the algorithm to adapt and find alternative routes
- Shown in red color
- When an obstacle blocks the planned path, the algorithm re-runs

## Testing Scenarios

### Best Case Scenario
Clear path with minimal obstacles. The algorithm finds the goal quickly with few nodes explored.

Good for testing: BFS, Bidirectional Search

### Worst Case Scenario
Complex maze layout with the goal far from start. The algorithm explores most of the grid before finding the path.

Good for testing: DFS, IDDFS

### Comparison Mode
Run all 6 algorithms on the same grid to compare their performance.

## Project Structure

```
AI_Pathfinder/
│
├── pathfinder.py          # Main implementation
├── README.md             # This file
├── requirements.txt      # Dependencies
│
└── screenshots/          # For your report
   
```

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'matplotlib'"
Solution: Install matplotlib using pip install matplotlib

### Problem: GUI window doesn't appear
Solution:
- Windows: Make sure you're not using WSL without X server
- macOS: Install python-tk using brew install python-tk
- Linux: Install tkinter using sudo apt-get install python3-tk

### Problem: Animation is too fast or too slow
Solution: When running the program, choose a different visualization speed option (1-4)

### Problem: Program closes immediately
Solution: Make sure you're running it from command line or IDE, not by double-clicking the file

## For Assignment Submission

### What to Submit

1. Zip file containing:
   - pathfinder.py (source code)
   - README.md (this file)
   - requirements.txt
   - Report PDF

2. GitHub Repository:
   - Upload all files to GitHub
   - Make sure your commit history shows your work
   - Include a clear README

3. PDF Report with:
   - Algorithm explanations
   - Pros and cons analysis
   - Screenshots (2 per algorithm: best and worst case)
   - Performance comparison tables
   - Challenges faced
   - References

### Creating Screenshots

To save screenshots for your report:
1. Run each algorithm
2. Wait for the final result to display
3. Take a screenshot of the GUI window
4. Save as: algorithm_name_scenario.png (e.g., bfs_best.png)
5. Include in your report

### GitHub Repository Setup

```bash
git init
git add pathfinder.py README.md requirements.txt
git commit -m "Initial commit: AI Pathfinder implementation"
git remote add origin https://github.com/yourusername/AI_Pathfinder.git
git push -u origin main
```

## Understanding the Code

### Main Classes

1. GridEnvironment: Handles the grid, obstacles, and movement validation
2. PathfindingVisualizer: Creates and updates the GUI
3. UninformedSearch: Implements all 6 search algorithms

### Key Functions

- get_neighbors(): Returns valid neighbors in clockwise order
- add_dynamic_obstacle(): Randomly spawns obstacles during search
- reconstruct_path(): Builds the final path from parent pointers
- update_visualization(): Redraws the grid with current state

### Customization

You can modify these in the code:

Grid size:
```python
env = GridEnvironment(rows=20, cols=20)
```

Dynamic obstacle probability:
```python
env = GridEnvironment(dynamic_obstacle_prob=0.03)  # 3% chance
```

Visualization delay:
```python
run_algorithm(algorithm_name, env, delay=0.1)  # slower animation
```

## Viva Preparation

Be ready to explain:
- How each algorithm works and why it behaves differently
- What data structures each algorithm uses (queue, stack, priority queue)
- Time and space complexity of each algorithm
- How dynamic obstacles are handled
- Why certain algorithms are optimal and others aren't
- How to modify the movement order
- How path reconstruction works

Common questions:
- "Show me where BFS is implemented"
- "What happens if you change the movement order?"
- "Why does DFS sometimes find longer paths?"
- "How would you add A-star search?"

## References

1. Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.)
2. Cormen, T. H., et al. (2009). Introduction to Algorithms (3rd ed.)
3. Red Blob Games - Pathfinding: https://www.redblobgames.com/pathfinding/
4. Matplotlib Documentation: https://matplotlib.org/
5. Python heapq module: https://docs.python.org/3/library/heapq.html

## Author Information
- Name: Haseeb zahid
- Student ID: 23F-0644
- Name: Adan Sajid
- Student ID: 23F-0691
- Course: AI2002 - Artificial Intelligence
- Semester: Spring 2026
- Assignment: Question 7 
- Date: 17-02-26
- Assignment: Question 7 - Uninformed Search in Grid Environment

