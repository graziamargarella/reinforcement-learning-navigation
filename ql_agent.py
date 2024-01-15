from enviroment import Enviroment
import numpy as np
import pandas as pd
import helper

# Optimized parameters
episodes = 1500
max_iter_episode = 5000
explo_proba = 1
explo_decre = 0.001
min_explo_proba = 0.01
gamma = 0.99
learning_rate = 0.001

class QlAgent:
    def __init__(self, enviroment):
        self.env = enviroment
        self.q_table = {}
        self.rewards = []
        self.scores = []
        self.mean_scores = []
        self.random = []
    
    # Export a csv of the q-table values (debugging function)
    def save_qtable(self):
        set = self.q_table
        result = pd.DataFrame(dict(set))
        result.to_csv('QL_q_table.csv')

    # Logging and plotting stats
    def logging_stats(self, episode_number, total_reward, score):
            print("For episode %s total reward %s" % (episode_number, total_reward))
            self.rewards.append(total_reward)
            self.scores.append(score)
            self.mean_scores.append(np.mean(self.scores))
            helper.plot(self.scores, self.mean_scores, self.random)
            print("Explo Proba %s" % explo_proba)
            self.save_qtable()

    # Return an action (and its rappresentation) using an epsilon-greedy stategy.
    def eps_greedy(self, obs):
        if obs not in self.q_table:
            self.q_table[obs] = np.zeros(4, dtype=np.double)
        if np.random.uniform(0, 1) < explo_proba:
            index = np.random.randint(0, 4)
        else:
            index = np.argmax(self.q_table[obs], axis=0)
        action = np.zeros(4)
        action[index] = 1
        return action, index
    
    # Execute the training of the agent
    def train(self):
        global explo_proba, explo_decre
        # Iteration on the episodes
        for e in range(episodes):
            print("EP %s" % e)
            obs = self.env.get_observations()
            self.random.append(explo_proba)
            # Decrease the exploration probability 
            if explo_proba > 0.01:
                explo_proba = explo_proba - explo_decre
            # Iteration on the possible action in a episode
            for i in range(max_iter_episode):
                action, index = self.eps_greedy(obs)
                reward, new_obs, finish, tot, score = self.env.execute_a_step(action)
                if new_obs not in self.q_table:
                    self.q_table[new_obs] = np.zeros(4)
                self.q_table[obs][index] = self.q_table[obs][index] + learning_rate * (reward + gamma *
                                        np.argmax(self.q_table[new_obs], axis=0) - self.q_table[obs][index])
                if finish:
                    break
                obs = new_obs
            self.logging_stats(e, tot,score)

if __name__ == "__main__":
    enviroment = Enviroment()
    QlAgent = QlAgent(enviroment)
    QlAgent.train()
    print(QlAgent.rewards)
