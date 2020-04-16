import random

class RoutePlanner(object):

    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        self.destination = None

    def route_to(self, destination=None):
        self.destination = (destination if destination is not None else random.choice(self.env.intersections.keys()))

    def next_waypoint(self):
        '''
        Proposes the next state (based on simple heuristics) at each time step
        to make the agent closer to the destination if it is not reached yet.
        '''

        ## Get the current location and heading
        location = self.env.agent_states[self.agent]['location']
        heading = self.env.agent_states[self.agent]['heading']

        ## Distance from current location to destination (x,y)
        delta = (self.destination[0] - location[0], self.destination[1] - location[1])

        if delta[0] == 0 and delta[1] == 0: # has reached destination
            return None
        elif delta[0] != 0:
            if delta[0] * heading[0] > 0:
                return 'forward'
            elif delta[0] * heading[0] < 0:
                return 'right'
            elif delta[0] * heading[1] > 0:
                return 'left'
            else:
                return 'right'
        elif delta[1] != 0:
            if delta[1] * heading[1] > 0:
                return 'forward'
            elif delta[1] * heading[1] < 0:
                return 'right'
            elif delta[1] * heading[0] > 0:
                return 'right'
            else:
                return 'left'
