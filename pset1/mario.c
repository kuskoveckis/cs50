#include <cs50.h>
#include <stdio.h>

// This is Mario more comfortable version

int main(void)
{
    int height;
    //Prompt height
    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0 || height > 8);

    //Print pyramid blocks

    for (int i = 0; i < height; i++)
    {
        //Print left block
        for (int j = height - 1 ; j > i; j--)
        {
            printf(" ");
        }
        for (int x = 0; x <= i; x++)
        {
            printf("#");
        }

        //Print empty middle blocks
        for (int z = 0; z <= 1; z++)
        {
            printf(" ");
        }

        //Print right block

        for (int y = 0; y <= i; y++)
        {
            printf("#");
        }

        printf("\n");
    }
}