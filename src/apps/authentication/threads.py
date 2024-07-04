import threading

import shared.utils.auth as utils


class SendEmailThread(threading.Thread):
    def __init__(self, token):
        threading.Thread.__init__(self)
        self.token = token

    def run(self):
        utils.send_email(self.token)
