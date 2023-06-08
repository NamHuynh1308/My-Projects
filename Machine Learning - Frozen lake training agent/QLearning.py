#Q-Learning

import gym
import numpy as np
import time

maze_size = input("Type in maze_size (format: numxnum): ")
iterations = int(input("Get number of iterations: "))

#set up environment
env = gym.make('FrozenLake-v1', map_name = maze_size, render_mode="human", is_slippery=False)
env.reset()
env.render() 

#set up Q-Table with size base on the created maze
Q = np.zeros([env.observation_space.n, env.action_space.n])

#default variable
alpha = 0.05
gamma = 0.9
egreedy = 0.7
epsilon = 0.1
egreedy_decay = 0.999

# Using Q_Learning
for i in range(iterations):
    #store number of steps for each iteration
    num_steps = 0
    #get the starting state with the probability
    state, probability = env.reset()
    #variable to check if the agent fall down to holes or finish the maze
    done = False
    
    while not done:
        #count the steps    
        num_steps += 1
        
        #greedy-epsilon policy
        #get action for current state
        random_egreedy = np.random.random()
        
        if random_egreedy > egreedy:      
            random_values = Q[state] + np.random.rand(1, env.action_space.n) / 1000      
            action = np.argmax(random_values, axis=1)[0] 
            action = action.item()
        else:
            #get action
            action = env.action_space.sample()
            
        if egreedy > epsilon:
            egreedy *= egreedy_decay
        
        #get to next state    
        next_state, reward, done, _, _ = env.step(action)

        #filling data in Q-Table
        Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        
        #move on to next state
        state = next_state

        #if the agent fell down to any holes or finished, exit that iteration
        if done:
            print('Number of iterations: {}, Reward: {}, Number of steps: {}'.format(i+1, reward, num_steps))
            break  

# Close the environment
env.close()
