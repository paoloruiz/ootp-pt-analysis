import sys

class ProgressBar:
    def __init__(self, size, name):
        self.size = size
        self.name = name
        self.previous_num = -1
        self.bar_size = 100
        self.max_line_length = 0
        self.index = 0

        sys.stdout.write(f"[{'=' * int(0):{self.bar_size}s}] {int(0)}%  {self.name}")
        sys.stdout.flush()

    
    def increment(self, update_name=None):
        self.index += 1
        self.index = min(self.size, self.index)
        new_progress = self.index / self.size
        if self.index == self.size:
            sys.stdout.write('\r')
            line = f"[{'=' * self.bar_size:{self.bar_size}s}] 100%  {self.name}"
            extra_length = max(0, self.max_line_length - len(line))
            sys.stdout.write(line + " " * extra_length)
            sys.stdout.flush()
        elif int(new_progress * self.bar_size) > int(self.previous_num * self.bar_size):
            self.previous_num = new_progress
            sys.stdout.write('\r')
            line = f"[{'=' * int(new_progress * self.bar_size):{self.bar_size}s}] {int(new_progress * 100)}%  {update_name if update_name != None else self.name}"
            extra_length = max(0, self.max_line_length - len(line))
            self.max_line_length = max(len(line), self.max_line_length)
            sys.stdout.write(line + " " * extra_length)
            sys.stdout.flush()

    # Do nothing but update the current line name
    def update(self, update_name=None):
        self.index -= 1
        self.increment(update_name)

    def finish(self, extra_str=""):
        if self.index < self.size:
            self.index = self.size - 1
            self.increment(self.name)
        print(extra_str)