from maze import load_maze
from agent import Agent
from config import *
import pandas as pd
import os
import concurrent.futures
import time


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

    return (comp, directed_every_n_steps, max_step, steps, directed_count, agent.reached_goal(), False)

def run_simulation_random(cfg, directed_every_n_steps, comp, max_step):
    
    maze, start, goal = load_maze(cfg["maze_file"])
    agent = Agent(start, goal, maze)
    steps = 0

    while not agent.reached_goal() and steps < (max_step + max_step / directed_every_n_steps):
        agent.move_random()
        steps += 1

    return (comp, directed_every_n_steps, (max_step + max_step / directed_every_n_steps), steps, 0, agent.reached_goal(), True)

def run_random_wrapper(maze, ratio, maze_num, max_steps):
        return run_simulation_random(maze, ratio, maze_num, max_steps)

def run_a_star_wrapper(maze, ratio, maze_num, max_steps):
    return run_simulation_a_star(maze, ratio, maze_num, max_steps)

if __name__ == "__main__":

    sim_count = 1000
    max_steps = 100000
    ratios = [5, 10, 25, 50, 100]
    ratio = 25
    MAZES = [MAZE_1, MAZE_2, MAZE_3, MAZE_4, MAZE_5]

    start_time = time.time()


    with concurrent.futures.ProcessPoolExecutor() as executor:

        futures = []

        for r in ratios:

            os.system("cls")
            print("Running Simulations for ratio " + str(r) + ":1")

            for maze in MAZES:
                maze_name = str(maze)[54:-6]
                maze_num = int(str(maze)[58:-6])
                print(f"Running control for {maze_name}")
                for _ in range(sim_count):
                    futures.append(executor.submit(run_random_wrapper, maze, r, maze_num, max_steps))


            for maze in MAZES:
                maze_name = str(maze)[54:-6]
                maze_num = int(str(maze)[58:-6])
                print(f"Running simulation for {maze_name}")
                for _ in range(sim_count):
                    futures.append(executor.submit(run_a_star_wrapper, maze, r, maze_num, max_steps))

            results = []
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        
        df = pd.DataFrame(results, columns=['complexity', 'ratio', 'max_steps', 'random_steps', 'direct_steps', 'reached_goal', 'control'])



    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Started at: " + time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(start_time)))
    print("Ended at: " + time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(end_time)))
    print(f"Execution time: {elapsed_time:.2f} seconds")

    df.to_excel("output.xlsx")