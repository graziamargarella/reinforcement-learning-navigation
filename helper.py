import matplotlib.pyplot as plt
from IPython import display

plt.ion()

"""
Define and execute a run-time visualization.

Parameters:
- scores (list): Values of the scores that the agent reaches at the end of each episode
- mean_scores (list): Value of the mean of the scores for each episode
- random (list): Values of the exploration probability through episodes
"""
def plot(scores, mean_scores,random):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.figure(1)
    # Score per episode
    plt.subplot(211)
    plt.title('Score per Episode')
    plt.xlabel('Number of Episode')
    plt.ylabel('Score\n')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], '%.3f'%(mean_scores[-1]))
    # Exploration probability per episode
    plt.subplot(212)
    plt.title('Proba per Episode')
    plt.xlabel('Number of Episode')
    plt.ylabel('Proba\n')
    plt.plot(random)
    plt.text(len(random) - 1, random[-1], '%.3f'%(random[-1]))
    plt.show(block=False)
    plt.tight_layout()
    plt.pause(.1)