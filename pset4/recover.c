#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    int counter = 0;
    //Buffer memory
    BYTE buffer[512];
    //New JPEG file
    FILE *img = NULL;
    // boolean statement for the first JPEG
    bool first_jpeg = false;

    // check for command-line argument
    if (argc > 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open memory card
    FILE *file = fopen(argv[1], "r");
    // check if image/card can't be opened for reading
    if (file == NULL)
    {
        printf("File can't be opened for reading\n");
        return 1;
    }

    // Repeat until end of card
    // Read card/image
    while (fread(buffer, 512, 1, file))
    {
        // Check buffer if it starts with a JPEG header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (!first_jpeg)
            {
                first_jpeg = true;
            }
            else
            {
                // Close jpeg file
                fclose(img);
            }

            // Create new JPEG file
            char filename[8];
            sprintf(filename, "%03i.jpg", counter ++);
            img = fopen(filename, "w");
            // Write to new JPEG file
            fwrite(buffer, 512, 1, img);
        }
        else if (first_jpeg)
        {
            // Continue writing to the current  JPEG file
            fwrite(buffer, 512, 1, img);
        }
        // Check if end of file is reached
        if (feof(file))
        {
            break;
        }

    }
    // Close file
    fclose(img);
    fclose(file);
}
