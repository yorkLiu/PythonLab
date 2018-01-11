import time
import progressbar

# bar = progressbar.ProgressBar(redirect_stdout=True)
# for i in range(100):
#     print 'Some text', i
#     time.sleep(0.1)
#     bar.update(i)

# bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
# for i in range(20):
#     time.sleep(0.1)
#     bar.update(i)

# bar = progressbar.ProgressBar(widgets=[
#     ' [', progressbar.Timer(), '] ',
#     progressbar.Bar(),
#     ' (', progressbar.ETA(), ') ',
# ])
# for i in bar(range(20)):
#     time.sleep(0.1)

import sys
import time
import threading
import progressbar


class progress_bar_loading(threading.Thread):
    def run(self):
        global stop
        global kill
        print 'Loading....  ',
        bar = None
        i = 0
        while stop != True:
            if not bar:
                # bar = progressbar.ProgressBar(widgets=[
                #         ' [', progressbar.Timer(), '] ',
                #         progressbar.Bar(fill='#'),
                #         ' (', progressbar.ETA(), ') ',
                #     ])

                bar = progressbar.ProgressBar(maxval=progressbar.UnknownLength)
            i+=1
            time.sleep(0.2)
            bar.update(i)

        if kill == True:
            print '\b\b\b\b ABORT!'
        else:
            print '\b\b done!'


kill = False
stop = False
p = progress_bar_loading()
p.start()

try:
    # anything you want to run.
    time.sleep(10)
    stop = True
except KeyboardInterrupt or EOFError:
    kill = True
    stop = True

