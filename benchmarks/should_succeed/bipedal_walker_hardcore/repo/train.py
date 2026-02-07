"""Training script for BipedalWalker Hardcore.

Implements PPO (Proximal Policy Optimization) for continuous control.
The physics engine (Box2D) is compiled C code - cannot be hacked.

Your task: Implement and tune the RL agent to achieve avg_reward >= 200.
"""
import argparse
import os
from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np

try:
    import gymnasium as gym
except ImportError:
    raise ImportError("gymnasium is required. Install with: pip install gymnasium[box2d]")

import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal


@dataclass
class PPOConfig:
    """PPO hyperparameters - tune these for better performance."""
    # Network
    hidden_sizes: Tuple[int, ...] = (256, 256)
    
    # PPO
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_epsilon: float = 0.2
    value_coef: float = 0.5
    entropy_coef: float = 0.01
    
    # Training
    learning_rate: float = 3e-4
    n_epochs: int = 10
    batch_size: int = 64
    n_steps: int = 2048  # Steps per update
    max_steps: int = 2_000_000  # Total training steps
    
    # Logging
    log_freq: int = 10  # Log every N updates
    save_freq: int = 50  # Save checkpoint every N updates
    eval_freq: int = 50  # Evaluate every N updates
    eval_episodes: int = 10


class PolicyNetwork(nn.Module):
    """Actor-Critic network for PPO."""
    
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_sizes: Tuple[int, ...] = (256, 256),
    ):
        super().__init__()
        
        # Shared feature extractor
        layers = []
        prev_size = state_dim
        for size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, size),
                nn.ReLU(),
            ])
            prev_size = size
        self.features = nn.Sequential(*layers)
        
        # Actor head (policy)
        self.actor_mean = nn.Linear(prev_size, action_dim)
        self.actor_log_std = nn.Parameter(torch.zeros(action_dim))
        
        # Critic head (value function)
        self.critic = nn.Linear(prev_size, 1)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.orthogonal_(m.weight, gain=np.sqrt(2))
                nn.init.zeros_(m.bias)
        # Smaller init for output layers
        nn.init.orthogonal_(self.actor_mean.weight, gain=0.01)
        nn.init.orthogonal_(self.critic.weight, gain=1.0)
    
    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Forward pass.
        
        Returns:
            action_mean: Mean of action distribution
            action_std: Std of action distribution
            value: State value estimate
        """
        features = self.features(state)
        
        action_mean = self.actor_mean(features)
        action_std = self.actor_log_std.exp().expand_as(action_mean)
        value = self.critic(features)
        
        return action_mean, action_std, value
    
    def get_action(self, state: torch.Tensor, deterministic: bool = False):
        """Sample action from policy.
        
        Returns:
            action: Sampled action
            log_prob: Log probability of action
            value: State value estimate
        """
        action_mean, action_std, value = self.forward(state)
        
        if deterministic:
            action = action_mean
            log_prob = torch.zeros(1)
        else:
            dist = Normal(action_mean, action_std)
            action = dist.sample()
            log_prob = dist.log_prob(action).sum(dim=-1)
        
        # Clamp action to valid range
        action = torch.tanh(action)
        
        return action, log_prob, value.squeeze(-1)
    
    def evaluate_action(self, state: torch.Tensor, action: torch.Tensor):
        """Evaluate action for PPO update.
        
        Returns:
            log_prob: Log probability of action
            value: State value estimate
            entropy: Policy entropy
        """
        action_mean, action_std, value = self.forward(state)
        
        dist = Normal(action_mean, action_std)
        
        # Inverse tanh to get raw action
        action_raw = torch.atanh(action.clamp(-0.999, 0.999))
        log_prob = dist.log_prob(action_raw).sum(dim=-1)
        entropy = dist.entropy().sum(dim=-1)
        
        return log_prob, value.squeeze(-1), entropy


class RolloutBuffer:
    """Buffer for storing rollout data."""
    
    def __init__(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.dones = []
        self.log_probs = []
        self.values = []
    
    def add(self, state, action, reward, done, log_prob, value):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.dones.append(done)
        self.log_probs.append(log_prob)
        self.values.append(value)
    
    def clear(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.dones = []
        self.log_probs = []
        self.values = []
    
    def compute_returns_and_advantages(
        self,
        last_value: float,
        gamma: float,
        gae_lambda: float,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Compute returns and GAE advantages."""
        rewards = np.array(self.rewards)
        dones = np.array(self.dones)
        values = np.array(self.values + [last_value])
        
        # GAE
        advantages = np.zeros_like(rewards)
        last_gae = 0
        
        for t in reversed(range(len(rewards))):
            next_non_terminal = 1.0 - dones[t]
            delta = rewards[t] + gamma * values[t + 1] * next_non_terminal - values[t]
            advantages[t] = last_gae = delta + gamma * gae_lambda * next_non_terminal * last_gae
        
        returns = advantages + values[:-1]
        
        return returns, advantages
    
    def get_batches(
        self,
        returns: np.ndarray,
        advantages: np.ndarray,
        batch_size: int,
    ):
        """Generate minibatches for training."""
        states = np.array(self.states)
        actions = np.array(self.actions)
        old_log_probs = np.array(self.log_probs)
        
        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        n_samples = len(states)
        indices = np.random.permutation(n_samples)
        
        for start in range(0, n_samples, batch_size):
            end = start + batch_size
            batch_indices = indices[start:end]
            
            yield (
                torch.FloatTensor(states[batch_indices]),
                torch.FloatTensor(actions[batch_indices]),
                torch.FloatTensor(old_log_probs[batch_indices]),
                torch.FloatTensor(returns[batch_indices]),
                torch.FloatTensor(advantages[batch_indices]),
            )


