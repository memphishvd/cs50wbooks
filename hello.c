#include <cs50.h>
#include <stdio.h>

int main(void)

{
    // Asking for user input i.e. name
    string name = get_string("What is your name?\n");
    // Printing hello combined with user's name
    printf("hello, %s\n", name);
}
