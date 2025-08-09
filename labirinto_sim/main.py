from maze import load_maze
from agent import Agent
from config import *
import pandas as pd
import os
os.system('cls')

print("Initializing DataFrame.")
df = pd.DataFrame({'complexity': [],
                   'ratio': [],
                   'max_steps': [],
                   'random_steps': [],
                   'direct_steps': [],
                   'reached_goal': [],
                   'control': []})

def run_simulation_a_star(cfg, directed_every_n_steps, comp, max_step):
    
    maze, start, goal = load_maze(cfg["maze_file"])
    agent = Agent(start, goal, maze)
    steps = 0
    directed_count = 0

    while not agent.reached_goal() and steps < max_step:
        if steps % directed_every_n_steps == 0:
            agent.move_directed()
            directed_count += 1
        else:
            agent.move_random()
        steps += 1

    df.loc[len(df)] = [comp, directed_every_n_steps, max_step, steps, directed_count, agent.reached_goal(), False]

def run_simulation_random(cfg, directed_every_n_steps, comp, max_step):
    
    maze, start, goal = load_maze(cfg["maze_file"])
    agent = Agent(start, goal, maze)
    steps = 0

    while not agent.reached_goal() and steps < (max_step + max_step / directed_every_n_steps):
        agent.move_random()
        steps += 1

    df.loc[len(df)] = [comp, directed_every_n_steps, (max_step + max_step / directed_every_n_steps), steps, 0, agent.reached_goal(), True]
    

if __name__ == "__main__":

    sim_count = 1000
    max_steps = 100000
    ratio = 100
    
    print("Starting [" + str(sim_count) + "] control simulations")
    
    for i in range(0, sim_count):
        run_simulation_random(MAZE_1, ratio, 1, max_steps)

    for i in range(0, sim_count):
        run_simulation_random(MAZE_2, ratio, 2, max_steps)

    for i in range(0, sim_count):
        run_simulation_random(MAZE_3, ratio, 3, max_steps)

    for i in range(0, sim_count):
        run_simulation_random(MAZE_4, ratio, 4, max_steps)
    
    for i in range(0, sim_count):
        run_simulation_random(MAZE_5, ratio, 5, max_steps)
    

    print("Starting [" + str(sim_count) + "] simulations for ratio ["+str(ratio)+"-1]")

    for i in range(0, sim_count):
        run_simulation_a_star(MAZE_1, ratio, 1, max_steps)
    
    for i in range(0, sim_count):
        run_simulation_a_star(MAZE_2, ratio, 2, max_steps)

    for i in range(0, sim_count):
        run_simulation_a_star(MAZE_3, ratio, 3, max_steps)

    for i in range(0, sim_count):
        run_simulation_a_star(MAZE_4, ratio, 4, max_steps)

    for i in range(0, sim_count):
        run_simulation_a_star(MAZE_5, ratio, 5, max_steps)
    
    df.to_excel("output.xlsx")
