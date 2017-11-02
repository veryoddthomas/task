import subprocess as proc


def run_command(command, input_text=None, env=None, cwd='.', host=None):
    # print(" ".join(command))
    p = proc.Popen(command, stdin=proc.PIPE, stdout=proc.PIPE, stderr=proc.PIPE, cwd=cwd, env=env)
    output, errors = p.communicate(input_text)
    return p.returncode, output, errors


def run_long_command(command, input_text=None, env=None, cwd='.', host=None):
    assert(input_text is None)  # don't handle this for now.
    print(" ".join(command))

    p = proc.Popen(command, stdin=proc.PIPE, stdout=proc.PIPE, stderr=proc.STDOUT, cwd=cwd, env=env)

    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        print line,
        if line == '' and p.poll() != None:
            break
    output = ''.join(stdout)

    return p.returncode, output, None
