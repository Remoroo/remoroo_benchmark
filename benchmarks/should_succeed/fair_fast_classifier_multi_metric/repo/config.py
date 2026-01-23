SEED = 1337

# Intentionally poor defaults (benchmark starts broken):
# - Too many epochs
# - Too large learning rate (unstable)
EPOCHS = 2000
LEARNING_RATE = 5.0
L2_REG = 1e-4

# Data
N_SAMPLES = 4000
N_FEATURES = 12
TRAIN_FRACTION = 0.8

# Fairness: group labels are 0/1
FAIRNESS_WEIGHT = 0.0  # currently disabled (benchmark expects it to be addressed)


