# Navigazione Indoor utilizzando algoritmi di Reinforcement Learning Q-Learning e SARSA
Progetto nell'ambito del corso di Intelligenza Artificiale in cui abbiamo simulato la navigazione indoor di un agente robotico adibito alla pulizia.

Per costruire l'ambiente simulato abbiamo utilizzato la libreria *PyGame*, installabile tramite comando `pip install pygame`, inserendo nell'ambiente immagini, per rappresentare l'agente, gli ostacoli e i target, e una label per rappresentare il numero di target consecutivi acquisiti.

Per addestrare l'agente abbiamo utilizzato due algoritmi di reinforcement learning, il Q-Learning e il SARSA.

Per eseguire l'applicazione è possibile eseguire su linea di comando `python <ql_agent.py/sarsa_agent.py>`, ed analizzare gli action values generati esplorando i due file .csv generati dal codice.
