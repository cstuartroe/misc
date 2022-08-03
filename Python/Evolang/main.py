import string
import subprocess
import random
from queue import Queue

INCLUDED_CHARACTERS = string.ascii_letters + string.digits + '\n !"$%&\'()*+,-.:;<=>?@[\\]_{|}'
INCLUDED_CHARACTERS += '/'
# INCLUDED_CHARACTERS += '#'


def run_python(content: str):
    with open(".tmp.py", 'w') as fh:
        fh.write(content)

    process = subprocess.Popen(
        ['python', '.tmp.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr


def random_member(l):
    return l[random.randrange(len(l))]


def add_to(s: str):
    position = random.randrange(len(s) + 1)

    return s[:position] + random_member(INCLUDED_CHARACTERS) + s[position:]


if __name__ == "__main__":
    valid_programs = Queue()
    valid_programs.put('')

    while True:
        program = valid_programs.get()

        code, stdout, stderr = run_python(program)

        if code == 0:
            valid_programs.put(program)
            valid_programs.put(add_to(program))

            if len(program) > 3:
                print(repr(program))

