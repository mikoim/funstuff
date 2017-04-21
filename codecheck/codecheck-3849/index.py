import argparse

from app import LookAndSay

parser = argparse.ArgumentParser()
parser.add_argument('number', type=int, default=1, help='Print n\'th term in look-and-say sequence')
parser.add_argument('--limit', type=int, default=None, help='Limit number of digits')
args = parser.parse_args()

val = None
for val in LookAndSay(args.number, args.limit):
    pass

print(val)
