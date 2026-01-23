"""Neural network training with multiple metric requirements.

BUGS TO FIX:
1. Model architecture is too simple - won't reach 85% accuracy
2. Learning rate is way too high - causes divergence (high loss)
3. Training loop is inefficient - takes too long

REQUIREMENTS (all must be met):
- accuracy >= 0.85 on test set
- loss <= 0.5 at end of training
- training_time < 30 seconds

The Judge will check artifacts/metrics.json for all three metrics.
"""

import numpy as np
import time
import json
import os
from typing import Tuple, Dict, Any

# Seed for reproducibility
np.random.seed(42)


def generate_data(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generate synthetic classification data.
    
    Creates a dataset where points in quadrants 1 and 3 are class 0,
    and points in quadrants 2 and 4 are class 1.
    """
    X = np.random.randn(n_samples, 2) * 2
    # XOR-like pattern: class depends on sign of x1 * x2
    y = ((X[:, 0] * X[:, 1]) > 0).astype(int)
    
    # Split 80/20
    split = int(0.8 * n_samples)
    return X[:split], y[:split], X[split:], y[split:]


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Sigmoid activation."""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


def relu(x: np.ndarray) -> np.ndarray:
    """ReLU activation."""
    return np.maximum(0, x)


def relu_derivative(x: np.ndarray) -> np.ndarray:
    """ReLU derivative."""
    return (x > 0).astype(float)


class NeuralNetwork:
    """Simple neural network for binary classification.
    
    BUG: Architecture is too shallow for XOR-like problem.
    The network needs at least one hidden layer to learn non-linear boundaries.
    """
    
    def __init__(self, input_size: int = 2, hidden_size: int = 4, output_size: int = 1):
        # BUG: Only using input -> output (no hidden layer effectively used)
        # This linear model can't learn XOR pattern
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01  # BUG: Weights too small
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
    
    def forward(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Forward pass."""
        # BUG: Using sigmoid for hidden layer (relu would be better)
        self.z1 = X @ self.W1 + self.b1
        self.a1 = sigmoid(self.z1)  # BUG: Should use ReLU
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = sigmoid(self.z2)
        return self.a2
    
    def backward(self, X: np.ndarray, y: np.ndarray, output: np.ndarray, lr: float) -> float:
        """Backward pass with gradient descent."""
        m = X.shape[0]
        
        # Output layer gradients
        dz2 = output - y.reshape(-1, 1)
        dW2 = (self.a1.T @ dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m
        
        # Hidden layer gradients
        da1 = dz2 @ self.W2.T
        dz1 = da1 * self.a1 * (1 - self.a1)  # Sigmoid derivative
        dW1 = (X.T @ dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m
        
        # Update weights
        self.W2 -= lr * dW2
        self.b2 -= lr * db2
        self.W1 -= lr * dW1
        self.b1 -= lr * db1
        
        # Compute loss
        eps = 1e-7
        loss = -np.mean(y * np.log(output + eps) + (1 - y.reshape(-1, 1)) * np.log(1 - output + eps))
        return loss
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        output = self.forward(X)
        return (output > 0.5).astype(int).flatten()


def train(epochs: int = 1000, lr: float = 10.0) -> Dict[str, Any]:
    """Train the neural network.
    
    BUGS:
    1. lr=10.0 is WAY too high - causes divergence
    2. epochs=1000 with inefficient loop is too slow
    3. No early stopping
    """
    print("Generating data...")
    X_train, y_train, X_test, y_test = generate_data(n_samples=2000)
    
    print("Initializing model...")
    model = NeuralNetwork(input_size=2, hidden_size=4)  # BUG: hidden_size too small
    
    print(f"Training for {epochs} epochs with lr={lr}...")
    start_time = time.time()
    
    losses = []
    for epoch in range(epochs):
        # BUG: Processing one sample at a time is SLOW
        # Should use batch processing
        for i in range(len(X_train)):
            x = X_train[i:i+1]
            y = y_train[i:i+1]
            output = model.forward(x)
            loss = model.backward(x, y, output, lr)
        
        # Compute epoch loss
        output = model.forward(X_train)
        eps = 1e-7
        epoch_loss = -np.mean(
            y_train * np.log(output.flatten() + eps) + 
            (1 - y_train) * np.log(1 - output.flatten() + eps)
        )
        losses.append(epoch_loss)
        
        if epoch % 100 == 0:
            print(f"  Epoch {epoch}: loss = {epoch_loss:.4f}")
        
        # BUG: No early stopping - wastes time even after convergence
    
    training_time = time.time() - start_time
    
    # Evaluate
    predictions = model.predict(X_test)
    accuracy = np.mean(predictions == y_test)
    final_loss = losses[-1] if losses else float('inf')
    
    print(f"\nResults:")
    print(f"  accuracy: {accuracy:.4f}")
    print(f"  loss: {final_loss:.4f}")
    print(f"  training_time: {training_time:.2f}")
    
    # Save metrics to artifacts
    os.makedirs("artifacts", exist_ok=True)
    metrics = {
        "accuracy": float(accuracy),
        "loss": float(final_loss),
        "training_time": float(training_time)
    }
    
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\nMetrics saved to artifacts/metrics.json")
    
    # Check requirements
    success = accuracy >= 0.85 and final_loss <= 0.5 and training_time < 30
    if success:
        print("\n✅ All requirements met!")
    else:
        print("\n❌ Requirements NOT met:")
        if accuracy < 0.85:
            print(f"   - accuracy {accuracy:.4f} < 0.85")
        if final_loss > 0.5:
            print(f"   - loss {final_loss:.4f} > 0.5")
        if training_time >= 30:
            print(f"   - training_time {training_time:.2f}s >= 30s")
    
    return metrics


if __name__ == "__main__":
    train()

