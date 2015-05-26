import os
from collections import deque, Counter

import HttpParser as P
from logger import get_logger

EXPT_NFLAGS = 5


class Crawler:
    """
    The model for a Web Crawler
    """
    def __init__(self, entry, domain, client, crawlall=False):
        self.logger = get_logger(os.path.basename(__file__))
        self.logger.debug("Initializing the Crawler")
        target_regex = r'secret_flag[^>]*>FLAG:\s*([0-9a-zA-Z]{64})<'
        self.parser = P.HttpParser(target_regex)
        self.domain = domain
        self.client = client
        self.crawlall = crawlall
        self.uris_queue = deque([entry])
        self.uris_seen = set([])
        self.counters = Counter(html=0, secret_flags=0)

    def dump_counters(self):
        dump = '\n'.join('\t%s: %d' % (k, v) for (k, v)
                         in self.counters.items())
        self.logger.info("Counters in Crawler:\n%s" % dump)
        return self.counters

    def crawl(self):
        secret_flags = set([])
        while (self.uris_queue):
            uri = self._deque_uri()
            self.uris_seen.add(uri)
            html = self.client.GET(uri)[2]
            self.counters['html'] += 1
            new_urls = self.parser.parse_urls(html)
            flags = self.parser.parse_secret(html)
            if flags:
                secret_flags.update(flags)
                self.counters["secret_flags"] = len(secret_flags)
                self.logger.info("Found %d secret flags: %s, Total found %d"
                                 % (len(flags), flags, len(secret_flags)))
                if self._can_quit(secret_flags):
                    self.logger.info(("Found all %d secret flags, "
                                     + "quiting because the crawlall "
                                     + "flag is set to %s")
                                     % (EXPT_NFLAGS, str(self.crawlall)))
                    break
            valid_uris = self._get_valid_uris(new_urls)
            self._enque_uris(valid_uris)
        return secret_flags

    def _can_quit(self, secret_flags):
        """
        If the 5 secret flags have been crawled and we don't
        set the crawlall flag to True, then we can just quit
        at this point
        """
        return ((len(secret_flags) == EXPT_NFLAGS) and (not self.crawlall))

    def _deque_uri(self):
        if self.uris_queue:
            return self.uris_queue.popleft()
        else:
            return None

    def _enque_uris(self, uris):
        uris = filter(self._not_seen, uris)
        self.uris_seen.update(uris)
        self.uris_queue.extend(uris)
        return len(uris)

    def _not_seen(self, uri):
        return (uri not in self.uris_seen)

    def _get_valid_uris(self, urls):
        valid_uris = set([])
        for url in urls:
            host, uri = self.parser.parse_url(url)
            if host and host != self.domain:
                self.logger.debug("Invalid host: %s, out of domain %s"
                                  % (host, self.domain))
            else:
                valid_uris.add(uri)
        return valid_uris
