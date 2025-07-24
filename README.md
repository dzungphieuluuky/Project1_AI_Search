# 🚗 Project 1 – AI Search Visualization: Rush Hour Game

This project is developed as part of the **Introduction to Artificial Intelligence** course at **Ho Chi Minh City University of Science (HCMUS)**.

It aims to **visualize the behavior of classical search algorithms** through an interactive implementation of the **Rush Hour puzzle game**, using **Python** and the **Pygame** library.

## 🔍 Search Algorithms Implemented

The following search strategies are implemented to solve the puzzle:

* **Breadth-First Search (BFS)**
* **Depth-First Search (DFS)**
* **Uniform-Cost Search (UCS)**
* **A\* Search**

## 🧩 Game Overview

**Rush Hour** is a classic sliding block puzzle where the objective is to move the target vehicle out of a crowded 6×6 grid by shifting blocking vehicles out of the way using search algorithms.

This project not only solves the puzzle but also offers real-time **visual feedback** on the algorithm’s progress, including:

* 🔢 **Current step count**
* 💰 **Total path cost**

## 📊 Performance Metrics

Each algorithm is evaluated based on the following performance criteria:

* ⏱️ **Search time**
* 🧠 **Memory usage**
* 🌲 **Number of nodes expanded**

These metrics help demonstrate the efficiency and trade-offs of each strategy.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have **Python 3** and **pip** installed on your system.

### Installation

1. Open Terminal or Command Prompt and navigate to the project directory.
2. Install required libraries:

   ```bash
   pip install -r requirements.txt
   ```

### Run the Application

Once dependencies are installed, launch the game using:

```bash
py source/main.py
```

Enjoy the puzzle and observe how different search algorithms solve it in real time!

---

## 📂 Project Structure

```
Project1_AI_Search/
├── source/
│   ├── main.py
│   ├── ... (other game and algorithm files)
├── assets/
│   └── ... (images, sounds, etc.)
├── requirements.txt
└── README.md
```

---

## 🙌 Credits

Developed by students of **HCMUS - Introduction to AI** as one of the projects in the course.
