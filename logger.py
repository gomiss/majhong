from multiprocessing.managers import BaseManager
import config
import time


if __name__ == "__main__":
    BaseManager.register('SendLog')
    manager = BaseManager(address=(config.server, config.server_port - 1), authkey='dqn')
    manager.connect()
    log_server = manager.SendLog()

    nowStamp = int(time.time())
    timeTuple = time.localtime(nowStamp)
    otherTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeTuple)
    file_name = otherTime + ".txt"
    with open(file_name, "w") as output_file:
        while True:
            log = log_server.get()
            print(log)
            output_file.write("\t".join([str(x) for x in log]))
            output_file.write("\n")
            output_file.flush()


