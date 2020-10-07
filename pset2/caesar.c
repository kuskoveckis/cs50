#include <cs50.h>
#include <string.h>
#include <math.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // Check for number of arguments
    if (argc < 2 || argc > 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (argc == 2)
    {
        int k = atoi(argv[1]);
        // Loop through argment's characters
        for (int x = 0; x < strlen(argv[1]); x++)
        {
            // Check if all characters are digits
            if (strspn(argv[1], "0123456789") == strlen(argv[1]))
            {
                string plaintext = get_string("plaintext: ");
                printf("ciphertext: ");
                // Convert input chracters to cipher characters
                for (int i = 0; i < strlen(plaintext); i++)
                {
                    if (plaintext[i] >= 'a' && plaintext[i] <= 'z')
                    {
                        printf("%c", (plaintext[i] - 'a' + k) % 26 + 'a');
                    }
                    else if (plaintext[i] >= 'A' && plaintext[i] <= 'Z')
                    {
                        printf("%c", (plaintext[i] - 'A' + k) % 26 + 'A');
                    }
                    else
                    {
                        printf("%c", plaintext[i]);
                    }
                }
                printf("\n");
                return 0;
            }
            else
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }

}