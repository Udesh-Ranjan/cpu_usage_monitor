from __future__ import print_function
from time import sleep
import os
from threading import Thread


class Core(Thread):
    def __init__(self, _id = '', call=None, delay=1):
        super().__init__()
        self.id = _id
        self.last_idle = self.last_total = 0
        self.utilisation = 0
        self.call=call
        self.delay = delay
        self.running = True

    def run(self):
        while self.running:
            with open('/proc/stat') as f:
                line = None
                for l in f.readlines():
                    if f"cpu{self.id}" in l:
                        line = l
                        break
                if line:
                    fields = [float(column) for column in line.strip().split()[1:]]
                    idle, total = fields[3], sum(fields)
                    idle_delta, total_delta = idle - self.last_idle, total - self.last_total
                    self.last_idle, self.last_total = idle, total
                    self.utilisation = 100.0 * (1.0 - idle_delta / total_delta)
                    print(f'{self.id}: %5.1f%%' % self.utilisation, end='\n')
                    if self.call:
                        self.call(self.utilisation, f"cpu {self.id}: {self.utilisation:.2f}%")
                sleep(self.delay)

if __name__ == "__main__":
    cores = [ Core(_id = count) for count in range(os.cpu_count())]
    for core in cores:
        core.start()

    for core in cores:
        core.join()
