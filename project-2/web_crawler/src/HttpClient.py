import socket as s
import os
from collections import Counter

import HttpParser as P
from logger import get_logger

DELIM = "\r\n"
BLANK = ""
RECVBUFSIZE = 8192
RC = {
    "200": "OK",
    "301": "Moved",
    "302": "Found",
    "403": "Forbidden",
    "404": "Not Found",
    "500": "Internal Error",
}


class HttpClient:
    """
    A simple HTTP client wrapper based on socket
    ONE client per host
    """
    def __init__(self, server, port):
        self.logger = get_logger(os.path.basename(__file__))
        self.logger.debug("Initializing the HTTP client")
        self.server = server
        self.port = port
        self.GET_BASE = self._GET_base()
        self.POST_BASE = self._POST_base()
        self.http_params = {
            "uri": BLANK,
            "sessionid": BLANK,
            "csrftoken": BLANK,
            "contlen": len(BLANK),
            "content": BLANK,
        }   # get params are usually a subset of post params
        self.login_params = {
            "username": BLANK,
            "password": BLANK,
            "csrfmiddlewaretoken": BLANK,
        }
        self.parser = P.HttpParser()
        self.socket = None
        self.counters = Counter(GET=0, POST=0, OK=0,
                                REDR=0, DROP=0, RETRY=0)

    def dump_counters(self):
        dump = '\n'.join('\t%s: %d' % (k, v) for (k, v)
                         in self.counters.items())
        self.logger.info("Counters in HttpClient:\n%s" % dump)
        return self.counters

    def login(self, username, password):
        response_code, headers, html = self.GET("/accounts/login/")
        # grab auth tokens
        hdr_vals = self.parser.get_header_values(headers, "Set-Cookie")
        csrftoken = self.parser.get_header_parameter(hdr_vals, "csrftoken")
        sessionid = self.parser.get_header_parameter(hdr_vals, "sessionid")
        self.logger.info("GET login page: %s, sessionid: %s"
                         % (response_code, sessionid))
        # construct login post request content
        self.login_params["csrfmiddlewaretoken"] = csrftoken
        self.login_params["username"] = username
        self.login_params["password"] = password
        login_content = self._login_content(**self.login_params)
        # construct login post request
        self.http_params["csrftoken"] = csrftoken
        self.http_params["sessionid"] = sessionid
        self.http_params["contlen"] = len(login_content)
        self.http_params["content"] = login_content
        response_code, headers, html = self.POST("/accounts/login/",
                                                 login_content)
        self.logger.info("POST login form: %s, sessionid: %s"
                         % (response_code, self.http_params["sessionid"]))

    def logout(self):
        response_code, headers, html = self.GET("/accounts/logout/")
        self._close_connection()
        self.logger.info("Logout: %s" % response_code)

    def GET(self, uri):
        self.counters["GET"] += 1
        self.http_params["uri"] = uri
        response = self._send_request(self.GET_BASE, **self.http_params)
        response_code = self.parser.get_response_code(response)
        headers, html = self._process_response(
            response_code, response, self.GET_BASE, **self.http_params)
        return response_code, headers, html

    def POST(self, uri, content):
        self.counters["POST"] += 1
        self.http_params["uri"] = uri
        self.http_params["content"] = content
        self.http_params["contlen"] = len(content)
        response = self._send_request(self.POST_BASE, **self.http_params)
        response_code = self.parser.get_response_code(response)
        # get the new sessionid if there is one
        headers = self.parser.split_response(response)[0]
        try:
            cookie_values = self.parser.get_header_values(headers,
                                                          "Set-Cookie")
            sessionid = self.parser.get_header_parameter(cookie_values,
                                                         "sessionid")
            self.http_params["sessionid"] = sessionid
            self.logger.info("Get a new sessionid from the POST response")
        except RuntimeError:
            self.logger.info("Cannot get a new sessionid from the "
                             + "POST response, continuing")
            pass
        headers, html = self._process_response(
            response_code, response, self.POST_BASE, **self.http_params)
        return response_code, headers, html

    def _send_request(self, req_base, **params):
        self.logger.debug("[Request: %s]" % params["uri"])
        request = req_base % params
        self._close_connection()
        self.socket = self._new_connection()
        self.socket.sendall(request)
        response = self.socket.recv(RECVBUFSIZE)
        return response

    def _process_response(self, rc, response, req_base, **params):
        headers, html = self.parser.split_response(response)
        if rc in ("200",):  # just return the html if OK
            self.logger.debug("[Response: %s %s, URL: %s], OK"
                              % (rc, RC[rc], params["uri"]))
            self.counters["OK"] += 1
            return headers, html
        elif rc in ("301", "302",):   # redirect to new location
            self.logger.warn("[Response: %s %s, URL: %s], redirecting"
                             % (rc, RC[rc], params["uri"]))
            self.counters["REDR"] += 1
            location = self.parser.get_header_values(headers, "Location")[0]
            host, uri = self.parser.parse_url(location)
            self._ensure_host(host)
            rc, headers, html = self.GET(uri)
            return headers, html
        elif rc in ("403", "404",):   # abandon the broken url
            self.logger.warn("[Response: %s %s, URL: %s], dropping the url"
                             % (rc, RC[rc], params["uri"]))
            self.counters["DROP"] += 1
            return headers, BLANK if html is None else html
        elif rc in ("500",):    # retry until success
            self.logger.warn("[Response: %s %s, URL: %s], retrying"
                             % (rc, RC[rc], params["uri"]))
            self.counters["RETRY"] += 1
            response = self._send_request(req_base, **params)
            rc = self.parser.get_response_code(response)
            return self._process_response(rc, response,
                                          req_base, **params)
        else:   # abandon unsupported response
            self.logger.warn("[Response: %s, URL: %s], unsupported response"
                             % (rc, params["uri"]))
            return headers, BLANK if html is None else html

    def _ensure_host(self, host):
        if host and host != self.server:
            self.logger.error("Trying to redirect to a illegal host: %s"
                              % host)
            raise RuntimeError()

    def _new_connection(self):
        socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        socket.connect((self.server, self.port))
        return socket

    def _close_connection(self):
        if self.socket:
            self.socket.close()

    def _GET_base(self):
        """
        Return a GET request string with placeholder
        """
        GET_BASE = "GET %(uri)s HTTP/1.1" + DELIM + \
            "From: yuan.yin@husky.neu.edu" + DELIM + \
            "User-Agent: enzen/1.0" + DELIM + \
            "Cookie: csrftoken=%(csrftoken)s; sessionid=%(sessionid)s" + \
            DELIM + \
            "Host: cs5700.ccs.neu.edu" + DELIM + \
            "Connection: keep-alive" + DELIM + \
            "Accept: text/html,application/xhtml+xml,application/xml;" + \
            "q=0.9,image/webp,*/*;q=0.8" + DELIM + \
            DELIM
        return GET_BASE

    def _POST_base(self):
        """
        Return a POST request string with placeholder
        """
        POST_BASE = "POST %(uri)s HTTP/1.1" + DELIM + \
            "From: yuan.yin@husky.neu.edu" + DELIM + \
            "User-Agent: enzen/1.0" + DELIM + \
            "Cookie: csrftoken=%(csrftoken)s; sessionid=%(sessionid)s" + \
            DELIM + \
            "Content-Type: application/x-www-form-urlencoded" + DELIM + \
            "Content-Length: %(contlen)d" + DELIM + \
            "Host: cs5700.ccs.neu.edu" + DELIM + \
            "Connection: keep-alive" + DELIM + \
            "Accept: text/html,application/xhtml+xml,application/xml;" + \
            "q=0.9,image/webp,*/*;q=0.8" + DELIM + \
            DELIM + "%(content)s"
        return POST_BASE

    def _login_content(self, **kwargs):
        """
        Return login request parameters content
        """
        content = "csrfmiddlewaretoken=%(csrfmiddlewaretoken)s" + \
            "&username=%(username)s" + \
            "&password=%(password)s" + \
            "&next=/fakebook/"
        return content % kwargs
