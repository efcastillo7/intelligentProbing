import time
import random
from collections import OrderedDict
import numpy as np
import sys
sys.path.insert(0, '/home/ryu/ryu/ryu/app/intelligentProbing/database/')
import ConnectionBD_v2

class TrafficLight(object):
    """
    A traffic light that switches state periodically.
    """
    
    valid_states = [True, False]  # True = NS open, False = EW open
    
    def __init__(self, state=None, period=None):
        self.state = state if state is not None else random.choice(self.valid_states)
        ## The random period of being in one state {NS, EW}
        self.period = period if period is not None else random.choice([3, 4, 5])
        self.last_updated = 0
    
    def reset(self):
        self.last_updated = 0
    
    def update(self, t):
        '''
        Switches the state {NS, EW} of the traffic light.
        '''
        if t - self.last_updated >= self.period:
            self.state = not self.state  # assuming state is boolean
            self.last_updated = t
            
class Environment(object):
    """
    An environment in which the agent interact with.
    """
    #None = 'equal'
    valid_actions = [None, 'forward', 'left', 'right']
    valid_headings = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # East, North, West, South
        
    def __init__(self, fw=None, progress=None):
        self.done = False
        self.t = 0
        self.agent_states = OrderedDict()
        self.status_text = ""
        ## Added variables
        self.fw = fw # the log file writer
        self.cumulative_reward = 0
        self.trial = 0 # the trial number
        self.cumulative_rewards = []

        self.progress = progress  # the progress bar
        self.success_trials = []
                         
        # Primary agent
        self.primary_agent = None  # to be set explicitly
        self.enforce_deadline = False

        # Reward Parameter
        self.goal_load = 700
        self.goal_cpu = 40  
        self.sigma = 7  #standard deviation

        # Road network
        self.grid_size = (6, 5)  # (cols, rows)
        self.bounds = (1, 1, self.grid_size[0], self.grid_size[1])
        self.probing_frequencies = []
        self.block_size = 100
        self.intersections = OrderedDict()
        self.roads = []
        self.probing_frequency = 3
        self.current_network_state = {}
        self.current_value_network_state = {}

        ## Put a traffic light at each intersection
        for x in xrange(self.bounds[0], self.bounds[2] + 1):
            for y in xrange(self.bounds[1], self.bounds[3] + 1):
                self.intersections[(x, y)] = TrafficLight()  # a traffic light at each intersectio
        
        ## Set equal length (1) for all segments
        for a in self.intersections:
            for b in self.intersections:
                if a == b:
                    continue
                if (abs(a[0] - b[0]) + abs(a[1] - b[1])) == 1:  # L1 distance = 1
                    self.roads.append((a, b))
        
        # Set probing frequencies
        for k in xrange(1,self.grid_size[0]* self.grid_size[1] + 1):
            self.probing_frequencies.append(float(k))
        # Primary agent
        self.primary_agent = None  # to be set explicitly
        self.enforce_deadline = False

    def set_cumulative_reward(self, cumulative_reward=0):
        self.cumulative_reward = cumulative_reward
    
    def set_trial_number(self, trial=0):
        self.trial = trial
        if self.progress is not None:
            self.progress.update(trial-1)
    
    def get_success_trials(self):
        return self.success_trials
    
    def get_cumulative_rewards(self):
        return self.cumulative_rewards    

    def create_agent(self, agent_class, *args, **kwargs):
        agent = agent_class(self, *args, **kwargs)
        ## All agents initially head South?
        self.agent_states[agent] = {'location': random.choice(self.intersections.keys()), 'heading': (0, 1)}
        print("Created agent", self.agent_states[agent])
        return agent

    def set_primary_agent(self, agent, enforce_deadline=False):
        self.primary_agent = agent
        self.enforce_deadline = enforce_deadline
    
    def set_probing_frequency(self,probing_frequency):
        self.probing_frequency = probing_frequency
        
    def set_current_network_state(self,current_network_state):
        self.current_network_state = current_network_state

    def set_value_current_network_state(self,current_value_network_state):
        self.current_value_network_state = current_value_network_state    
    
    def reset(self):
        self.done = False
        self.t = 0
        # Pick random start (origin) and destination
        start = random.choice(self.intersections.keys())
        destination = random.choice(self.intersections.keys())
        
        # Ensure starting location and destination are not too close
        while self.compute_dist(start, destination) < 4:
            start = random.choice(self.intersections.keys())
            destination = random.choice(self.intersections.keys())

        ## Set random start heading (N, S, E, W)
        start_heading = random.choice(self.valid_headings)
        deadline = self.compute_dist(start, destination) * 5
        #print ("Environment.reset(): Trial set up with start = {}, destination = {}, deadline = {}".format(start, destination, deadline))

        # Initialize the agent
        for agent in self.agent_states.iterkeys():
            self.agent_states[agent] = {
                'location': start if agent is self.primary_agent else random.choice(self.intersections.keys()),
                'heading': start_heading if agent is self.primary_agent else random.choice(self.valid_headings),
                'destination': destination if agent is self.primary_agent else None,
                'deadline': deadline if agent is self.primary_agent else None}
            agent.reset(destination=(destination if agent is self.primary_agent else None))
        
    def compute_dist(self, a, b):
        """L1 distance between two points."""
        return abs(b[0] - a[0]) + abs(b[1] - a[1])
        
    def step(self):
        '''
        Update the agents' observations (states)
        '''
        #print "Environment.step(): t = {}".format(self.t)  # [debug]

        for intersection, traffic_light in self.intersections.iteritems():
            traffic_light.update(self.t)
        
        for agent in self.agent_states.iterkeys():
            agent.update(self.t)
        #print(self.probing_frequency)

        self.t += 1

        if self.primary_agent is not None:
            if self.enforce_deadline and self.agent_states[self.primary_agent]['deadline'] <= 0:
                self.done = True
                output_str = str(self.trial) + ". Environment.reset(): Primary agent could not reach destination within deadline!\n"
                output_str += 'Cumulative reward = ' + str(self.cumulative_reward)

                ## Record the failure trial
                self.success_trials.append(False)
                self.cumulative_rewards.append(self.cumulative_reward)
            self.agent_states[self.primary_agent]['deadline'] -= 1  # decrement the deadline of primary agent
            print("Agent Step", self.agent_states[self.primary_agent])
    
    def sense(self, agent):
        '''
            We get the state of control channel and cpu usage
        '''
        ## Make sure the agent is one of those created
        assert agent in self.agent_states, "Unknown agent!"
        state = self.agent_states[agent]

        
        return self.current_network_state
    
    def get_deadline(self, agent):
        return self.agent_states[agent]['deadline'] if agent is self.primary_agent else None

    def gaussian(self, x, mu, sig):
        return round(np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.))),3)
    
    def act(self, agent, action):
        assert agent in self.agent_states, "Unknown agent!"
        assert action in self.valid_actions, "Invalid action!"
        #https://medium.com/@annishared/searching-for-optimal-policies-in-python-an-intro-to-optimization-7182d6fe4dba
                
        #STATES PARAMETERS
        cpu_usage = self.current_network_state['cpu']
        probing_f = self.current_network_state['frequency']
        load = self.current_network_state['load']
        #VALUES OF THE STATES PARAMETERS
        load_value_tx = self.current_value_network_state['load_tx']
        load_value_rx = self.current_value_network_state['load_rx']
        cpu_value = self.current_value_network_state['cpu']

        #print("VALUES", load_value_tx, load_value_rx, cpu_value)

        state = self.agent_states[agent]  # the agent's current state
        location = state['location']
        heading = state['heading']
        
        # Move the agent if within bounds and obey traffic rules
        ## Note that the prescribed action translates into the new heading
        reward = 0  # reward/penalty
        move_okay = True
        if action == 'forward':
            if load == 'load_error':
                move_okay = False
                probing_f += 4
        elif action == 'left':
            ## Reduces current monitoring interval if the control channel is available
            if probing_f in self.probing_frequencies:
                if load != 'load_error':
                    if probing_f < 30 and probing_f > 0:
                        if cpu_usage != "cpu_error":
                            probing_f -= 1
                            heading = (heading[1], -heading[0]) # update the heading tuple
                        else:
                            move_okay = False
                    else:
                        move_okay = False
                else:
                    move_okay = False                           
            else:
                move_okay = False
        elif action == 'right':
            ## Increases current monitoring interval
            if probing_f in self.probing_frequencies:
                if probing_f < 30:
                    probing_f += 1
                    heading = (-heading[1], heading[0]) # update the heading tuple
                else:
                    move_okay = False    
            else:
                move_okay = False
                            
        if action is not None:
            ## Update the current monitoring interval
            #DB
            ConnectionBD_v2.updateProbingFrequency(probing_f)
            
            ## Update the current location (intersection)
            location = (
                (location[0] + heading[0] - self.bounds[0]) % (self.bounds[2] - self.bounds[0] + 1) + self.bounds[
                    0],
                (location[1] + heading[1] - self.bounds[1]) % (self.bounds[3] - self.bounds[1] + 1) + self.bounds[
                    1])  # wrap-around
            
            ## Update the location and heading
            state['location'] = location
            state['heading'] = heading
    
            if move_okay:
                # Reward if action matches next waypoint
                reward = 2 if action == agent.get_next_waypoint() else 0.5
            else:
                ## Penalize if action violates traffic rules
                reward = -1
        else:
            ## Reward for doing nothing -- this gives a high tendency to do nothing!
            reward = 1

        if agent is self.primary_agent:
            if state['deadline'] >= 0:
                reward += float(self.gaussian(load_value_tx+load_value_rx, self.goal_load, self.sigma)) + float(self.gaussian(cpu_value,self.goal_cpu, self.sigma)) 
                output_str = str(self.trial) + ". Environment.act(): Primary agent has reached destination!\n"  # [debug]
                # Record the success trial
                self.success_trials.append(True)
            else:
                output_str = str(self.trial) + ". Environment.act(): Primary agent has reached destination exceeding deadline!\n"  # [debug]
                ## Record the failure trial
                self.success_trials.append(False)
        
            self.cumulative_reward += reward
            output_str += 'Cumulative reward = ' + str(self.cumulative_reward)
            # print (output_str)
            self.fw.write(output_str + '\n')
            self.cumulative_rewards.append(self.cumulative_reward)
            self.done = True           
    
            self.status_text = "state: {}\naction: {}\nreward: {}".format(agent.get_state(), action, reward)
            print "Environment.act() [POST]: location: {}, heading: {}, action: {}, reward: {}".format(location, heading, action, reward)  # [debug]

        print("CUMULATIVE REWARDS",self.cumulative_rewards)
        print("TRIAL",self.trial)
        return reward
        #mu = random.randint(0,100)
        #print("MU",mu, "REWARD",float(self.gaussian(5,mu,2)))

class Agent(object):
    """Base class for all agents."""
    
    def __init__(self, env):
        self.env = env
        self.state = None
        self.next_waypoint = None
        self.color = 'cyan'

    def reset(self, destination=None):
        pass

    def update(self, t):
        pass

    def get_state(self):
        return self.state

    def get_next_waypoint(self):
        return self.next_waypoint
    
    def set_params(self):
        pass
    
    
    '''
    import os
    os.system("some_command &")
    '''