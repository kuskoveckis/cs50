#include <cs50.h>
#include <string.h>
#include <math.h>
#include <stdio.h>
#include <ctype.h>


int main(void)
{
    string text = get_string("Text: ");

    int letters = 0;
    int words = 1;
    int sentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // Count number of letters
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            letters++;
        }
        else if (text[i] >= 'A' && text[i] <= 'Z')
        {
            letters++;
        }
        // Count number of words
        if (isspace(text[i]))
        {
            words++;
        }
        // Count sentences
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }

    // Calculate index number

    float index = 0.0588 * (100 * (float) letters / (float) words) - 0.296 * (100 * (float) sentences / (float) words) - 15.8;

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index > 1 && index < 16)
    {
        printf("Grade %i\n", (int)round(index));
    }
    else
    {
        printf("Before Grade 1\n");
    }

}


