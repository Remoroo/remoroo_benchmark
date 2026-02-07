"""Evaluation script for BipedalWalker Hardcore.

Runs 100 episodes and outputs the average reward.
Success threshold: avg_reward >= 200
"""
import argparse
import json
import os
import numpy as np

try:
    import gymnasium as gym
except ImportError:
    raise ImportError("gymnasium is required. Install with: pip install gymnasium[box2d]")


def load_agent(checkpoint_path: str):
    """Load a trained agent from checkpoint.
    
    Returns a callable policy: state -> action
    """
    import torch
    
    if not os.path.exists(checkpoint_path):
        print(f"Warning: No checkpoint found at {checkpoint_path}")
        print("Using random policy for evaluation.")
        return None
    
    # Load the checkpoint
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
    # Reconstruct the policy network
    from train import PolicyNetwork
    
    state_dim = 24
    action_dim = 4
    policy = PolicyNetwork(state_dim, action_dim)
    policy.load_state_dict(checkpoint['policy_state_dict'])
    policy.eval()
    
    def get_action(state):
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            action, _, _ = policy(state_tensor)
            return action.squeeze(0).numpy()
    
    return get_action


def random_policy(state):
    """Random policy for baseline comparison."""
    return np.random.uniform(-1, 1, size=4)


def evaluate(
    env_name: str = "BipedalWalkerHardcore-v3",
    checkpoint_path: str = "checkpoints/agent.pt",
    n_episodes: int = 100,
    render: bool = False,
    seed: int = 42,
) -> dict:
    """Evaluate agent on environment.
    
    Args:
        env_name: Gymnasium environment name
        checkpoint_path: Path to agent checkpoint
        n_episodes: Number of evaluation episodes
        render: Whether to render (slow)
        seed: Random seed
        
    Returns:
        Dictionary with evaluation metrics
    """
    # Create environment
    render_mode = "human" if render else None
    env = gym.make(env_name, render_mode=render_mode)
    
    # Load agent or use random policy
    policy = load_agent(checkpoint_path)
    if policy is None:
        policy = random_policy
        print("Evaluating random policy...")
    else:
        print(f"Loaded agent from {checkpoint_path}")
    
    # Run episodes
    rewards = []
    for ep in range(n_episodes):
        state, _ = env.reset(seed=seed + ep)
        episode_reward = 0.0
        done = False
        truncated = False
        
        while not done and not truncated:
            action = policy(state)
            state, reward, done, truncated, info = env.step(action)
            episode_reward += reward
        
        rewards.append(episode_reward)
        
        if (ep + 1) % 10 == 0:
            print(f"Episode {ep + 1}/{n_episodes}: {episode_reward:.1f} (avg: {np.mean(rewards):.1f})")
    
    env.close()
    
    # Compute metrics
    avg_reward = float(np.mean(rewards))
    std_reward = float(np.std(rewards))
    min_reward = float(np.min(rewards))
    max_reward = float(np.max(rewards))
    success_rate = float(np.mean([r >= 200 for r in rewards]))
    
    metrics = {
        "avg_reward": avg_reward,
        "std_reward": std_reward,
        "min_reward": min_reward,
        "max_reward": max_reward,
        "success_rate": success_rate,
        "n_episodes": n_episodes,
    }
    
    print("\n" + "=" * 50)
    print("EVALUATION RESULTS")
    print("=" * 50)
    print(f"  Average Reward: {avg_reward:.2f}")
    print(f"  Std Reward: {std_reward:.2f}")
    print(f"  Min/Max: {min_reward:.1f} / {max_reward:.1f}")
    print(f"  Success Rate (>=200): {success_rate:.1%}")
    print("=" * 50)
    
    # Output metrics as JSON for parsing
    print("\nMETRICS_JSON:")
    print(json.dumps(metrics, indent=2))
    
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Evaluate BipedalWalker agent")
    parser.add_argument("--checkpoint", type=str, default="checkpoints/agent.pt",
                        help="Path to agent checkpoint")
    parser.add_argument("--episodes", type=int, default=100,
                        help="Number of evaluation episodes")
    parser.add_argument("--render", action="store_true",
                        help="Render evaluation (slow)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed")
    parser.add_argument("--easy", action="store_true",
                        help="Use easier BipedalWalker-v3 instead of Hardcore")
    
    args = parser.parse_args()
    
    env_name = "BipedalWalker-v3" if args.easy else "BipedalWalkerHardcore-v3"
    
    metrics = evaluate(
        env_name=env_name,
        checkpoint_path=args.checkpoint,
        n_episodes=args.episodes,
        render=args.render,
        seed=args.seed,
    )
    
    # Exit with success if avg_reward >= 200
    if metrics["avg_reward"] >= 200:
        print("\n✅ SUCCESS: Agent achieved avg_reward >= 200")
        return 0
    else:
        print(f"\n❌ FAILED: avg_reward = {metrics['avg_reward']:.1f} < 200")
        return 1


if __name__ == "__main__":
    exit(main())
