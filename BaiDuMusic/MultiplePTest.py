# -*- coding: UTF-8 -*-
from collections import deque
from multiprocessing import Pool
import multiprocessing
import contextlib

queue=deque()

# def proxy(cls_instance, i):
#     return cls_instance.download(i)

import copy_reg
import types
def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)

class MyTest(object):


    def __del__(self):
        print "... Destructor %s" % multiprocessing.current_process().name


    def download(self, songId):
        print songId



    def run(self):
        queue.extendleft([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        with contextlib.closing(Pool(processes=4)) as pool:
            pool.map(self.download, [1,2,3,4,5,6,7])
        # pool = multiprocessing.Pool(processes=3)
        # pool.map(self.download, [1,2,3,4,5,6,7,8])
        # for num in range(8):
        #     # pool.apply_async(self.func, args=(num,))
        #     pool.apply_async(self, args=(self, num,))
        # pool.close()
        # pool.join()


if __name__=="__main__":
    MyTest().run()

