#!/usr/bin/env python
import sys


def stat_hosts_by_ip(ipfile, meddle_server_ip,
                     device_vpn_ip, device_isp_ip):
    ip_parts = meddle_server_ip.split('.')
    meddle_mask = '.'.join([ip_parts[0], ip_parts[1], ''])
    ip_parts = device_vpn_ip.split('.')
    vpn_mask = '.'.join([ip_parts[0], ip_parts[1], ''])
    ipmap = {}
    with open(ipfile, 'r') as f:
        for line in f:
            dest_ip = line.split(',')[1].strip().split()[1].strip()
            if not dest_ip.startswith(meddle_mask) and \
                    not dest_ip.startswith(vpn_mask):
                if dest_ip in ipmap:
                    ipmap[dest_ip] += 1
                else:
                    ipmap[dest_ip] = 1
    return ipmap


def dump_stats(ipmap, out_path, filename):
    filepath = '/'.join([out_path, filename])
    with open(filepath, 'a') as f:
        for k, v in ipmap.items():
            f.write('%s %d\n' % (k, v))


def main():
    ipfile = sys.argv[1]
    meddle_server_ip = sys.argv[2]
    device_vpn_ip = sys.argv[3]
    device_isp_ip = sys.argv[4]
    out_path = sys.argv[5]
    out_filename = sys.argv[6]
    ipmap = stat_hosts_by_ip(ipfile, meddle_server_ip,
                             device_vpn_ip, device_isp_ip)
    dump_stats(ipmap, out_path, out_filename)


if __name__ == '__main__':
    main()
