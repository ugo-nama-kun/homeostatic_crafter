import argparse
import pathlib
import time
import numpy as np

import homeostatic_crafter

import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--area', nargs=2, type=int, default=(64, 64))
    parser.add_argument('--length', type=int, default=10000)
    parser.add_argument('--health', type=int, default=9)
    parser.add_argument('--record', type=pathlib.Path, default=None)
    parser.add_argument('--episodes', type=int, default=1)
    args = parser.parse_args()
    
    random = np.random.RandomState(args.seed)
    homeostatic_crafter.constants.items['health']['max'] = args.health
    homeostatic_crafter.constants.items['health']['initial'] = args.health
    env = homeostatic_crafter.Env(area=args.area, length=args.length, seed=args.seed, random_health=True)
    env = homeostatic_crafter.Recorder(env, args.record)
    
    reward_hist = []
    health_hist = []
    
    for _ in range(args.episodes):
        
        start = time.time()
        obs = env.reset()
        print('')
        print(f'Reset time: {1000 * (time.time() - start):.2f}ms')
        print('Coal exist:    ', env._world.count('coal'))
        print('Iron exist:    ', env._world.count('iron'))
        print('Diamonds exist:', env._world.count('diamond'))
        
        start = time.time()
        done = False
        while not done:
            action = random.randint(0, env.action_space.n)
            obs, reward, done, info = env.step(action)
            
            reward_hist.append(reward)
            
            # print(info.keys())
            # print(f"health : {info['inventory']['health']}, thirst: {env._player._thirst}, hunger: {env._player._hunger}")
            # print(f"reward: {reward}")
            
            health_hist.append(info['normalized_health'])
        
        duration = time.time() - start
        step = env._step
        print(f'Step time: {1000 * duration / step:.2f}ms ({int(step / duration)} FPS)')
        print('Episode length:', step)
        
        plt.subplot(211)
        plt.plot(reward_hist)
        plt.subplot(212)
        plt.plot(health_hist)
        plt.plot(np.ones_like(health_hist) * 0.8, "--k", alpha=0.6)
        plt.show()


if __name__ == '__main__':
    main()
