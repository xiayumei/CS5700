#!/usr/bin/env python
import os
import argparse

from logger import init_logger, get_logger
import HttpClient as H
import Crawler as C
from utils import Timer


def parse_arguments():
    """
    Set up the arugments and parse the command
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("username",
                        type=str,
                        help="The user name for Fakebook")
    parser.add_argument("password",
                        type=str,
                        help="The password for Fakebook")
    parser.add_argument("-s", "--server",
                        type=str,
                        default="cs5700.ccs.neu.edu",
                        action="store",
                        help="The name of the server to first connect")
    parser.add_argument("-p", "--port",
                        type=int,
                        default=80,
                        action="store",
                        help="The port number of the server above")
    parser.add_argument("-e", "--entry",
                        type=str,
                        default="/",
                        action="store",
                        help="The entry url for the crawler")
    parser.add_argument("-d", "--domain",
                        type=str,
                        default="cs5700.ccs.neu.edu",
                        action="store",
                        help="The domain restrict for the crawler")
    parser.add_argument("-a", "--crawlall",
                        action="store_true",
                        help="If specified, crawl all web pages even"
                        + " if the 5 secret flags have been found")
    parser.add_argument("-l", "--logfile",
                        type=str,
                        action="store",
                        help="The name of the log file")
    parser.add_argument("-v", "--verbosity",
                        action="count",
                        default=0,
                        help="Increase program verbosity")
    return parser.parse_args()


if __name__ == '__main__':
    # parse command line arguments
    args = parse_arguments()

    # init logging
    init_logger(args.logfile, args.verbosity)
    logger = get_logger(os.path.basename(__file__))
    logger.info("Running the Web Crawler in verbosity Level: %d"
                % args.verbosity)

    # init the http client
    client = H.HttpClient(args.server, args.port)

    # login into fakebook
    client.login(args.username, args.password)

    # init the crawler
    crawler = C.Crawler(args.entry, args.domain, client, args.crawlall)

    # crawl it
    with Timer() as t:
        secret_flags = crawler.crawl()
    logger.info("Time taken for crawling: %ss" % t.duration)

    # logout from fakebook
    client.logout()

    # print out the 5 secret_flags
    print '\n'.join(flag for flag in secret_flags)

    # dump counters for statistics
    crawler.dump_counters()
    client.dump_counters()
