import random
import time
import sys
import argparse

print(sys.argv)

start_time = time.time()
run_time = int(sys.argv[1])
itime = start_time


while True:
  itime = time.time()
  idata = random.random()
  print(itime, idata)
  time.sleep(1)
