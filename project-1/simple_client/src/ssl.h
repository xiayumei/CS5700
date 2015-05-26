#include <openssl/ssl.h>
#include <openssl/err.h>
#include "common.h"

#define SOCK_COMM_STYLE SOCK_STREAM
#define SOCK_NAME_SPACE PF_INET
#define SOCK_PROTOCOL 0
#define SOCK_CREATE_ERROR -1

#define MSG_ERROR_SSL_IS_NULL "ssl is null"
#define MSG_ERROR_SSL_INIT "ssl init error"
#define MSG_ERROR_SSL_NEW "ssl create error"
#define MSG_ERROR_SSL_CONNECT "ssl connect error"
#define MSG_ERROR_SOCKET_CREATE_ERROR "socket create error"
#define MSG_ERROR_SOCKET_INVALIDE_HOST "socket invalid host"
#define MSG_ERROR_SOCKET_BIND "socket bind error"
#define MSG_ERROR_SOCKET_CONNECT "socket connect error"

char* ssl_part(int fd, char *nuid);

