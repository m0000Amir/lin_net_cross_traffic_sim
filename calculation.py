from decouple import config
import time
import json

from cross_traffic import run

conf = config("TASK_PARAMS")


def f(data):
    return json.loads(run(data))


with open("/file.txt", "w") as writer:
    writer.write(f(json.dumps(conf)))

