#include "common.h"

/** private functions */
int _compute(char *left, char *right, char operator);
int _is_number(char *maybe_number);
int _is_operator(char *maybe_operator);

int print(const char *format, ...)
{
    int done = 0;

    if (DEBUG)
    {
        va_list arg;
        va_start(arg, format);
        done = vfprintf(stdout, format, arg);
        va_end(arg);
    }

    return done;
}

void die(const char *err_msg, int usage)
{
    char *prog = "./client";
    fprintf(stderr, "Error: %s\n", err_msg);

    if (usage)
        fprintf(stderr, "Usage: %s <-p port> <-s> [hostname] [NEU ID]\n", prog);

    exit(1);
}

void parse_args(int argc, char **argv, int *p_flag, char **port,
        int *s_flag, char **host_name, char **neu_id)
{
    char *opt_string = "p:s";
    int index;
    char next_opt;

    /** check the arguments number */
    if ((argc < 3) || (argc > 6))
    {
        die("Wrong number of arguments", 1);
    }

    /** get available options and their arguments */
    while ((next_opt = getopt(argc, argv, opt_string)) != -1)
    {
        switch (next_opt)
        {
            case 'p':
                *p_flag = 1;
                *port = optarg;
                break;
            case 's':
                *s_flag = 1;
                break;
            case '?':
                die("Missing arguments", 1);
            default:
                break;
        }
    }

    /** check the remaining arguments and get them */
    if ((argc - optind) < 2) {
        die("Insufficient remaining arguments", 1);
    } else {
        *host_name = argv[optind];
        *neu_id = argv[optind + 1];
    }
}

struct sockaddr_in *init_server_addr(struct hostent *host_entry,
        unsigned short server_port)
{
    struct sockaddr_in *server_addr = (struct sockaddr_in *)
        malloc(sizeof(struct sockaddr_in));
    server_addr->sin_family = host_entry->h_addrtype;
    memcpy(&(server_addr->sin_addr.s_addr), host_entry->h_addr,
            host_entry->h_length);
    server_addr->sin_port = htons(server_port);
    return server_addr;
}

char* get_field(char *message, int index, const char *delim)
{
    int current_index = 0;
    char *copy = strdup(message);

    char *field = strtok(copy, delim);
    while (field != NULL)
    {
        if (current_index == index)
        {
            field = strdup(field);
            free(copy);
            return field;
        }

        field = strtok(NULL, delim);
        current_index++;
    }

    free(copy);
    return NULL;
}

void assert_format(char *message, int is_bye)
{
    char *field = NULL;
    if (message == NULL)
        die("Received NULL message", 0);

    // check MSG_HEADER for both messages
    field = get_field(message, 0, MSG_DELIM);
    if (field == NULL || strcmp(field, MSG_HEADER) != 0)
        die("Invalid MSG_HEADER field", 0);
    free(field);

    /** check the STATUS message format */
    if (!is_bye)
    {
        // check MSG_STATUS
        field = get_field(message, 1, MSG_DELIM);
        if (field == NULL || strcmp(field, MSG_STATUS) != 0)
            die("Invalid MSG_STATUS field", 0);
        free(field);
        // check left operant
        field = get_field(message, 2, MSG_DELIM);
        if (field == NULL || !_is_number(field))
            die("Invalid left operant", 0);
        free(field);
        // check operator
        field = get_field(message, 3, MSG_DELIM);
        if (field == NULL || !_is_operator(field))
            die("Invalid operator", 0);
        free(field);
        // check right operant
        field = get_field(message, 4, MSG_DELIM);
        if (field == NULL || !_is_number(field))
            die("Invalid right operant", 0);
        free(field);
    }
    /** check the bye message format */
    else
    {
        // check the secret_flag
        field = get_field(message, 1, MSG_DELIM);
        if (field == NULL || strlen(field) != LEN_SECRET_FLAG)
            if (strcmp(field, UNKNOWN_NUID) != 0)
                die("Invalid secret flag", 0);
        free(field);
        // check MSG_BYE
        field = get_field(message, 2, MSG_DELIM);
        if (field == NULL || strcmp(field, MSG_BYE) != 0)
            die("Invalid MSG_BYE", 0);
        free(field);
    }
}

char* resolve(char *status_msg)
{
    char *left_operant_str = NULL, *right_operant_str = NULL,
          *operator_str = NULL;
    char operator;
    int result = 0;
    char result_str[32];
    char *solution = NULL;
    int len_header = 0, len_result = 0;

    /** get the operants and operator */
    left_operant_str = get_field(status_msg, 2, MSG_DELIM);
    right_operant_str = get_field(status_msg, 4, MSG_DELIM);
    operator_str = get_field(status_msg, 3, MSG_DELIM);
    operator = operator_str[0];

    /** compute the result */
    result = _compute(left_operant_str, right_operant_str, operator);

    /** release the dynamically allocated memory made by strdup */
    free(left_operant_str);
    free(right_operant_str);
    free(operator_str);

    /** construct the string formatted result */
    sprintf(result_str, "%d", result);

    /** construct solution string */
    len_header = strlen(MSG_HEADER);
    len_result = strlen(result_str);
    solution = (char *) malloc(len_header + LEN_CHAR + len_result
            + LEN_CHAR + (size_t) 1);
    strncpy(solution, MSG_HEADER, len_header);
    strncpy(solution + len_header, SPACE, LEN_CHAR);
    strncpy(solution + len_header + LEN_CHAR, result_str, len_result);
    strcpy(solution + len_header + LEN_CHAR + len_result, RETURN);

    return solution;
}

/**
 * compute the numeric result of the given expression
 */
int _compute(char *left, char *right, char operator)
{
    int left_operant = atoi(left);
    int right_operant = atoi(right);
    int result = 0;

    switch(operator)
    {
        default:
            die("Invalid operator", 0);
        case '+':
            result = left_operant + right_operant;
            break;
        case '-':
            result = left_operant - right_operant;
            break;
        case '*':
            result = left_operant * right_operant;
            break;
        case '/':
            result = left_operant / right_operant;
            break;
    }

    return result;
}

/**
 * Return true if the given string is a number
 */
int _is_number(char *maybe_number)
{
    char *end_ptr = NULL;

    if (isspace(*maybe_number))
        return 0;
    else if (*maybe_number == '\0')
        return 0;
    else
        strtod(maybe_number, &end_ptr);

    if (*end_ptr == '\0')
        return 1;
    else
        return 0;
}

/**
 * Return true if the given string is an operator
 */
int _is_operator(char *maybe_operator)
{
    if (strlen(maybe_operator) != 1)
        return 0;

    char optr = maybe_operator[0];
    if (optr == '+' || optr == '-' \
            || optr == '*' || optr == '/')
        return 1;

    return 0;
}

