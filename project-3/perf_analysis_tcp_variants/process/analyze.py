from utils import avg_rtts, format_data_file_name, save_to_file


"""
type = fields[0]
time = fields[1]
src_node = fields[2]
dest_node = fields[3]
pkt_name = fields[4]
pkt_size = fields[5]
flags = fields[6]
flow_id = fields[7]
src_addr = fields[8]
dest_addr = fields[9]
seq_num = fields[10]
pkt_uid = fields[11]
"""

# file scope constants
evt_drop = 'd'
evt_recv = 'r'
evt_enque = '+'
delim = ' '


def process_exp1_file(filename, **kwargs):
    print 'Processing exp1 file: %s' % filename
    # function scope constants
    cbr_rate = kwargs.pop('cbr_rate')
    agent_name = kwargs.pop('agent_name')
    tcp_fid = '2'
    tcp_src_node = '0'
    tcp_sink_node = '3'

    # function scope refs
    pkt_tcp_uids = set()
    pkt_drops = 0
    throughput = 0
    rtts = {}
    cells = None
    with open(filename, 'r') as f:
        for line in f:
            cells = line.split()
            # grab tcp events according to the flow id
            if cells[7] == tcp_fid:
                # adds the packet unique id to the set
                pkt_tcp_uids.add(cells[11])
                # record tcp drop event, no need to proceed
                if cells[0] == evt_drop:
                    pkt_drops += 1
                    continue
                # a tcp packet enque (send) event
                elif cells[0] == evt_enque:
                    # if it is a tcp packet sent from tcp src node
                    if cells[2] == tcp_src_node and cells[4] == 'tcp':
                        # record the start time of rtt: (start, end)
                        # if the seq num not exists in the dict
                        if cells[10] not in rtts:
                            rtts[cells[10]] = [float(cells[1]), None]
                    continue
                # a tcp packet recv event
                elif cells[0] == evt_recv:
                    # if it is a tcp packet recved by tcp sink node
                    if cells[3] == tcp_sink_node:
                        # record record packet size to throughput
                        throughput += int(cells[5])
                    # a tcp src node recv (ack) event
                    elif cells[3] == tcp_src_node and cells[4] == 'ack':
                        if cells[10] in rtts:
                            # update rtt end time
                            rtts[cells[10]][1] = float(cells[1])
                            # record ack packet size to throughput
                            throughput += int(cells[5])
                    continue

    # convert throughput, in MB
    throughput = float(throughput) / (1024.0 * 1024.0)
    # calculate drop rate, in digits
    pkt_tcp = len(pkt_tcp_uids)
    drop_rate = float(pkt_drops) / float(pkt_tcp)
    # calculate latency, in seconds
    latency = avg_rtts(rtts)
    print 'From pkt drop field: %d packets were dropped' % pkt_drops
    # append to file
    save_to_file(format_data_file_name(filename, agent_name, 'THP'),
                 delim, *[cbr_rate, throughput])
    save_to_file(format_data_file_name(filename, agent_name, 'DR'),
                 delim, *[cbr_rate, drop_rate])
    save_to_file(format_data_file_name(filename, agent_name, 'LT'),
                 delim, *[cbr_rate, latency])


