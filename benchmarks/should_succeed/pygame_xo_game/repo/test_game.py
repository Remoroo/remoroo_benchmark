"""Test script to verify the game win detection works correctly."""

import sys

def test_win_detection():
    """Test that win detection works for all win conditions."""
    import game
    
    test_cases = [
        {
            "name": "Horizontal win - top row",
            "board_state": [['X', 'X', 'X'], [None, None, None], [None, None, None]],
            "expected_winner": 'X'
        },
        {
            "name": "Vertical win - left column",
            "board_state": [['O', None, None], ['O', None, None], ['O', None, None]],
            "expected_winner": 'O'
        },
        {
            "name": "Diagonal win - top-left to bottom-right",
            "board_state": [['X', None, None], [None, 'X', None], [None, None, 'X']],
            "expected_winner": 'X'
        },
        {
            "name": "Diagonal win - top-right to bottom-left",
            "board_state": [[None, None, 'O'], [None, 'O', None], ['O', None, None]],
            "expected_winner": 'O'
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        game.game_over = False
        game.winner = None
        
        for i in range(3):
            for j in range(3):
                game.board[i][j] = test_case["board_state"][i][j]
        
        game.check_winner()
        
        if game.winner != test_case["expected_winner"]:
            print(f"FAIL: {test_case['name']} - Expected {test_case['expected_winner']}, got {game.winner}")
            all_passed = False
        elif not game.game_over:
            print(f"FAIL: {test_case['name']} - game_over should be True")
            all_passed = False
    
    if all_passed:
        print("game_works: true")
        return True
    else:
        print("game_works: false")
        return False

if __name__ == "__main__":
    result = test_win_detection()
    sys.exit(0 if result else 1)

