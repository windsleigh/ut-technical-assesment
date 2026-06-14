import subprocess


def getHeader():
    procHeader = []
    cmd = "ps -e --no-headers | wc -l"
    processCount = subprocess.run(cmd, shell=True,
                                  encoding='utf-8',
                                  stdout=subprocess.PIPE)
    cmd2 = "cat /proc/stat |grep cpu |tail -1|awk '{print ($5*100)/($2+$3+$4+$5+$6+$7+$8+$9+$10)}'|awk '{print 100-$1}'"
    cpuPercent = subprocess.run(cmd2, shell=True,
                                encoding='utf-8',
                                stdout=subprocess.PIPE)
    cmd3 = "free | grep Mem | awk '{print $3/$2 * 100.0}'"
    memPercent = subprocess.run(cmd3, shell=True,
                                encoding='utf-8',
                                stdout=subprocess.PIPE)
    procCount = int(processCount.stdout) - 2
    procHeader = [
        {"CPU": float(cpuPercent.stdout),
         "MEM": float(memPercent.stdout),
         "PROC": procCount}
    ]
    return procHeader