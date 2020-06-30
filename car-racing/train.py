import gym
import torch
import numpy as np
from ddpg_agent import Agent
import matplotlib.pyplot as plt

env = gym.make('CarRacing-v0')

state_dim = env.observation_space.shape
action_dim = env.action_space.shape[0]

print(state_dim)
print(action_dim)

# agent = Agent(state_size=state_dim, action_size=action_dim, random_seed=0)


def ddpg(episodes, step, pretrained, noise):

    if pretrained:
        agent.actor_local.load_state_dict(torch.load('1checkpoint_actor.pth', map_location="cpu"))
        agent.critic_local.load_state_dict(torch.load('1checkpoint_critic.pth', map_location="cpu"))
        agent.actor_target.load_state_dict(torch.load('1checkpoint_actor.pth', map_location="cpu"))
        agent.critic_target.load_state_dict(torch.load('1checkpoint_critic.pth', map_location="cpu"))

    reward_list = []

    for i in range(episodes):

        state = env.reset()
        score = 0

        for t in range(step):

            env.render()

            # action = agent.act(state, noise)
            action = [0, .01, 0]
            next_state, reward, done, info = env.step(action)
            # agent.step(state, action, reward, next_state, done)
            state = next_state.squeeze()
            score += reward

            if done:
                print('Reward: {} | Episode: {}/{}'.format(score, i, episodes))
                break

        reward_list.append(score)

        if score >= 270:
            print('Task Solved')
            torch.save(agent.actor_local.state_dict(), 'checkpoint_actor.pth')
            torch.save(agent.critic_local.state_dict(), 'checkpoint_critic.pth')
            torch.save(agent.actor_target.state_dict(), 'checkpoint_actor_t.pth')
            torch.save(agent.critic_target.state_dict(), 'checkpoint_critic_t.pth')
            break

    torch.save(agent.actor_local.state_dict(), 'checkpoint_actor.pth')
    torch.save(agent.critic_local.state_dict(), 'checkpoint_critic.pth')
    torch.save(agent.actor_target.state_dict(), 'checkpoint_actor_t.pth')
    torch.save(agent.critic_target.state_dict(), 'checkpoint_critic_t.pth')

    print('Training saved')
    return reward_list


scores = ddpg(episodes=100, step=2000, pretrained=0, noise=0)

fig = plt.figure()
plt.plot(np.arange(1, len(scores) + 1), scores)
plt.ylabel('Score')
plt.xlabel('Episode #')
plt.show()