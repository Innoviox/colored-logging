# colored-logging
Colored logging for Nephos, with Google Code In

Sample usage (in main.py):

```python
import logger

logger.info("Hello, welcome to Simon's logger!")
logger.debug("You can write to a default file, which is stamped with when the module was imported.")
logger.set_file("new_file.txt")
logger.debug("Or you can write to a file of your choosing!")
logger.config(user='root')
logger.info("You can set attributes using the .config method")
```
