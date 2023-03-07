import numpy as np

class cacfar(object):
    def __init__(self, window_size, guard_size,pfa = 0.01, scale=1.0):
        self.pfa = pfa
        self.scale = scale
        self.window_size = window_size
        self.guard_size = guard_size

    def cal_threshold(self, left, right):       
        n = len(left)+len(right)
        s = np.sum(np.square(left))+np.sum(np.square(right))

        if n > 0:
            T= np.power(self.pfa,(-1.0 /n)) - 1
            average = s/n
            return T*average * self.scale
        
        return 0

    def clip_window(self, window,limit):
        for i in range(len(window)):
            if window[i] < 0:
                window[i] = 0
            if window[i] > limit:
                window[i] = limit
        return window        

    def get_thresholds(self,signal):
        threshold = np.zeros_like(signal)       
        for i in range(len(signal)):
            left_window = self.clip_window([i-self.guard_size-self.window_size,i-self.guard_size],len(signal)-1)
            right_window = self.clip_window([i+self.guard_size,i+self.guard_size+self.window_size],len(signal)-1)
            
            threshold[i] = self.cal_threshold(signal[left_window[0]:left_window[1]],signal[right_window[0]:right_window[1]])

        return threshold
