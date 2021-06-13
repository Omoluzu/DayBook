
import os
import datetime
from pathlib import Path


MAIN = {
    "OTHER": {
        "path_save_daybook": os.path.abspath(os.curdir),
        "days_of": str(datetime.datetime.now().date()),
    },
    "TEXT": {
        "size": 12
    },
    "Databases": {
        "path": os.path.join(Path.home(), r"DayBook\DayBook.db")
    }
}
