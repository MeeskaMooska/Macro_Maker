import multiprocessing
import time


def square_number(numbers):
    for n in numbers:
        time.sleep(1)
        print("Squared: ", n*n, ";")


def cube_number(numbers):
    for n in numbers:
        time.sleep(1)
        print("Cubed: ", n*n*n, ";")


if __name__ == "__main__":
    arr = [2, 3, 8, 9]
    p1 = multiprocessing.Process(target=square_number, args=(arr,))
    p2 = multiprocessing.Process(target=cube_number, args=(arr,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