def process_exp2_file(filename, **kwargs):
    print 'Processing exp2 file: %s' % filename
    # function scope constants
    cbr_rate = kwargs.pop('cbr_rate')
    agent_names = (kwargs.pop('agent1_name'), kwargs.pop('agent2_name'))
    tcp_fids = ('2', '3')
    tcp_src_nodes = ('0', '4')
    tcp_sink_nodes = ('3', '5')

    # function scope refs
    pkt_tcp_uids = [set(), set()]
    pkt_tcp = [0, 0]
    drop_rates = [0.0, 0.0]
    latencies = [0.0, 0.0]
    pkt_drops = [0, 0]
    throughputs = [0, 0]
    rtts = [{}, {}]
    cells = None
    i = 0
    with open(filename, 'r') as f:
        for line in f:
            cells = line.split()
            try:
                i = tcp_fids.index(cells[7])
            except ValueError:
                continue

            # now switched to corresponding var space
            pkt_tcp_uids[i].add(cells[11])
            if cells[0] == evt_drop:
                pkt_drops[i] += 1
                continue
            elif cells[0] == evt_enque:
                if cells[2] == tcp_src_nodes[i] and cells[4] == 'tcp':
                    if cells[10] not in rtts[i]:
                        rtts[i][cells[10]] = [float(cells[1]), None]
                continue
            elif cells[0] == evt_recv:
                if cells[3] == tcp_sink_nodes[i]:
                    throughputs[i] += int(cells[5])
                elif cells[3] == tcp_src_nodes[i] and cells[4] == 'ack':
                    if cells[10] in rtts[i]:
                        rtts[i][cells[10]][1] = float(cells[1])
                        throughputs[i] += int(cells[5])
                continue

    # save to file
    for i in (0, 1):
        throughputs[i] = float(throughputs[i]) / (1024.0 * 1024.0)
        pkt_tcp[i] = len(pkt_tcp_uids[i])
        drop_rates[i] = float(pkt_drops[i]) / float(pkt_tcp[i])
        latencies[i] = avg_rtts(rtts[i])
        print 'From pkt drop field: %d packets were dropped' % pkt_drops[i]

    cust_name = '_'.join(agent_names)
    save_to_file(format_data_file_name(filename, cust_name, 'THP'),
                 delim, *[cbr_rate, throughputs[0], throughputs[1]])
    save_to_file(format_data_file_name(filename, cust_name, 'DR'),
                 delim, *[cbr_rate, drop_rates[0], drop_rates[1]])
    save_to_file(format_data_file_name(filename, cust_name, 'LT'),
                 delim, *[cbr_rate, latencies[0], latencies[1]])


def process_exp3_file(filename, **kwargs):
    print 'Processing exp3 file: %s' % filename

    print filename

    agentname = kwargs.pop('agent_name')
    queuetype = kwargs.pop('queue_type')

    tcp_fid = '2'

    ## Four files will be handled here
    ## reno_droptail, reno_red, sack_droptail, sack_red

    ## rtts : {[seqNum] : [(first send time), (first ack received time)]}
    rtts = {}
    ## tps : {[second] : [throughput]}; e.g. : second : 0 ~ 1;
    tps = {}

    with open(filename, 'r') as f:
        for line in f:
            cells = line.split()
            ## if this flow is not tcp flow, continue it.
            if cells[7] != tcp_fid:
                continue

            # calculate throughput for each second
            # refactor
            # if it is an ack received by node 0, add package size into
            # throughput of this second
            # if it is an tcp received by node 3, add package size into
            # throughput of this second
            if cells[0] == 'r' and \
                    ((cells[3] == '0' and cells[4] == 'ack') or
                     (cells[3] == '3' and cells[4] == 'tcp')):
                ## if this is an ack received by node 0;
                ## put timestamp into rtts's recv time part.
                if cells[3] == '0' and cells[10] in rtts:
                    rtts[cells[10]][1] = float(cells[1])
                ## calculate the throughput
                timeindex = int(float(cells[1]))
                if timeindex in tps:
                    tps[timeindex][0] += int(cells[5])
                    tps[timeindex][1] += 1
                else:
                    tps[timeindex] = [int(cells[5]), 1]
                    continue

            ## if node 0 send this SeqNum package for the first time
            ## add a new rtt into rtts dict with seqNum as the key
            if cells[0] == '+' and cells[2] == '0' and cells[10] not in rtts:
                rtts[cells[10]] = [float(cells[1]), None]
                continue

    cust_name = '%s_%s' % (agentname, queuetype)

    ## save bandwidth file
    ## each file record format: <time bandwidth>
    bandwidthfilename = format_data_file_name(filename, cust_name, 'THP')
    bandwidthfile = open(bandwidthfilename, 'a')
    record_tmp = '%f %f\n'
    for key in tps:
        time = key + 0.5
        thp = tps[key][0] * 1.0 / (1024 * 1024)
        record = record_tmp % (time, thp)
        bandwidthfile.write(record)
    bandwidthfile.close()

    print bandwidthfilename

    lst = []

    for key in rtts:
        if not rtts[key][1]:
            continue
        latency = rtts[key][1] - rtts[key][0]
        time = rtts[key][0] + latency / 2
        item = (time, latency * 1000)
        lst.append(item)

    lst.sort(key=lambda tup: tup[0])

    ## save latency file
    ## each file record format: <time latency>
    latencyfilename = format_data_file_name(filename, cust_name, 'LT')
    latencyfile = open(latencyfilename, 'a')
    record_tmp = '%f %f\n'
    for item in lst:
        record = record_tmp % (item[0], item[1])
        latencyfile.write(record)
    latencyfile.close()

    print latencyfilename
