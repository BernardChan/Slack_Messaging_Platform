# File for message/sendlater(token, channel_id, message, time_sent)
# Will use a POST request

# Dependencies:
# - message_send()

import threading
import time
import sched
from interface_functions.message import message_send
import helper_functions.interface_function_helpers as help
from error import InputError


# Message queue for sending a message later
q = []
do_work = threading.Event()
is_thread_running_flag = False


# TODO: import the real message_send function
# Dequeues send_later_queue whenever a new item is added to it
def set_sched():
    global q, do_work
    while True:

        # If there are items to dequeue
        if q:

            # get the time_sent, message and priority from send_later_queue
            time_sent, message, priority, token, channel_id = q[0]["time_sent"], q[0]["message"], q[0]["priority"], q[0]["token"], q[0]["channel_id"]
            del(q[0])

            # Create a schedule object to be run at a later date
            s = sched.scheduler(time.time, time.sleep)
            s.enterabs(time_sent, priority, message_send, [token, channel_id, message])
            s.run()
        else:
            do_work = threading.Event()
            do_work.wait()


# TODO: move this to server.py
# Creates a thread for setting a schedule
def start_thread_helper():
    global is_thread_running_flag
    if is_thread_running_flag:
        return

    else:
        is_thread_running_flag = True
        t = threading.Thread(target=set_sched)
        t.start()


# Adds a message to be sent at a later date
def send_later(token, channel_id, message, time_sent):
    help.is_message_valid(token, message, channel_id)
    curr = time.time()
    if time_sent - curr < 0:
        raise InputError("Time given was in the past")

    global do_work
    q.append({"message": message, "time_sent": time_sent, "priority": time.time(), "token": token, "channel_id": channel_id})
    do_work.set()

    # TODO: send a message_id back.
    #   need to create a message_id, then pass it into message_send() and then return message_id
    # TODO: add an optional arg to message_send()
    #   accepts the message_id, and uses that instead of creating one itself


if __name__ == "__main__":
    start_thread_helper()  # Should only be called once
    curr = time.time()

    for i in range(100):
        send_later(0, 0, str(i), curr + 5)

    time.sleep(20)
    send_later(0, 0, "yoyoyo", time.time())
    start_thread_helper()  # Should do nothing
