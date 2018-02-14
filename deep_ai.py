import numpy as np
import random
from interface import Interface
import RewardEnv


ACTIONS_DIM = 27
OBSERVATIONS_DIM = 27

def main():
    majhong_env = RewardEnv.RewardEnv()

    interface = Interface(1)

    while True:
        observation, done, reward = majhong_env.reset()
        old_observation = []
        last_action = None
        while True:
            interface.SendSample(old_observation, last_action, reward, observation, done)
            if done:
                print reward
                break
            last_action = interface.ReceiveAction()
            old_observation = observation
            observation, done, reward = majhong_env.step(last_action - 1)

if __name__ == "__main__":
    main()
