from lib.data import get_numbers
from lib.alpha_calc import sum_numbers

def main() -> None:
    nums = get_numbers()
    _alpha_sum = sum_numbers(nums)
    print("alpha complete")

if __name__ == "__main__":
    main()