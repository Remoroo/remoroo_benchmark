# BipedalWalker Hardcore RL Benchmark

Train a reinforcement learning agent to walk across randomly generated hardcore terrain.

## Task

Use the `gymnasium` library's `BipedalWalkerHardcore-v3` environment to train an RL agent.

**Success criteria**: Average reward >= 200 over 100 evaluation episodes.

## Environment Details

- **State**: 24-dimensional (hull angle, velocities, joint angles, leg contact, lidar readings)
- **Action**: 4 continuous values (hip/knee torques for each leg)
- **Terrain**: Randomly generated stumps, stairs, and pits
- **Physics**: Box2D (compiled C library - accurate simulation)

## Getting Started

```bash
pip install -r requirements.txt
python train.py
python evaluate.py
```

## Files

- `train.py` - Training script (implement your RL agent here)
- `evaluate.py` - Evaluation script (runs 100 episodes, outputs avg_reward)
- `requirements.txt` - Dependencies

## Notes

- The physics engine (Box2D) is a compiled C library - dynamics cannot be modified
- Terrain is randomly generated each episode - cannot be pre-memorized
- This is a continuous control problem - consider PPO, SAC, or TD3 algorithms
