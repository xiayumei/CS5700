#!/usr/bin/env python
import argparse

from collections import OrderedDict
from utils import ns, frange, format_trace_file_name
from process import post_process, wait_for


def parse_arguments():
    """
    Set up simple arguments parsing
    """
    parser = argparse.ArgumentParser()
    init_parent_parser(parser)
    subparsers = parser.add_subparsers()
    parser_exp1 = subparsers.add_parser('exp1')
    parser_exp2 = subparsers.add_parser('exp2')
    parser_exp3 = subparsers.add_parser('exp3')
    init_exp1_parser(parser_exp1)
    init_exp2_parser(parser_exp2)
    init_exp3_parser(parser_exp3)
    return parser.parse_args()


def init_parent_parser(parser):
    parser.add_argument('-g', '--granularity', type=float,
                        choices=[0.10, 0.01], default=0.1,
                        help='The granularity of the increase of cbr_rate')


def init_exp1_parser(parser_exp1):
    """
    Argument parser for experiment1
    """
    parser_exp1.add_argument('-o', '--out', type=str,
                             default='../out/experiment1/exp1.tr',
                             help='The name of the output file in experiment1')
    parser_exp1.add_argument('--cbr-start', type=float, default=0.5,
                             help='Start time of the CBR flow in experiment1')
    parser_exp1.add_argument('--cbr-stop', type=float, default=99.5,
                             help='Stop time of the CBR flow in experiment1')
    parser_exp1.add_argument('--tcp-start', type=float, default=1.0,
                             help='Start time of the TCP flow in experiment1')
    parser_exp1.add_argument('--tcp-stop', type=float, default=99.0,
                             help='Stop time of the TCP flow in experiment1]')
    parser_exp1.add_argument('-d', '--duration', type=float, default=100.0,
                             help='The total simulation time of experiment1')
    parser_exp1.set_defaults(which='exp1')


def init_exp2_parser(parser_exp2):
    """
    Argument parser for experiment2
    """
    parser_exp2.add_argument('-o', '--out', type=str,
                             default='../out/experiment2/exp2.tr',
                             help='The name of the output file in experiment2')
    parser_exp2.add_argument('--cbr-start', type=float, default=0.5,
                             help='Start time of the CBR flow in experiment2')
    parser_exp2.add_argument('--cbr-stop', type=float, default=99.5,
                             help='Stop time of the CBR flow in experiment2')
    parser_exp2.add_argument('--tcp1-start', type=float, default=1.0,
                             help='Start time of the left TCP flow in '
                             + 'experiment2')
    parser_exp2.add_argument('--tcp1-stop', type=float, default=99.0,
                             help='Stop time of the left TCP flow in '
                             + 'experiment2')
    parser_exp2.add_argument('--tcp2-start', type=float, default=1.0,
                             help='Start time of the right TCP flow in '
                             + 'experiment2')
    parser_exp2.add_argument('--tcp2-stop', type=float, default=99.0,
                             help='Stop time of the right TCP flow in '
                             + 'experiment2')
    parser_exp2.add_argument('-d', '--duration', type=float, default=100.0,
                             help='The total simulation time of experiment2')
    parser_exp2.set_defaults(which='exp2')


def init_exp3_parser(parser_exp3):
    """
    Argument parser for experiment3
    """
    parser_exp3.add_argument('-o', '--out', type=str,
                             default='../out/experiment3/exp3.tr',
                             help='The name of the output file in experiment3')
    parser_exp3.add_argument('-r', '--cbr-rate', type=float, default=8.0,
                             help='The CBR rate for all agents in experiment3')
    parser_exp3.add_argument('--cbr-start', type=float, default=2.5,
                             help='Start time of the CBR flow in experiment3')
    parser_exp3.add_argument('--cbr-stop', type=float, default=99.0,
                             help='Stop time of the CBR flow in experiment3')
    parser_exp3.add_argument('--tcp-start', type=float, default=0.5,
                             help='Start time of the TCP flow in experiment3')
    parser_exp3.add_argument('--tcp-stop', type=float, default=99.5,
                             help='Stop time of the TCP flow in experiment3')
    parser_exp3.add_argument('-d', '--duration', type=float, default=100.0,
                             help='The total simulation time of experiment3')
    parser_exp3.set_defaults(which='exp3')


