#!/usr/bin/env python3

from itertools import permutations
from string import ascii_lowercase, digits
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
from sys import stderr, stdout, argv
import random
import argparse

from requests import post, codes

import colors


class Domain:

  @classmethod
  def bruteforce(self, max_username_len=3):
    chars = ascii_lowercase + digits
    for x in range(1, max_username_len + 1):
      for y in permutations(chars, x):
        yield "".join(y)

  @classmethod
  def random(self, limit=100, length=5):
    for _ in range(limit):
      chars = [random.choice(ascii_lowercase + digits) for _ in range(length)]
      yield ''.join(chars)


class SignupChecker:

  URL = 'https://github.com/signup_check/username'
  TEST_URL = 'http://127.0.0.1:8000'

  LOG_ICONS = {
      codes.OK: colors.green('✓'),
      codes.TOO_MANY: colors.fail('⚠'),
      codes.FORBIDDEN: colors.warn('✗')
  }

  def __init__(self, domain='bruteforce', workers=10, url=URL, test=False):
    if test:
      url = self.TEST_URL
    self.outputs = [stderr, stdout]
    self.workers = workers
    self.url = url

    self.next_queue = Queue()
    for x in getattr(Domain, domain)():
      self.next_queue.put(x)

  def run(self):
    while not self.next_queue.empty():
      queue = self.next_queue
      self.next_queue = Queue()
      targets = []
      while not queue.empty():
        targets.append(queue.get())
      executor = ThreadPoolExecutor(self.workers)
      futures = executor.map(self.check, targets)
      for future in futures:
        self.log(*future)

  def check(self, username):
    res = post(self.url, params={'value': username})
    if res.status_code == codes.TOO_MANY:
      self.next_queue.put(username)
    return res.status_code, username

  def log(self, code, username):
    icon = self.LOG_ICONS.get(code, '❓')
    code = colors.header(code)
    msg = " ".join([icon, username, code, "\n"])
    for out in self.outputs:
      out.write(msg)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--domain", default="bruteforce")
  parser.add_argument("--workers", default=10)
  parser.add_argument("--url", default=SignupChecker.URL)
  parser.add_argument("--test", action='store_true')
  args = vars(parser.parse_args())
  SignupChecker(**args).run()
