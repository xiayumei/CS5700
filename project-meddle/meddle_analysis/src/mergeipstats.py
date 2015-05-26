#!/usr/bin/env python
import sys


def main():
    ipstatsfile = sys.argv[1]
    ipstatsfile_merged = sys.argv[2]
    ipstats_merged = {}
    with open(ipstatsfile, 'r') as f:
        for line in f:
            stats = line.split()
            ip = stats[0]
            count = int(stats[1])
            if ip in ipstats_merged:
                ipstats_merged[ip] += count
            else:
                ipstats_merged[ip] = count
    with open(ipstatsfile_merged, 'w') as f:
        for k, v in ipstats_merged.items():
            f.write('%s %d\n' % (k, v))


if __name__ == '__main__':
    main()
