"""Interactive training script for BipedalWalker.

Allows watching the agent learn in real-time.
Controls:
  T - Toggle training (Eval / Train)
  R - Reset agent
  S - Save checkpoint
  Q - Quit
"""
import argparse
import sys
import os
import pygame
import numpy as np
import gymnasium as gym
import torch

from train import PPOConfig, PPOAgent

def main():
    parser = argparse.ArgumentParser(description="Interactive BipedalWalker")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--checkpoint", type=str, default="checkpoints/interactive_agent.pt")
    args = parser.parse_args()

    # Config
    config = PPOConfig()
    config.n_steps = 1024  # Smaller batch for more frequent updates in interactive
    
    # Create env with rendering
    env = gym.make("BipedalWalkerHardcore-v3", render_mode="human")
    # env = gym.make("BipedalWalker-v3", render_mode="human")  # Easy mode
    
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    
    # Create agent
    agent = PPOAgent(state_dim, action_dim, config)
    
    # Check for existing checkpoint
    if os.path.exists(args.checkpoint):
        print(f"Loading checkpoint: {args.checkpoint}")
        agent.load(args.checkpoint)
    
    print("\nControls:")
    print("  T: Toggle Training/Eval")
    print("  R: Reset Agent")
    print("  S: Save Checkpoint")
    print("  Q: Quit")
    
    training = False  # Start in EVAL mode to see initial performance
    state, _ = env.reset(seed=args.seed)
    episode_reward = 0
    steps = 0
    
    running = True
    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_t:
                    training = not training
                    mode = "TRAIN" if training else "EVAL"
                    print(f"Switched to {mode} mode")
                    # Clear buffer if switching modes to avoid mixing
                    agent.buffer.clear()
                elif event.key == pygame.K_r:
                    print("Resetting agent...")
                    agent = PPOAgent(state_dim, action_dim, config)
                elif event.key == pygame.K_s:
                    agent.save(args.checkpoint)
                    print(f"Saved to {args.checkpoint}")

        # Select action
        # If training, sample from distribution. If eval, deterministic.
        if training:
            action, log_prob, value = agent.select_action(state, deterministic=False)
        else:
            # For PPO, eval often uses deterministic mean
            action, log_prob, value = agent.select_action(state, deterministic=True)
            
        # Step
        next_state, reward, done, truncated, _ = env.step(action)
        
        # Store if training
        if training:
            agent.buffer.add(state, action, reward, done or truncated, log_prob, value)
            
            # Update if buffer full
            if len(agent.buffer.states) >= config.n_steps:
                print(f"Updating agent... (Reward: {episode_reward:.1f})")
                # Need value of next state
                _, _, last_value = agent.select_action(next_state)
                loss = agent.update(last_value)
                print(f"  Update complete. Loss: {loss:.4f}")

        state = next_state
        episode_reward += reward
        steps += 1
        
        if done or truncated:
            print(f"Episode finished. Reward: {episode_reward:.1f}")
            state, _ = env.reset()
            episode_reward = 0
            steps = 0
            
    env.close()

if __name__ == "__main__":
    main()
