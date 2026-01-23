"""Resource manager with deadlock bug.

This simulates a banking system where transfers between accounts
can deadlock due to inconsistent lock ordering.

The classic deadlock scenario:
- Thread 1: locks Account A, then tries to lock Account B
- Thread 2: locks Account B, then tries to lock Account A
- Both threads wait forever = DEADLOCK

The fix requires consistent lock ordering (e.g., always lock lower ID first).
"""

import threading
import time
import random

class Account:
    """Bank account with a lock for thread-safe operations."""
    
    def __init__(self, account_id: int, balance: float = 1000.0):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()
    
    def __repr__(self):
        return f"Account({self.account_id}, balance={self.balance:.2f})"


class ResourceManager:
    """Manages transfers between accounts.
    
    BUG: Deadlock due to inconsistent lock ordering!
    
    When transferring from A to B:
    - This code locks A first, then B
    - But another thread transferring B to A locks B first, then A
    - This causes deadlock!
    
    FIX: Always acquire locks in a consistent order (e.g., by account_id)
    """
    
    def __init__(self):
        self.accounts = {}
        self.transfer_count = 0
        self.count_lock = threading.Lock()
    
    def create_account(self, account_id: int, initial_balance: float = 1000.0) -> Account:
        account = Account(account_id, initial_balance)
        self.accounts[account_id] = account
        return account
    
    def transfer(self, from_id: int, to_id: int, amount: float) -> bool:
        """Transfer amount from one account to another.
        
        BUG: Acquires locks in order of parameters, not by account_id!
        This causes deadlock when two threads transfer in opposite directions.
        """
        if from_id == to_id:
            return False
        
        from_account = self.accounts.get(from_id)
        to_account = self.accounts.get(to_id)
        
        if not from_account or not to_account:
            return False
        
        # BUG: Lock ordering based on parameter order causes deadlock!
        # Thread 1: transfer(A, B) -> locks A, then B
        # Thread 2: transfer(B, A) -> locks B, then A
        # DEADLOCK!
        
        with from_account.lock:  # BUG: Should use consistent ordering!
            # Small delay to increase chance of deadlock
            time.sleep(0.001)
            
            with to_account.lock:  # BUG: This is where deadlock occurs
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    
                    with self.count_lock:
                        self.transfer_count += 1
                    
                    return True
        
        return False
    
    def get_transfer_count(self) -> int:
        with self.count_lock:
            return self.transfer_count


def worker(manager: ResourceManager, num_transfers: int, account_ids: list):
    """Worker that performs random transfers."""
    for _ in range(num_transfers):
        from_id = random.choice(account_ids)
        to_id = random.choice(account_ids)
        if from_id != to_id:
            manager.transfer(from_id, to_id, random.uniform(1, 10))


def main():
    """Test the resource manager with concurrent transfers."""
    random.seed(42)
    
    manager = ResourceManager()
    
    # Create accounts
    num_accounts = 5
    for i in range(num_accounts):
        manager.create_account(i, 10000.0)
    
    account_ids = list(range(num_accounts))
    
    # Spawn workers
    num_workers = 10
    transfers_per_worker = 100
    expected_transfers = num_workers * transfers_per_worker
    
    print(f"Starting {num_workers} workers, each doing {transfers_per_worker} transfers")
    print(f"Expected total transfers: {expected_transfers}")
    print("(If this hangs, there's a deadlock!)\n")
    
    threads = []
    start_time = time.time()
    
    for i in range(num_workers):
        t = threading.Thread(target=worker, args=(manager, transfers_per_worker, account_ids))
        threads.append(t)
        t.start()
    
    # Wait with timeout
    timeout = 30  # seconds
    for t in threads:
        t.join(timeout=timeout)
        if t.is_alive():
            print("DEADLOCK DETECTED! Thread did not complete.")
            print(f"completed_transfers: {manager.get_transfer_count()}")
            return
    
    elapsed = time.time() - start_time
    completed = manager.get_transfer_count()
    
    print(f"Completed in {elapsed:.2f} seconds")
    print(f"completed_transfers: {completed}")
    
    # Note: Not all transfers succeed (insufficient balance), but should be close
    if completed >= expected_transfers * 0.8:  # At least 80% should complete
        print(f"\nSUCCESS: {completed} transfers completed without deadlock!")
    else:
        print(f"\nFAILED: Only {completed}/{expected_transfers} transfers completed")


if __name__ == "__main__":
    main()

