import numpy as np
import random
import matplotlib.pyplot as plt

class FootballSimulatorMDP:
    def __init__(self, grid_size=(10, 5), n_opponents=5, delta=1):
        self.grid_size = grid_size
        self.n_opponents = n_opponents
        self.goal = (self.grid_size[0], self.grid_size[1]/2)
        self.delta = delta  # Distance threshold for losing the ball
        
        # Initialize opponents
        self.opponents = [(5,0), (7,2), (7,4) ,(8,4), (9,3)]
        # for _ in range(self.n_opponents):
        #     opp = (random.randint(self.grid_size[0]/2, self.grid_size[0] - 1),
        #      random.randint(0, self.grid_size[1] - 1)) 
        #     while opp in self.opponents:
        #         opp = (random.randint(self.grid_size[0]/2, self.grid_size[0] - 1),
        #      random.randint(0, self.grid_size[1] - 1)) 
        #     self.opponents.append(opp)
        
        self.reset()

    def reset(self):
        # Initialize player position
        
        self.player_pos = (random.randint(0, self.grid_size[0]/2 - 1),
                random.randint(0, self.grid_size[1] - 1))
        while self.player_pos in self.opponents:
            self.player_pos = (random.randint(0, self.grid_size[0]/2 - 1),
                           random.randint(0, self.grid_size[1] - 1))
        # self.player_pos = (0, int(self.grid_size[1]/2))
        self.is_done = False
        return self.get_state()

    def get_state(self):
        # State includes player position and opponents' positions
        return self.player_pos

    def step(self, action):
        # if self.is_done:
        #     raise Exception("Game is over. Reset the environment.")
        
        # Update player's position or attempt a shoot
        if action in ['up', 'down', 'left', 'right']:
            self.move_player(action)
        elif action == 'shoot':
            return self.shoot()

        # Check for ball loss
        if self.check_loss():
            self.is_done = True
            return self.get_state(), -10, self.is_done, {}

        # Per-step penalty
        return self.get_state(), -0.05, self.is_done, {}

    def move_player(self, action):
        x, y = self.player_pos
        if action == 'down' and y > 0:
            y -= 1
        elif action == 'up' and y < self.grid_size[1] - 1:
            y += 1
        elif action == 'left' and x > 0:
            x -= 1
        elif action == 'right' and x < self.grid_size[0] - 1:
            x += 1
        self.player_pos = (x, y)

    def shoot(self):
        # Calculate probability of scoring based on distance
        distance = np.sqrt((self.goal[0] - self.player_pos[0])**2 + (self.goal[1] - self.player_pos[1])**2)
        prob_success = max(0.1, 1 - (distance / self.grid_size[0]))
        self.is_done = True

        # Check if any opponent blocks the shot
        for opp in self.opponents:
            if self.is_in_shooting_line(opp):
                return self.get_state(), -8, self.is_done, {0}

        # Attempt the shot
        if random.random() < prob_success:
            print(f"Goal! Scored from: {self.get_state()}")
            return self.get_state(), 10, self.is_done, {prob_success}
        else:
            print(f"Missed! Shot from: {self.get_state()}")
            return self.get_state(), -5, self.is_done, {prob_success}

    def is_in_shooting_line(self, opponent):
        px, py = self.player_pos
        gx, gy = self.goal
        ox, oy = opponent
        if min(px, gx) < ox < max(px, gx):
            y_loc = ((ox - px)*((gy - py)/(gx - px))) + py
            if (y_loc > oy and oy + self.delta > y_loc) or (y_loc < oy and oy - self.delta < y_loc): 
            # if min(py, gy) <= oy <= max(py, gy):
                print(f"Shot Blocked! Shot from: {self.player_pos}, and blocked by: {opponent}")
                return True
        return False

    def check_loss(self):
        px, py = self.player_pos
        for ox, oy in self.opponents:
            if np.sqrt((px - ox)**2 + (py - oy)**2) < self.delta:
                print("Ball Lost!")
                return True
        return False
    


