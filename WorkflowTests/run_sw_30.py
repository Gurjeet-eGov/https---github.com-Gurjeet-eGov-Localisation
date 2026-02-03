import time
from SW import NewSW

# Number of connections to create
COUNT = 30

# Delay between iterations (seconds)
DELAY = 2

if __name__ == '__main__':
    for i in range(1, COUNT + 1):
        print(f"=== Run {i}/{COUNT} : Starting SW workflow ===")
        try:
            NewSW()
            print(f"=== Run {i}/{COUNT} : Completed ===\n")
        except Exception as e:
            print(f"=== Run {i}/{COUNT} : Failed with error: {e} ===\n")
        time.sleep(DELAY)
