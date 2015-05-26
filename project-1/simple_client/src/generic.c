#include "generic.h"

char* say_hello(int client_socket, char *neu_id)
{
    int sent_len = 0, recv_len = 0;
    char *status = (char *) malloc(RECVBUFSIZE * sizeof(char));
    int len_header = 0, len_hello = 0, len_neu_id = 0;

    /** construct hello message */
    len_header = strlen(MSG_HEADER);
    len_hello = strlen(MSG_HELLO);
    len_neu_id = strlen(neu_id);

    char *hello = (char *) malloc(len_header + LEN_CHAR + len_hello
            + LEN_CHAR + len_neu_id + (size_t) 1);

    /** dirty copy */
    strncpy(hello, MSG_HEADER, len_header);
    strncpy(hello + len_header, SPACE, LEN_CHAR);
    strncpy(hello + len_header + LEN_CHAR, MSG_HELLO, len_hello);
    strncpy(hello + len_header + LEN_CHAR + len_hello, SPACE, LEN_CHAR);
    strncpy(hello + len_header + LEN_CHAR + len_hello + LEN_CHAR, neu_id, len_neu_id);
    strcpy(hello + len_header + LEN_CHAR + len_hello + LEN_CHAR + len_neu_id, RETURN);
    sent_len = (int) strlen(hello);

    /** send the hello message */
    if (send(client_socket, hello, sent_len, 0) != sent_len)
        die("Failed to send the hello message to the server", 0);

    /** receive first status message */
    if ((recv_len = recv(client_socket, status, RECVBUFSIZE - 1, 0)) <= 0)
        die("Failed to receive the message from server", 0);

    status[recv_len] = '\0';

    /** release the hello memory space */
    free(hello);

    return status;
}

char* solve(int client_socket, char *first_status)
{
    int sent_len = 0, recv_len = 0;
    char status[RECVBUFSIZE];
    char *solution = NULL, *bye = NULL;

    /** initialize the status buffer */
    memset(status, '\0', sizeof(status));
    strcpy(status, first_status);
    assert_format(status, 0);

    while (strstr(status, "BYE\n") == NULL)
    {
        /** assert the STATUS message format to be correct */
        assert_format(status, 0);

        /** resolve the challenge */
        print("%s", status);
        solution = resolve(status);
        print("%s", solution);

        /** send the solution */
        sent_len = (int) strlen(solution);
        if (send(client_socket, solution, sent_len, 0) != sent_len)
            die("Failed to senf the solution message to the server", 0);

        /** release the memory of the last solution space */
        free(solution);

        /** receive next challenge */
        if ((recv_len = recv(client_socket, status, RECVBUFSIZE - 1, 0)) <= 0)
            die("Failed to receive the message from server", 0);
        status[recv_len] = '\0';
    }

    /** assert the BYE message format to be correct */
    assert_format(status, 1);
    bye = strdup(status);

    return bye;
}

