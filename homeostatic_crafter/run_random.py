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
    env = homeostatic_crafter.Env(area=args.area, length=args.length, seed=args.seed, random_internal=True)
    env = homeostatic_crafter.Recorder(env, args.record)
    
    reward_hist = []
    intero_hist = []
    
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
            obs, reward, done, truncated, info = env.step(action)
            done = done | truncated
            
            reward_hist.append(reward)
            
            # print(info.keys())
            print(f"health : {info['inventory']['health']}, thirst: {env._player._thirst}, hunger: {env._player._hunger}")
            print(info["interoception"])
            intero_hist.append(info['interoception'])
            # print(env.metadata)
            
            # plt.imshow(env.render((64, 64)))
            # plt.pause(0.0001)
        
        duration = time.time() - start
        step = env._step
        print(f'Step time: {1000 * duration / step:.2f}ms ({int(step / duration)} FPS)')
        print('Episode length:', step)

        plt.clf()
        plt.subplot(231)
        plt.plot(reward_hist)
        plt.title("reward")
        plt.subplot(232)
        plt.plot(intero_hist, label=["health", "food", "drink", "energy"])
        target = np.array(list(homeostatic_crafter.constants.homeostasis['target'].values()), dtype=np.float32)
        plt.plot(args.health * np.ones_like(intero_hist) * target, "--", alpha=0.6, label=["target_h", "target_f", "target_d", "target_e"])
        plt.ylim([-0.1, 9.1])
        plt.title("intero")
        plt.legend()
        plt.subplot(234)
        plt.imshow(obs["obs"][0])
        plt.subplot(235)
        plt.imshow(obs["obs"][1])
        plt.subplot(236)
        plt.imshow(obs["obs"][2])
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    main()
