"""Order processing state machine with multiple bugs.

This implements a Finite State Machine (FSM) for order processing:

States:
    PENDING -> PROCESSING -> SHIPPED -> DELIVERED
                   |
                   v
              CANCELLED

Valid transitions:
    PENDING -> PROCESSING (requires payment_received=True)
    PENDING -> CANCELLED
    PROCESSING -> SHIPPED
    PROCESSING -> CANCELLED
    SHIPPED -> DELIVERED
    
Invalid transitions (should be rejected):
    CANCELLED -> any state (cancelled orders are final)
    DELIVERED -> any state (delivered orders are final)
    PENDING -> SHIPPED (can't skip PROCESSING)
    SHIPPED -> CANCELLED (too late to cancel)

BUGS TO FIX:
1. Allows transition from CANCELLED state (should be terminal)
2. No guard checking payment_received for PENDING->PROCESSING
3. Allows SHIPPED->CANCELLED (invalid, too late)
4. Doesn't track transition history properly
"""

from enum import Enum, auto
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field


class OrderState(Enum):
    PENDING = auto()
    PROCESSING = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


@dataclass
class Order:
    order_id: str
    payment_received: bool = False
    items: List[str] = field(default_factory=list)


class InvalidTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


class OrderStateMachine:
    """State machine for order processing.
    
    BUGS:
    1. Allows transitions from CANCELLED state
    2. No payment check for PENDING -> PROCESSING
    3. Allows SHIPPED -> CANCELLED (should be rejected)
    4. Duplicate transitions not prevented
    """
    
    def __init__(self, order: Order):
        self.order = order
        self.state = OrderState.PENDING
        self.history: List[Dict[str, Any]] = []
    
    def transition(self, new_state: OrderState) -> bool:
        """Attempt to transition to a new state.
        
        Returns True if transition succeeded, raises InvalidTransitionError if not.
        
        BUGS:
        1. Doesn't check if current state is terminal (CANCELLED/DELIVERED)
        2. Doesn't validate payment for PENDING->PROCESSING
        3. Allows invalid SHIPPED->CANCELLED
        """
        old_state = self.state
        
        # BUG 1: Should check if current state is terminal!
        # CANCELLED and DELIVERED are terminal states
        
        # Define valid transitions (but implementation is buggy!)
        valid_transitions = {
            OrderState.PENDING: [OrderState.PROCESSING, OrderState.CANCELLED],
            OrderState.PROCESSING: [OrderState.SHIPPED, OrderState.CANCELLED],
            OrderState.SHIPPED: [OrderState.DELIVERED, OrderState.CANCELLED],  # BUG 3: CANCELLED shouldn't be here!
            OrderState.DELIVERED: [],  # Terminal
            OrderState.CANCELLED: [OrderState.SHIPPED],  # BUG 1: Should be empty (terminal)!
        }
        
        # Check if transition is in valid list
        if new_state not in valid_transitions.get(self.state, []):
            raise InvalidTransitionError(
                f"Cannot transition from {self.state.name} to {new_state.name}"
            )
        
        # BUG 2: Should check payment_received for PENDING -> PROCESSING!
        # Missing guard condition check here
        
        # BUG 4: Should check if we're already in this state
        # (prevent no-op transitions that pollute history)
        
        # Perform transition
        self.state = new_state
        self.history.append({
            "from": old_state.name,
            "to": new_state.name,
        })
        
        return True
    
    def process(self) -> bool:
        """Move order to PROCESSING state."""
        return self.transition(OrderState.PROCESSING)
    
    def ship(self) -> bool:
        """Move order to SHIPPED state."""
        return self.transition(OrderState.SHIPPED)
    
    def deliver(self) -> bool:
        """Move order to DELIVERED state."""
        return self.transition(OrderState.DELIVERED)
    
    def cancel(self) -> bool:
        """Move order to CANCELLED state."""
        return self.transition(OrderState.CANCELLED)
    
    def get_state(self) -> OrderState:
        """Get current state."""
        return self.state
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get transition history."""
        return self.history.copy()


def run_tests():
    """Run all state machine tests."""
    results = []
    
    # Test 1: Normal flow - pending -> processing -> shipped -> delivered
    print("Test 1: Normal order flow")
    order = Order("order-1", payment_received=True)
    fsm = OrderStateMachine(order)
    try:
        fsm.process()
        fsm.ship()
        fsm.deliver()
        success = fsm.get_state() == OrderState.DELIVERED
        print(f"  Final state: {fsm.get_state().name}, expected: DELIVERED")
        results.append(("normal_flow", success))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("normal_flow", False))
    
    # Test 2: Cancel from pending
    print("\nTest 2: Cancel from PENDING")
    order = Order("order-2")
    fsm = OrderStateMachine(order)
    try:
        fsm.cancel()
        success = fsm.get_state() == OrderState.CANCELLED
        print(f"  Final state: {fsm.get_state().name}, expected: CANCELLED")
        results.append(("cancel_pending", success))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("cancel_pending", False))
    
    # Test 3: Cancel from processing
    print("\nTest 3: Cancel from PROCESSING")
    order = Order("order-3", payment_received=True)
    fsm = OrderStateMachine(order)
    try:
        fsm.process()
        fsm.cancel()
        success = fsm.get_state() == OrderState.CANCELLED
        print(f"  Final state: {fsm.get_state().name}, expected: CANCELLED")
        results.append(("cancel_processing", success))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("cancel_processing", False))
    
    # Test 4: Cannot cancel from shipped (BUG TEST)
    print("\nTest 4: Cannot cancel from SHIPPED (should fail)")
    order = Order("order-4", payment_received=True)
    fsm = OrderStateMachine(order)
    try:
        fsm.process()
        fsm.ship()
        fsm.cancel()  # This SHOULD raise an error!
        print(f"  BUG: Allowed cancel from SHIPPED!")
        results.append(("no_cancel_shipped", False))
    except InvalidTransitionError:
        print(f"  Correctly rejected cancel from SHIPPED")
        results.append(("no_cancel_shipped", True))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("no_cancel_shipped", False))
    
    # Test 5: Cannot transition from cancelled (BUG TEST)
    print("\nTest 5: Cannot transition from CANCELLED (should fail)")
    order = Order("order-5")
    fsm = OrderStateMachine(order)
    try:
        fsm.cancel()
        fsm.ship()  # This SHOULD raise an error!
        print(f"  BUG: Allowed transition from CANCELLED!")
        results.append(("cancelled_terminal", False))
    except InvalidTransitionError:
        print(f"  Correctly rejected transition from CANCELLED")
        results.append(("cancelled_terminal", True))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("cancelled_terminal", False))
    
    # Test 6: Cannot transition from delivered
    print("\nTest 6: Cannot transition from DELIVERED (should fail)")
    order = Order("order-6", payment_received=True)
    fsm = OrderStateMachine(order)
    try:
        fsm.process()
        fsm.ship()
        fsm.deliver()
        fsm.cancel()  # This SHOULD raise an error!
        print(f"  BUG: Allowed transition from DELIVERED!")
        results.append(("delivered_terminal", False))
    except InvalidTransitionError:
        print(f"  Correctly rejected transition from DELIVERED")
        results.append(("delivered_terminal", True))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("delivered_terminal", False))
    
    # Test 7: Cannot skip states (pending -> shipped)
    print("\nTest 7: Cannot skip PROCESSING (PENDING -> SHIPPED should fail)")
    order = Order("order-7", payment_received=True)
    fsm = OrderStateMachine(order)
    try:
        fsm.ship()  # This SHOULD raise an error!
        print(f"  BUG: Allowed skipping PROCESSING!")
        results.append(("no_skip_states", False))
    except InvalidTransitionError:
        print(f"  Correctly rejected skipping PROCESSING")
        results.append(("no_skip_states", True))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("no_skip_states", False))
    
    # Test 8: Payment required for processing (BUG TEST)
    print("\nTest 8: Payment required for PROCESSING (should fail without payment)")
    order = Order("order-8", payment_received=False)  # No payment!
    fsm = OrderStateMachine(order)
    try:
        fsm.process()  # This SHOULD raise an error - no payment!
        print(f"  BUG: Allowed processing without payment!")
        results.append(("payment_required", False))
    except InvalidTransitionError:
        print(f"  Correctly rejected processing without payment")
        results.append(("payment_required", True))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("payment_required", False))
    
    # Test 9: Payment allows processing
    print("\nTest 9: Payment allows PROCESSING")
    order = Order("order-9", payment_received=True)
    fsm = OrderStateMachine(order)
    try:
        fsm.process()
        success = fsm.get_state() == OrderState.PROCESSING
        print(f"  Final state: {fsm.get_state().name}, expected: PROCESSING")
        results.append(("payment_allows", success))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("payment_allows", False))
    
    # Test 10: History is tracked correctly
    print("\nTest 10: Transition history tracked")
    order = Order("order-10", payment_received=True)
    fsm = OrderStateMachine(order)
    try:
        fsm.process()
        fsm.ship()
        history = fsm.get_history()
        expected_len = 2
        success = len(history) == expected_len
        print(f"  History length: {len(history)}, expected: {expected_len}")
        results.append(("history_tracked", success))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("history_tracked", False))
    
    return results


def main():
    """Run tests and report results."""
    print("=" * 60)
    print("ORDER STATE MACHINE TESTS")
    print("=" * 60)
    print()
    
    results = run_tests()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {name}")
    
    all_tests_pass = (passed == len(results))
    
    print(f"\nPassed: {passed}/{len(results)}")
    print(f"all_tests_pass: {all_tests_pass}")
    
    if all_tests_pass:
        print("\nSUCCESS: All state machine bugs fixed!")
    else:
        print(f"\nFAILED: {len(results) - passed} test(s) failed")


if __name__ == "__main__":
    main()

