from decouple import config
import time
import json

from cross_traffic import run

conf = config("TASK_PARAMS")


def f(data):
    return json.dumps(run(data))


with open("/file.txt", "w") as writer:
    writer.write(f(json.loads(conf)))

