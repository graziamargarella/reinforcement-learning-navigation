from enviroment import Enviroment
import numpy as np
import pandas as pd
import helper

episodes = 3000
max_iter_episode = 10000
explo_proba = 1
explo_decre = 0.01
min_explo_proba = 0.01
gamma = 0.99
learning_rate = 0.001 #0.001


class QlAgent:

    def __init__(self, enviroment):
        self.env = enviroment
        self.q_table = {}
        self.rewards = []
        self.scores = []
        self.mean_scores = []
        self.random = []

    def save_qtable(self):
        set = self.q_table
        result = pd.DataFrame(dict(set))
        result.to_csv('q_table.csv')

    def train(self):
        global explo_proba
        for e in range(episodes):
            print("EP %s" % e)
            obs = self.env.get_observations()
            self.random.append(explo_proba)
            for i in range(max_iter_episode):
                if obs not in self.q_table:
                    self.q_table[obs] = np.zeros(4, dtype=np.double)
                if np.random.uniform(0, 1) < explo_proba:
                    index = np.random.randint(0, 4)
                else:
                    index = np.argmax(self.q_table[obs], axis=0)
                    print("Obs %s" % str(obs))
                    print("Max %s %s" % (str(index), str(self.q_table[obs])))
                action = np.zeros(4)
                action[index] = 1
                reward, new_obs, finish, tot, score = self.env.execute_a_step(action)
                if new_obs not in self.q_table:
                    self.q_table[new_obs] = np.zeros(4)
                # self.q_table[obs][index] = self.q_table[obs][index] + learning_rate * (
                #        reward + gamma * np.argmax(self.q_table[new_obs], axis=0))
                self.q_table[obs][index] = ((1 - learning_rate) * (self.q_table[obs][index]) + learning_rate *
                                            (reward + gamma * np.argmax(self.q_table[new_obs], axis=0)))
                if finish:
                    break
                obs = new_obs
            explo_proba = max(min_explo_proba, explo_proba - 2 / episodes)
            print("For episode %s total reward %s" % (e, tot))
            self.rewards.append(tot)
            self.scores.append(score)
            self.mean_scores.append(np.mean(self.scores))
            helper.plot(self.scores, self.mean_scores, self.random)
            print("Explo Proba %s" % explo_proba)
            self.save_qtable()


if __name__ == "__main__":
    enviroment = Enviroment()
    QlAgent = QlAgent(enviroment)
    QlAgent.train()
    print(QlAgent.rewards)