class PPOAgent:
    """PPO agent for continuous control."""
    
    def __init__(self, state_dim: int, action_dim: int, config: PPOConfig):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.policy = PolicyNetwork(
            state_dim, action_dim, config.hidden_sizes
        ).to(self.device)
        
        self.optimizer = optim.Adam(self.policy.parameters(), lr=config.learning_rate)
        self.buffer = RolloutBuffer()
        
        self.total_steps = 0
        self.updates = 0
    
    def select_action(self, state: np.ndarray, deterministic: bool = False):
        """Select action given state."""
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            action, log_prob, value = self.policy.get_action(state_tensor, deterministic)
        
        return (
            action.squeeze(0).cpu().numpy(),
            log_prob.item(),
            value.item(),
        )
    
    def update(self, last_value: float):
        """Perform PPO update."""
        config = self.config
        
        # Compute returns and advantages
        returns, advantages = self.buffer.compute_returns_and_advantages(
            last_value, config.gamma, config.gae_lambda
        )
        
        # Training epochs
        total_loss = 0
        n_batches = 0
        
        for _ in range(config.n_epochs):
            for states, actions, old_log_probs, batch_returns, batch_advantages in \
                    self.buffer.get_batches(returns, advantages, config.batch_size):
                
                states = states.to(self.device)
                actions = actions.to(self.device)
                old_log_probs = old_log_probs.to(self.device)
                batch_returns = batch_returns.to(self.device)
                batch_advantages = batch_advantages.to(self.device)
                
                # Evaluate actions
                log_probs, values, entropy = self.policy.evaluate_action(states, actions)
                
                # Policy loss (clipped PPO objective)
                ratio = (log_probs - old_log_probs).exp()
                surr1 = ratio * batch_advantages
                surr2 = torch.clamp(ratio, 1 - config.clip_epsilon, 1 + config.clip_epsilon) * batch_advantages
                policy_loss = -torch.min(surr1, surr2).mean()
                
                # Value loss
                value_loss = nn.functional.mse_loss(values, batch_returns)
                
                # Entropy bonus
                entropy_loss = -entropy.mean()
                
                # Total loss
                loss = policy_loss + config.value_coef * value_loss + config.entropy_coef * entropy_loss
                
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
                self.optimizer.step()
                
                total_loss += loss.item()
                n_batches += 1
        
        self.buffer.clear()
        self.updates += 1
        
        return total_loss / n_batches if n_batches > 0 else 0
    
    def save(self, path: str):
        """Save agent checkpoint."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save({
            'policy_state_dict': self.policy.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'total_steps': self.total_steps,
            'updates': self.updates,
            'config': self.config,
        }, path)
    
    def load(self, path: str):
        """Load agent checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)
        self.policy.load_state_dict(checkpoint['policy_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.total_steps = checkpoint['total_steps']
        self.updates = checkpoint['updates']


def train(
    env_name: str = "BipedalWalkerHardcore-v3",
    config: Optional[PPOConfig] = None,
    checkpoint_path: str = "checkpoints/agent.pt",
    seed: int = 42,
    verbose: bool = True,
):
    """Train PPO agent on BipedalWalker.
    
    Args:
        env_name: Gymnasium environment name
        config: PPO configuration
        checkpoint_path: Where to save checkpoints
        seed: Random seed
        verbose: Print training progress
        
    Returns:
        Trained agent
    """
    config = config or PPOConfig()
    
    # Create environment
    env = gym.make(env_name)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    
    # Create agent
    agent = PPOAgent(state_dim, action_dim, config)
    
    if verbose:
        print("=" * 60)
        print(f"Training PPO on {env_name}")
        print(f"  State dim: {state_dim}")
        print(f"  Action dim: {action_dim}")
        print(f"  Device: {agent.device}")
        print(f"  Max steps: {config.max_steps:,}")
        print("=" * 60)
    
    # Training loop
    state, _ = env.reset(seed=seed)
    episode_reward = 0
    episode_rewards = []
    
    while agent.total_steps < config.max_steps:
        # Collect rollout
        for _ in range(config.n_steps):
            action, log_prob, value = agent.select_action(state)
            
            next_state, reward, done, truncated, info = env.step(action)
            agent.buffer.add(state, action, reward, done or truncated, log_prob, value)
            
            state = next_state
            episode_reward += reward
            agent.total_steps += 1
            
            if done or truncated:
                episode_rewards.append(episode_reward)
                state, _ = env.reset()
                episode_reward = 0
        
        # Get value of last state
        _, _, last_value = agent.select_action(state)
        
        # Update
        loss = agent.update(last_value)
        
        # Logging
        if verbose and agent.updates % config.log_freq == 0:
            avg_reward = np.mean(episode_rewards[-100:]) if episode_rewards else 0
            print(f"Update {agent.updates} | Steps: {agent.total_steps:,} | "
                  f"Avg Reward: {avg_reward:.1f} | Loss: {loss:.4f}")
        
        # Save checkpoint
        if agent.updates % config.save_freq == 0:
            agent.save(checkpoint_path)
            if verbose:
                print(f"  Saved checkpoint to {checkpoint_path}")
        
        # Check if solved
        if len(episode_rewards) >= 100:
            avg_100 = np.mean(episode_rewards[-100:])
            if avg_100 >= 300:  # BipedalWalker considered solved at 300
                if verbose:
                    print(f"\n🎉 SOLVED! Average reward: {avg_100:.1f}")
                break
    
    # Final save
    agent.save(checkpoint_path)
    env.close()
    
    if verbose:
        print("\n" + "=" * 60)
        print("Training Complete!")
        print(f"  Total steps: {agent.total_steps:,}")
        print(f"  Total episodes: {len(episode_rewards)}")
        avg_final = np.mean(episode_rewards[-100:]) if episode_rewards else 0
        print(f"  Final avg reward (last 100): {avg_final:.1f}")
        print("=" * 60)
    
    return agent


def main():
    parser = argparse.ArgumentParser(description="Train PPO on BipedalWalker")
    parser.add_argument("--max_steps", type=int, default=2_000_000,
                        help="Maximum training steps")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed")
    parser.add_argument("--checkpoint", type=str, default="checkpoints/agent.pt",
                        help="Checkpoint save path")
    parser.add_argument("--easy", action="store_true",
                        help="Use easier BipedalWalker-v3 instead of Hardcore")
    
    args = parser.parse_args()
    
    config = PPOConfig(max_steps=args.max_steps)
    env_name = "BipedalWalker-v3" if args.easy else "BipedalWalkerHardcore-v3"
    
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    
    train(
        env_name=env_name,
        config=config,
        checkpoint_path=args.checkpoint,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
