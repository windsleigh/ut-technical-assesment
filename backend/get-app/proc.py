import subprocess


def getProcs():
    totalProcs = []
    proc = subprocess.run(["ps",
                           "-eo",
                           "pid,pcpu,pmem,comm",
                           "--sort",
                           "-pcpu"],
                          encoding='utf-8',
                          stdout=subprocess.PIPE)

    for line in proc.stdout.split('\n')[1:-1]:
        totalProcs.append({"PID": int(line.split()[0]),
                           "CPU": float(line.split()[1]),
                           "MEM": float(line.split()[2]),
                           "PROC": line.split()[3]})
    return totalProcs