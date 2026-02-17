# QUICK START GUIDE

## For Students Who Want to Run This Right Now

### Windows Users

1. Download Python (if you don't have it):
   - Go to: https://www.python.org/downloads/
   - Download Python 3.10 or higher
   - During installation, CHECK the box "Add Python to PATH"

2. Open Command Prompt:
   - Press Win + R
   - Type cmd and press Enter

3. Install Libraries:
   ```cmd
   pip install matplotlib numpy
   ```

4. Run the Program:
   ```cmd
   cd path\to\your\folder
   python pathfinder.py
   ```

### Mac Users

1. Open Terminal:
   - Press Cmd + Space
   - Type "Terminal" and press Enter

2. Install Libraries:
   ```bash
   pip3 install matplotlib numpy
   ```

3. Run the Program:
   ```bash
   cd path/to/your/folder
   python3 pathfinder.py
   ```

### Linux Users

1. Open Terminal (Ctrl + Alt + T)

2. Install Libraries:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip
   pip3 install matplotlib numpy
   ```

3. Run the Program:
   ```bash
   cd path/to/your/folder
   python3 pathfinder.py
   ```

## What You'll See

1. A menu asking you to choose grid size
2. Choose a scenario type (random, best case, or worst case)
3. Select an algorithm (1-7)
4. Choose visualization speed
5. Enable or disable dynamic obstacles
6. A colorful window will pop up showing the search in action

## Understanding the Colors

- Blue Square with S = Start Point
- Green Square with T = Target/Goal
- Black Squares = Walls/Obstacles
- Red Squares = Dynamic obstacles that appear randomly
- Light Blue Squares = Nodes waiting to be checked (Frontier)
- Light Gray Squares = Already visited nodes
- Yellow Path = Final solution path

## Quick Test

Want to test if everything works?

1. Save pathfinder.py to your Desktop
2. Open terminal or command prompt
3. Type these commands:
   ```
   cd Desktop
   python pathfinder.py
   ```
4. Follow the prompts:
   - Grid size: Just press Enter (uses default 15x15)
   - Scenario: Type 1 and press Enter
   - Algorithm: Type 1 (for BFS) and press Enter
   - Speed: Type 2 and press Enter
   - Dynamic obstacles: Type y and press Enter
5. Watch it work!

## Common Problems and Solutions

Problem: "python: command not found"
Solution: 
- Windows: Use py instead of python
- Mac/Linux: Use python3 instead of python

Problem: "No module named 'matplotlib'"
Solution: You forgot to install the libraries. Run: pip install matplotlib numpy

Problem: GUI window doesn't show up
Solution: 
- Try: pip install --upgrade matplotlib
- Mac: brew install python-tk
- Linux: sudo apt-get install python3-tk

Problem: Program runs but closes immediately
Solution: Don't double-click the file. Run it from command line or terminal as shown above.

## For Your Assignment Report

Step 1: Run All Algorithms
- Test each algorithm (1-6)
- Take screenshots of the GUI window
- Try both best case and worst case scenarios

Step 2: Fill in Your Report
- Explain how each algorithm works
- List pros and cons
- Include screenshots
- Add performance comparison tables

Step 3: Upload to GitHub
```bash
git init
git add pathfinder.py README.md requirements.txt
git commit -m "AI Pathfinder Assignment"
git remote add origin https://github.com/yourusername/AI_Pathfinder.git
git push -u origin main
```




