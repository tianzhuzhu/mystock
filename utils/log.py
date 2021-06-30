import os, logging, logging.config, settings


class MyLogger(logging.Logger):
    """重写Logger的某些函数，给这些等级的日志输出不同颜色"""

    def info(self, msg, *args, **kwargs):
        """重写info函数"""

        if self.isEnabledFor(20):
            self._log(20, "\033[36;1m%s\033[0m" % msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """重写error函数"""

        if self.isEnabledFor(40):
            self._log(40, "\033[31;1m%s\033[0m" % msg, args, **kwargs)

logging.setLoggerClass(MyLogger)
logging.config.fileConfig(os.path.join(settings.PROJECT_ROOT, "logger.conf"))
log = logging.getLogger("infile")
log.info("============== log initialized ==============")
