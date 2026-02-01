import os
from lib.data import get_numbers
from lib.beta_calc import mean_numbers

def main() -> None:
    nums = get_numbers()
    _beta_mean = mean_numbers(nums)
    print("beta complete")

if __name__ == "__main__":
    main()