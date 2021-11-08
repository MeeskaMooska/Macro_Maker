import logging
import time
import threading


def thread_function(id):
    logging.info("Thread %s: starting", id)
    time.sleep(1)
    logging.info("Thread %s: ending", id)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    threads = list()
    for index in range(3):
        logging.info("Main   : before joining thread %d", index)
        x = threading.Thread(target=thread_function(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main   : before joining thread %d", index)
        thread.join()
        logging.info("Main   : thread %d done", index)
