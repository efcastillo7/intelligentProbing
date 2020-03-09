import csv
import glob
# import math
import time
import random
import calendar
from argparse import ArgumentParser, RawDescriptionHelpFormatter, ArgumentDefaultsHelpFormatter
from textwrap import dedent

from environment import Agent, Environment
from simulator import Simulator
from planner import RoutePlanner

class LearningAgent(Agent):
    """An agent that learns how to probe in the states."""
    def __init__(self, env, init_value=0, gamma=0.90, alpha=0.20, epsilon=0.10,
                 discount_deadline=False, history=0):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color

        # simple route planner to get next_waypoint
        self.planner = RoutePlanner(self.env, self)
        ## Initialize the Q-function as a dictionary (state) of dictionaries (actions)
        self.q_function = {}
        ## Initial value of any (state, action) tuple is an arbitrary random number
        self.init_value = init_value
        ## Discount factor gamma: 0 (myopic) vs 1 (long-term optimal)
        self.gamma = gamma
        self.discount_deadline = discount_deadline
        ## Learning rate alpha: 0 (no learning) vs 1 (consider only most recent information)
        ## NOTE: Normally, alpha decreases over time: for example, alpha = 1 / t
        self.alpha = alpha
        ## Parameter of the epsilon-greedy action selection strategy
        ## NOTE: Normally, epsilon should also be decayed by the number of trials
        self.epsilon = epsilon
        ## The trial number
        self.trial = 1
        ## The cumulative reward
        self.cumulative_reward = 0

    def get_q_function(self):
        return self.q_function

    def set_params(self, init_value=0, gamma=0.90, alpha=0.20, epsilon=0.10,
                   discount_deadline=False, history=0):
        self.init_value = init_value
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount_deadline = discount_deadline
        self.history = history

    def reset(self, destination=None):
        self.planner.route_to(destination)
        self.env.set_trial_number(self.trial)
        self.trial += 1
        ## Decay the epsilon parameter
        #         self.epsilon = self.epsilon / math.sqrt(self.trial)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.cumulative_reward = 0

    def select_action(self, state=None, is_current=True, t=1):
        '''
        Implements the epsilon-greedy action selection that selects the best-valued action in this state
        (if is_current) with probability (1 - epsilon) and a random action with probability epsilon.
        't' is the current time step that can be used to modify epsilon.
        '''
        if state in self.q_function:
            ## Find the action that has the highest value
            action_function = self.q_function[state]
            q_action = max(action_function, key = action_function.get)
            if is_current:
                ## Generate a random action
                rand_action = random.choice(self.env.valid_actions)
                ## Select action using epsilon-greedy heuristic
                rand_num = random.random()
                action = q_action if rand_num <= (1 - self.epsilon) else rand_action
            else:
                action = q_action
        else:
            ## Initialize <state, action> pairs and select random action
            action_function = {}
            for action in self.env.valid_actions:
                action_function[action] = self.init_value
            self.q_function[state] = action_function
            action = random.choice(self.env.valid_actions)

        return action

    def update(self, t):
        '''
        At each time step t, the agent:
        - Is given the next waypoint (relative to its current location and direction)
        - Senses the network state (frequency, load, and cpu)
        - Gets the current deadline value (time remaining)
        '''
        ## Observe the current state variables
        ## (1) Overhead (CPU and LOAD) variables
        inputs = self.env.sense(self)
        print("SENSE AGENT", inputs)
        load = inputs['load']
        cpu_usage = inputs['cpu']
        probing_f = inputs['frequency']

        ## (2) Direction variables
        self.next_waypoint = self.planner.next_waypoint()

        ## Update the current observed state
        self.state = (load, cpu_usage, probing_f, self.next_waypoint)
        current_state = self.state  # save this for future use

        ## Select the current action
        action = self.select_action(state=current_state, is_current=True, t=t)

        ## Execute action, get reward and new state
        reward = self.env.act(self, action)
        self.cumulative_reward += reward
        self.env.set_cumulative_reward(self.cumulative_reward)

        ## Retrieve the current Q-value
        current_q = self.q_function[self.state][action]
        print 'Current Q = ' + str(current_q)

        ## Update the state variables after action
        ## (1) Traffic variables
        new_inputs = self.env.sense(self)
        #print("DOS", new_inputs)
        load = new_inputs['load']
        cpu_usage = new_inputs['cpu']
        probing_f = new_inputs['frequency']

        ## (2) Direction variables
        self.next_waypoint = self.planner.next_waypoint()

        if self.discount_deadline:
            deadline = self.env.get_deadline(self)
            if t == 1:
                ## TODO: Set this as an input param
		        self.gamma = 1 - float(4) / deadline

        ## Update the new state, which is a tuple of state variables
        self.state = (load, cpu_usage, probing_f, self.next_waypoint)
        ## Get the best q_action in the new state
        new_action = self.select_action(state=self.state, is_current=False, t=t)
        ## Get the new Q_value
        new_q = self.q_function[self.state][new_action]

        ## Update the Q-function
        #         current_alpha = 1 / math.sqrt(t+1)
        current_alpha = self.alpha
        self.q_function[current_state][action] = (1 - current_alpha) * current_q + current_alpha * (
                    reward + self.gamma * new_q)

        #print ("LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs,action, reward))

