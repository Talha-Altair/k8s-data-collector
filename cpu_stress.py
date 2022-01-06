import os

def stress():

    time_in_seconds = 200

    cmd = f"stress --cpu 1 --timeout {time_in_seconds}s"

    os.system(cmd)

    return 0

if __name__ == '__main__':

    stress()