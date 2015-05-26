#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <netdb.h>

#define PORT "27993"
#define SSL_PORT "27994"
#define RECVBUFSIZE 256
#define MSG_HEADER "cs5700spring2014"
#define MSG_HELLO "HELLO"
#define MSG_STATUS "STATUS"
#define MSG_BYE "BYE"
#define SPACE " "
#define RETURN "\n"
#define MSG_DELIM " \n"

#define UNKNOWN_NUID "Unknown_Husky_ID"

#define LEN_CHAR 1
#define LEN_SECRET_FLAG 64

#define DEBUG 0

/**
 * Print formatted messages to stdout
 */
int print(const char *format, ...);

/**
 * Kill the client program with error messages
 */
void die(const char *err_msg, int usage);

/**
 * Check and parse the command line arguments
 */
void parse_args(int argc, char **argv, int *p_flag, char **port,
        int *s_flag, char **host_name, char **neu_id);

/**
 * Initialize the server socket address
 */
struct sockaddr_in *init_server_addr(struct hostent *host_entry,
        unsigned short server_port);

/**
 * Get the specified string field from the given string
 * The index starts from 0
 */
char* get_field(char *message, int index, const char *delim);

/**
 * Check if the given message is the correct format
 * The message would be one of STATUS/BYE
 */
void assert_format(char *status, int is_bye);

/**
 * Parse and resolve the expression
 * WARNING: must manually release the memory returned by this function
 */
char* resolve(char *status_msg);

