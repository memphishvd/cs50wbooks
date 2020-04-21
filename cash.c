#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
//declare variables
    float amount;
    int cents;
    int quarter;
    int dime;
    int nickel;
    int penny;
    int finaltally = 0;   
//loop to check if input amount is positive
    do  
    {
        amount = get_float("What is the amount of change owed in Dollars?\n");
    }
    while (amount < 0);    
// convert amount to cents
    cents = round(amount * 100);
// check if cents value is greater than a quarter and process accordingly
    for (quarter = 1; cents >= 25; quarter++)
    {
// if cents value is more than 25 then subtract 25, add 1 to finaltally and repeat above condition
        cents -= 25;
        finaltally += 1;
    }
// if cents value is more than 10 then subtract 10, add 1 to finaltally and repeat above condition
    for (dime = 1; cents >= 10; dime++)
    {
        cents -= 10;
        finaltally += 1;
    } 
// if cents value is more than 5 then subtract 5, add 1 to finaltally and repeat above condition
    for (nickel = 1; cents >= 5; nickel++)
    {
        cents -= 5;
        finaltally += 1;
    }
// if cents value is more than 5 then subtract 5, add 1 to finaltally and repeat above condition
    for (penny = 1; cents >= 1; penny++)
    {
        cents -= 1;
        finaltally += 1;
    }
// Print final tally
    printf("%i\n", finaltally);   
}
