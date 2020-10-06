#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    // Prompt user's input
    float dollars;
    do
    {
        dollars = get_float("Change owed:");
    }
    while (dollars <= 0);

    // Convert floats to int
    int cents = round(dollars * 100);

    //Calculating number of coins
    int coins = 0;

    int quarters = 25;
    int dimes = 10;
    int nickels = 5;
    int cent = 1;

    while (cents >= quarters)
    {
        cents = cents - quarters;
        coins++;
    }
    while (cents >= dimes && cents < quarters)
    {
        cents = cents - dimes;
        coins++;
    }
    while (cents >= nickels && cents < dimes)
    {
        cents = cents - nickels;
        coins++;
    }
    while (cents >= cent && cents < nickels)
    {
        cents = cents - cent;
        coins++;
    }
    //Print result
    printf(" %i\n", coins);
}