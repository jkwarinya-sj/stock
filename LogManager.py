import logging

level = logging.INFO

class LogManager:
    _initialized = False

    @classmethod
    def get_logger(cls, lvl):

        """
        if not _initialized:
            cls._setup()
            cls._initialized = True
        """

        #logging.setLevel(level)

        #console = logging.StreamHandler()
        #logging.addHandler(console)


        if not cls._initialized:
            log = logging.getLogger()
            log.setLevel(level)

            # 콘솔 출력 핸들러 추가
            console = logging.StreamHandler()
            log.addHandler(console)

            cls._initialized = True




        return logging.getLogger()

