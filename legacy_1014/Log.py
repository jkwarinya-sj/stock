import logging

class Log:

    def __init__(self, level):
        self.log = logging.getLogger()
        #logging.basicConfig()

        self.log.setLevel(level)
        
        # 콘솔 출력 핸들러 추가
        console = logging.StreamHandler()
        self.log.addHandler(console)

    def get_logger(self):
        return self.log
