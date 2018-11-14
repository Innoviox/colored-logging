import logger

logger.info("Hello, welcome to Simon's logger!")
logger.debug("You can write to a default file, which is stamped with when the module was imported.")
logger.set_file("new_file.txt")
logger.debug("Or you can write to a file of your choosing!")
