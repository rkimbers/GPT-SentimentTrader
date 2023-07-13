import time
import traceback
import main

if __name__ == "__main__":
    try:
        main.main()
    except Exception as e:
        print(f"main.py exited with exception: {e}")
        print(traceback.format_exc())  # print the stack trace
    while True:
        time.sleep(1000)  # wait indefinitely
