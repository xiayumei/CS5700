#include "generic.h"
#include "ssl.h"

int main(int argc, char **argv)
{
    /** variables holding parsed arguments */
    int p_flag = 0, s_flag = 0;
    char *server_port_string = NULL, *server_host_name = NULL,
         *neu_id = NULL;

    /** variables to be used in sokcet */
    int server_port;
    int client_socket;
    struct sockaddr_in *server_addr;
    struct hostent *host_entry;

    /** The receiving buffer pointer */
    char *first_status = NULL, *bye = NULL, *secret_flag = NULL;

    /** check and parse the command line arguments */
    parse_args(argc, argv, &p_flag, &server_port_string,
            &s_flag, &server_host_name, &neu_id);

    /** determine the port number */
    if (!p_flag)
        if (s_flag)
            server_port_string = SSL_PORT;
        else
            server_port_string = PORT;

    server_port = atoi(server_port_string);

    if ((host_entry = gethostbyname(server_host_name)) == NULL)
        die("Cannot find the host", 0);

    /** initialize the client socket */
    if ((client_socket = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        die("Failed to create a socket", 0);

    server_addr = init_server_addr(host_entry, server_port);

    /** connect to server */
    if (connect(client_socket, (struct sockaddr *) server_addr,
                sizeof(*server_addr)) < 0)
        die("Failed to connect to the server", 0);

    if (!s_flag)
    {
        /** send the HELLO message */
        first_status = say_hello(client_socket, neu_id);

        /** receive and resolve the first STATUS message */
        bye = solve(client_socket, first_status);

        /** only need to release it here since ssl does not use it */
        free(first_status);
    }
    else
    {
        /** directly get the BYE message to hold in the same SSL context */
        bye = ssl_part(client_socket, neu_id);
    }

    /** disconnect the socket first */
    close(client_socket);

    /** only print the secret flag */
    secret_flag = get_field(bye, 1, MSG_DELIM);
    fprintf(stdout, "%s\n", secret_flag);

    /** release all local dynamic memory */
    free(server_addr);
    free(secret_flag);
    free(bye);

    return 0;
}