def run(params={}):

    n_trials = int(params['trials'])
    assert n_trials > 0, 'n_trials is less than 1: %r' % n_trials
    update_delay = float(params['delay'])
    assert update_delay > 0 and update_delay <= 1, 'update_delay is not in range: %f' % update_delay
    log_filename = str(params['log'])

    ## Learning parameters
    alpha = float(params['alpha'])
    assert alpha >= 0 and alpha <= 1, 'alpha is not in range: %f' % alpha
    gamma = float(params['gamma'])
    assert gamma >= 0 and gamma <= 1, 'gamma is not in range: %f' % gamma
    epsilon = float(params['epsilon'])
    assert epsilon >= 0 and epsilon <= 1, 'epsilon is not in range: %f' % epsilon
    initial = float(params['initial'])
    assert initial >= 0, 'initial is less than 0: %f' %initial

    ## Discount factor gamma depends on deadline?
    discount_deadline = params['deadline']
    assert discount_deadline is True or discount_deadline is False, 'discount_deadline is non-binary: %s' % discount_deadline


    ## Set up environment and agent
    ## Create a log file for the environment for each run
    fw = open(log_filename, 'w')
    #progress = ProgressBar(maxval=n_trials).start()
    env = Environment(fw=fw)
    ## Create agent primary agent
    agent = env.create_agent(LearningAgent)  # create a learning agent
    env.set_primary_agent(agent, enforce_deadline=True)
    agent.set_params(initial, gamma, alpha, epsilon, discount_deadline)

    # Now simulate it
    sim = Simulator(env, update_delay=update_delay)  # reduce update_delay to speed up simulation
    start_time = time.time()
    sim.run(n_trials=n_trials)

def parse():
    '''
    returns: A dictionary containing the parsed configuration setting
    '''
    class CustomFormatter(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
        pass
    parser = ArgumentParser(formatter_class=CustomFormatter)

    parser.add_argument('-n', '--trials', type=int, default=600, help='Number of trials')
    parser.add_argument('-d', '--delay', type=float, default=0.50, help='Update delay to control simulation speed')
    parser.add_argument('-l', '--log', type=str, default='../ipro.log', help='Log output file')
    parser.add_argument('-a', '--alpha', type=float, default=0.10, help='Learning rate')
    parser.add_argument('-g', '--gamma', type=float, default=0.80, help='Discount factor')
    parser.add_argument('-e', '--epsilon', type=float, default=0.10, help='Probability of random action')
    parser.add_argument('-i', '--initial', type=float, default=0.0, help='Initial value of any <state, action> pair')
    parser.add_argument('-t', '--deadline', action='store_true', default=True, help='Whether to have discount factor gamma dependent on deadline')
    #parser.add_argument('-w', '--history', type=int, default=0, help='Max number of stored Q-tables to remember and initialize')
    return vars(parser.parse_args())

if __name__ == '__main__':
    params = parse()
    run(params)
