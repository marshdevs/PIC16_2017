import sys
import re

data = []

for line in sys.stdin:
    listtt = re.findall(",[0-9][0-9]*", line)
    data.append(listtt)

print data