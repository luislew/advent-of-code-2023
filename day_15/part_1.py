from day_15 import get_steps, hash_str


if __name__ == "__main__":
    print(sum(hash_str(step) for step in get_steps()))
