# Project1_AI_Search
This is a project in the course Introduction to Artificial Intelligence at HCMUS.  

This project aims to build an interactive application to visualize the behaviour of several search algorithms via Rush Hour Game:

- Breadth-First Search.
- Depth-First Search.
- Uniform-Cost Search.
- A* Search.

Rush Hour Game is a classic game where the target vehicle must escape a traffic jam through some searching strategy. The project is implemented in Python with Pygame library as the main library for visualization.

The performance of each algorithm is measured in 3 metrics:

- Search time.
- Memory usage.
- Number of nodes gen.

The current **step count** and **total cost** of the state of the game is presented real time on the screen to make it easy to follow.

# How to run the game
- Use the Terminal or Command Prompt to navigate into the project folder.
- Be sure that Python and Pip has been already installed in your computer.
- Run the following code to install all neccessary libraries and dependencies.
```
pip install -r requirements.txt
```
- After installing libraries, run the following code to run the game.
```
py source/main.py
```
- Enjoy the game!