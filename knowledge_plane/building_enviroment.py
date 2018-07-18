#https://medium.com/@curiousily/solving-an-mdp-with-q-learning-from-scratch-deep-reinforcement-learning-for-hackers-part-1-45d1d360c120

# 1. Building the Environment
ZOMBIE = "z"
CAR = "c"
ICE_CREAM = "i"
EMPTY = "*"

grid = [
    [ICE_CREAM, EMPTY],
    [ZOMBIE, CAR]
]

for row in grid:
    print(' '.join(row))


class State:
    # Having a constant-time access to the car position on each step
    def __init__(self, grid, car_pos):
        self.grid = grid
        self.car_pos = car_pos
        
    def __eq__(self, other):
        return isinstance(other, State) and self.grid == other.grid and self.car_pos == other.car_pos
    
    def __hash__(self):
        return hash(str(self.grid) + str(self.car_pos))
    
    def __str__(self):
        return f"State(grid={self.grid}, car_pos={self.car_pos})"

#All possible actions:
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

ACTIONS = [UP, DOWN, LEFT, RIGHT]   

#initial state:
start_state = State(grid=grid, car_pos=[1, 1])

"""
Your agent needs a way to interact with the environment, that is, choose actions. 
Let’s define a function that takes the current state with an action and 
returns new state, reward and whether or not the episode has completed:
"""
from copy import deepcopy

def act(state, action):
    
    def new_car_pos(state, action):
        p = deepcopy(state.car_pos)
        if action == UP:
            p[0] = max(0, p[0] - 1)
        elif action == DOWN:
            p[0] = min(len(state.grid) - 1, p[0] + 1)
        elif action == LEFT:
            p[1] = max(0, p[1] - 1)
        elif action == RIGHT:
            p[1] = min(len(state.grid[0]) - 1, p[1] + 1)
        else:
            raise ValueError(f"Unknown action {action}")
        return p
            
    p = new_car_pos(state, action)
    grid_item = state.grid[p[0]][p[1]]
    
    new_grid = deepcopy(state.grid)
    
    if grid_item == ZOMBIE:
        reward = -100
        is_done = True
        new_grid[p[0]][p[1]] += CAR
    elif grid_item == ICE_CREAM:
        reward = 1000
        is_done = True
        new_grid[p[0]][p[1]] += CAR
    elif grid_item == EMPTY:
        reward = -1
        is_done = False
        old = state.car_pos
        new_grid[old[0]][old[1]] = EMPTY
        new_grid[p[0]][p[1]] = CAR
    elif grid_item == CAR:
        reward = -1
        is_done = False
    else:
        raise ValueError(f"Unknown grid item {grid_item}")
    
    return State(grid=new_grid, car_pos=p), reward, is_done
    """
    In our case, one episode is starting from the initial state and 
    crashing into a Zombie or eating the ice cream.
    """



# 2. Learning to drive --> Training
"""
Ok, it is time to implement the Q-learning algorithm and get the ice cream. 
We have a really small state space, only 4 states. This allows us to keep 
things simple and store the computed Q values in a table. 
Let’s start with some constants:
"""
import numpy as np
import random

random.seed(42) # for reproducibility

N_STATES = 4
N_EPISODES = 20

MAX_EPISODE_STEPS = 100

MIN_ALPHA = 0.02

alphas = np.linspace(1.0, MIN_ALPHA, N_EPISODES)
gamma = 1.0
eps = 0.2

q_table = dict()

def q(state, action=None):
    
    if state not in q_table:
        q_table[state] = np.zeros(len(ACTIONS))
        
    if action is None:
        return q_table[state]
    
    return q_table[state][action]

def choose_action(state):
    if random.uniform(0, 1) < eps:
        return random.choice(ACTIONS) 
    else:
        return np.argmax(q(state))    


for e in range(N_EPISODES):
    
    state = start_state
    total_reward = 0
    alpha = alphas[e]
    
    for _ in range(MAX_EPISODE_STEPS):
        action = choose_action(state)
        next_state, reward, done = act(state, action)
        total_reward += reward
        
        q(state)[action] = q(state, action) + \
                alpha * (reward + gamma *  np.max(q(next_state)) - q(state, action))
        state = next_state
        if done:
            break
    #print("Episode "+repr(e+1).rjust(2) + ": total reward -> " + repr(total_reward).rjust(3))
    print(f"Episode {e + 1}: total reward -> {total_reward}")
"""
Here, we use all of the helper functions defined above to ultimately train your agent to behave 
(hopefully) kinda optimal. We start with the initial state, at every episode, choose an action, 
receive reward and update our Q values. Note that the implementation looks similar 
to the formula for Q-learning, discussed above.

You can clearly observe that the agent learns how to act efficiently, very quickly. 
Our MDP is really small and this might be just a fluke. Moreover, looking at some episodes. 
you can see that the agent hit a Zombie.
"""

# 3. Did it learn something?
"""
Let’s extract the policy your agent has learned by selecting the action with maximum Q value at each step,
 we will do that manually, like a boss. First up, the start_state:
"""

#print(start_state)
r = q(start_state)
print(f"up={r[UP]}, down={r[DOWN]}, left={r[LEFT]}, right={r[RIGHT]}")    

# UP seems to have the highest Q value, let’s take that action:
new_state, reward, done = act(start_state, UP)

r = q(new_state)
print(f"up={r[UP]}, down={r[DOWN]}, left={r[LEFT]}, right={r[RIGHT]}")  
