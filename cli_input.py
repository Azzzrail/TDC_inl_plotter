import sys


def cli_input(mode, message=""):
    if mode == 0:
        message = message + " Press <Enter> to continue or q to quit:"
        print(message)
        answer = sys.stdin.readline()
        if answer.lower() == "q":
            sys.exit(2)
        return answer
