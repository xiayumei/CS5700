#include "ssl.h"

void set_fd_for_ssl(SSL *ssl, int id);
void set_fd_for_ssl(SSL *ssl, int id);
SSL_CTX* ssl_init();
SSL * my_ssl_connect(SSL *ssl, SSL_CTX *ctx, int fd);

void send_hello(SSL *ssl, char *nuid);
char* receive_puzzle(SSL *ssl);

char* ssl_part(int fd, char *nuid)
{
    /* Init SSL */
    SSL_CTX *ctx = ssl_init();
    SSL *ssl = SSL_new(ctx);
    char *bye = NULL;
    my_ssl_connect(ssl, ctx, fd);

    /* say hello */
    send_hello(ssl, nuid);

    /* receive status and solve puzzles */
    bye = receive_puzzle(ssl);

    // free SSL
    SSL_free(ssl);
    // release context
    SSL_CTX_free(ctx);
    return bye;
}

SSL_CTX* ssl_init()
{
    const SSL_METHOD *method = NULL;
    SSL_CTX *ssl_ctx = NULL;

    OpenSSL_add_ssl_algorithms();
    SSL_load_error_strings();
    method = SSLv23_client_method();

    ssl_ctx = SSL_CTX_new(method);
    if(ssl_ctx == NULL){
        die(MSG_ERROR_SSL_INIT, 0);
    }
    return ssl_ctx;
}

void set_fd_for_ssl(SSL *ssl, int id){
    int check = SSL_set_fd(ssl, id);
    if(check == 0){
        // print error
        die(MSG_ERROR_SSL_INIT, 0);
    }
}

SSL * my_ssl_connect(SSL *ssl, SSL_CTX *ctx, int fd){
    set_fd_for_ssl(ssl, fd);
    if(ssl == NULL){
        die(MSG_ERROR_SSL_CONNECT, 0);
    }
    int ssl_connect_check =	SSL_connect(ssl);
    if(ssl_connect_check == -1|| ssl_connect_check == 0){

        int error =	SSL_get_error(ssl, ssl_connect_check);
        ERR_print_errors_fp(stderr);
        die(MSG_ERROR_SSL_CONNECT, 0);
    }
}

void send_hello(SSL *ssl, char *nuid){
    char *msg = "cs5700spring2014 HELLO ";
    int len_head = strlen(msg);
    int len_nuid = strlen(nuid);
    char *hello = (char *) malloc(len_head + len_nuid + (size_t) 1);
    strncpy(hello, msg, len_head);
    strncpy(hello + len_head, nuid, len_nuid);
    strcpy(hello + len_head + len_nuid, "\n");
    int ssl_write_check = SSL_write(ssl, hello, strlen(hello));
    free(hello);
}

char* receive_puzzle(SSL *ssl){

    int sent_len = 0, recv_len = 0;
    char status[RECVBUFSIZE];
    char *solution = NULL, *bye = NULL;

    memset(status, '\0', sizeof(status));

    // read the first message
    int len_read;
    if((len_read = SSL_read(ssl, status, sizeof(status))) <= 0){
        die("failed to receive the message from server", 0);
    }
    status[len_read] = '\0';
    assert_format(status, 0);

    while (strstr(status, "BYE\n") == NULL)
    {
        print("%s", status);
        assert_format(status, 0);

        solution = resolve(status);
        sent_len = (int) strlen(solution);
        print("%s", solution);

        if (SSL_write(ssl, solution, sent_len) != sent_len)
            die("Failed to senf the solution message to the server", 0);

        free(solution);

        if ((recv_len = SSL_read(ssl, status, RECVBUFSIZE - 1)) <= 0)
            die("Failed to receive the message from server", 0);
        status[recv_len] = '\0';
    }

    assert_format(status, 1);
    bye = strdup(status);

    return bye;
}