def run_experiment1(args):
    """
    Main entry for executing experiment1 and executing yielded
    files one by one
    """
    threads = []
    tcp_agents = OrderedDict({})
    tcp_agents['Tahoe'] = 'Agent/TCP'
    tcp_agents['Reno'] = 'Agent/TCP/Reno'
    tcp_agents['NewReno'] = 'Agent/TCP/Newreno'
    tcp_agents['Vegas'] = 'Agent/TCP/Vegas'
    cbr_rates = frange(1.00, 10.00, args.granularity)
    for agent_name, agent in tcp_agents.items():
        for cbr_rate in cbr_rates:
            out_file = format_trace_file_name(args.out, agent_name, cbr_rate)
            nsargs = [agent, cbr_rate, out_file, args.cbr_start, args.cbr_stop,
                      args.tcp_start, args.tcp_stop, args.duration]
            rc = ns('../ns2/experiment1.tcl', nsargs)
            nsargs.append(str(rc))
            nsargs[0] = agent_name
            print ("experiment1, tcp_agent: %s, cbr_rate: %s, " +
                   "out_to: %s, cbr_start: %s, cbr_stop: %s, " +
                   "tcp_start: %s, tcp_stop: %s, duration: %s, " +
                   "return code: %s") % tuple(map(lambda x: str(x), nsargs))
            kwargs = {
                'cbr_rate': str(cbr_rate),
                'agent_name': agent_name,
            }
            t = post_process(args.which, out_file, **kwargs)
            threads.append(t)
    # waits for all thread finish once get out of the loop
    wait_for(threads)


def run_experiment2(args):
    """
    Main entry for executing experiment2 and executing yielded
    files one by one
    """
    threads = []
    tcp_agent_pairs = OrderedDict({})

    tcp_agent_pairs[('Reno', 'Reno')] = ('Agent/TCP/Reno',
                                         'Agent/TCP/Reno')
    tcp_agent_pairs[('NewReno', 'Reno')] = ('Agent/TCP/Newreno',
                                            'Agent/TCP/Reno')
    tcp_agent_pairs[('Vegas', 'Vegas')] = ('Agent/TCP/Vegas',
                                           'Agent/TCP/Vegas')
    tcp_agent_pairs[('NewReno', 'Vegas')] = ('Agent/TCP/Newreno',
                                             'Agent/TCP/Vegas')
    cbr_rates = frange(1.00, 10.00, args.granularity)
    for pair_names, agent_pair in tcp_agent_pairs.items():
        for cbr_rate in cbr_rates:
            pair_name = '-'.join(pair_names)
            out_file = format_trace_file_name(args.out, pair_name, cbr_rate)
            nsargs = [agent_pair[0], agent_pair[1], cbr_rate, out_file,
                      args.cbr_start, args.cbr_stop, args.tcp1_start,
                      args.tcp1_stop, args.tcp2_start, args.tcp2_stop,
                      args.duration]
            rc = ns('../ns2/experiment2.tcl', nsargs)
            nsargs.append(str(rc))
            nsargs[1] = pair_name
            print ("experiment2, tcp_agents: %s, cbr_rate: %s, " +
                   "out_to: %s, cbr_start: %s, cbr_stop: %s, " +
                   "tcp1_start: %s, tcp1_stop: %s, tcp2_start: %s" +
                   "tcp2_stop: %s, duration: %s, return code: %s") \
                % tuple(map(lambda x: str(x), nsargs[1:]))
            kwargs = {
                'cbr_rate': str(cbr_rate),
                'agent1_name': pair_names[0],
                'agent2_name': pair_names[1],
            }
            t = post_process(args.which, out_file, **kwargs)
            threads.append(t)
    # waits for all thread finish once get out of the loop
    wait_for(threads)


def run_experiment3(args):
    """
    Main entry for executing experiment3 and executing yielded
    files one by one
    """
    threads = []
    tcp_agents_sink = OrderedDict({})
    tcp_agents_sink['Reno'] = ('Agent/TCP/Reno', 'Agent/TCPSink')
    tcp_agents_sink['Sack'] = ('Agent/TCP/Sack1', 'Agent/TCPSink/Sack1')
    queue_types = ['DropTail', 'RED']
    for agent_name, agent_sink in tcp_agents_sink.items():
        for queue_type in queue_types:
            out_file = format_trace_file_name(args.out, agent_name,
                                              args.cbr_rate, queue_type)
            nsargs = [agent_sink[0], agent_sink[1], queue_type, args.cbr_rate,
                      out_file, args.cbr_start, args.cbr_stop, args.tcp_start,
                      args.tcp_stop, args.duration]
            rc = ns('../ns2/experiment3.tcl', nsargs)
            nsargs.append(str(rc))
            nsargs[0] = agent_name
            print ("experiment3, tcp_agent: %s, tcp_sink: %s, " +
                   "queue_type: %s, cbr_rate: %s, out_to: %s, " +
                   "cbr_start: %s, cbr_stop: %s, tcp_start: %s, " +
                   "tcp_stop: %s, duration: %s, return code: %s") \
                % tuple(map(lambda x: str(x), nsargs))
            kwargs = {
                'agent_name': agent_name,
                'queue_type': queue_type,
            }
            t = post_process(args.which, out_file, **kwargs)
            threads.append(t)
    # waits for all thread finish once get out of the loop
    wait_for(threads)


if __name__ == "__main__":
    args = parse_arguments()
    if args.which == 'exp1':
        print 'Running experiment1'
        run_experiment1(args)
    elif args.which == 'exp2':
        print 'Running experiment2'
        run_experiment2(args)
    elif args.which == 'exp3':
        print 'Running experiment3'
        run_experiment3(args)
    else:
        print 'Wrong experiment number, aborting'
        exit(1)
