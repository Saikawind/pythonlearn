# 参考：https://itqna.net/questions/37569/what-print-flush-python-closed
import time

for _ in range(5):
    print('.', end='')
    time.sleep(0.5)
print('  Gairuo!')

# 在终端中最后一次性显示
# ..... Gairuo!