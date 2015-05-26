import os
import subprocess


def ns(tcl, args):
    """
    Execute the tcl script with args
    """
    cmd = []
    cmd.append('ns')
    cmd.append(tcl)
    cmd.extend(args)
    cmd = map(lambda x: str(x), cmd)
    try:
        return subprocess.call(cmd)
    except OSError as e:
        # print 'OSError({0}): {1}'.format(e.errno, e.strerror)
        cmd[0] = '/course/cs4700f12/ns-allinone-2.35/bin/ns'
        return subprocess.call(cmd)


def frange(off, end, step):
    """
    Get a list of floating range
    """
    ret = []
    e = off
    while e < end:
        ret.append(e)
        e += step
    return ret


def purge_file(path):
    """
    Delete the file with the given name
    if it exists
    """
    try:
        os.remove(path)
    except OSError, e:
        raise e


def avg_rtts(atts_dict):
    """
    Return the average rtt in ms of the atts
    in the given dict, as latency, in seconds
    """
    total = 0.0
    bad_rtts = 0
    for k, v in atts_dict.items():
        if v[0] and v[1]:
            total += (v[1] - v[0])
        else:
            print 'Packet: %s has null ack time: %s' % (k, tuple(v))
            bad_rtts += 1
    print 'From rtts dict: %d packets has null ack time' % bad_rtts
    num_valid_rtts = len(atts_dict.items()) - bad_rtts
    avg_rtts = (total / num_valid_rtts) * 1000
    return avg_rtts


def format_trace_file_name(basename, agent_name, cbr_rate, queue_type=None):
    """
    Returns a formatted output file name
    e.g. ../out/experiment1/exp1-Tahoe-cbrate1.tr
    """
    out_path, out_file = _split_file_name(basename)
    prefix, suffix = out_file.split('.')
    if queue_type:
        final_name = '%s/%s-%s-%s.%s' % \
            (out_path, prefix, agent_name, queue_type, suffix)
    else:
        final_name = '%s/%s-%s-cbrate%.2f.%s' % \
            (out_path, prefix, agent_name, cbr_rate, suffix)
    return final_name


def format_data_file_name(basename, cust_name, data_type):
    """
    Customize a new file new for stats data
    """
    out_path, tmp_name = _split_file_name(basename)
    return '%s/%s-%s.dat' % (out_path, data_type, cust_name)


def _split_file_name(filepath):
    """
    split the given filepath to a tuple of basepath and filename
    """
    basepath = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    return basepath, filename


def save_to_file(filename, delim, *args):
    """
    Save the given args list to file
    """
    line = delim.join(str(arg) for arg in args)
    line += '\n'
    with open(filename, 'a') as f:
        f.write(line)
        f.flush()
