import time
#prog_time = lambda: time.time()
class Timer:
    def __init__(self):
        self._passed = time.time()
        print(time.time())
        
    def time_passed(self):
        return time.time() - self._passed

    def loop(self, time_to_pass):
        if self.time_passed() >= time_to_pass:
            self._passed += time_to_pass
            return True
        return False
    
    def is_passed(self, time_to_pass):
        return self.time_passed() >=  time_to_pass
    
    def reset(self):
        self._passed = time.time()
    
    def get_time(self):
        return self._passed
    
    def set_time(self, new_time_in_seconds):
        self._passed = new_time_in_seconds

if __name__ == "__main__":
    test = Timer()