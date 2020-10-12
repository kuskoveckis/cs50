// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Word count variable;
int word_count = 0;


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int hash_number = hash(word);
    node *cursor = table[hash_number];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // hash function taken from cs50 study webpage (https://study.cs50.net/hashtables) and modified to suite pset5 task needs
    int hash = 0;

    for (int i = 0; word[i] != '\0'; i++)
    {
        hash += tolower(word[i]);
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // variables
    char d_word[LENGTH + 1];  // dictionary word

    // Open dicitionary
    FILE *dict = fopen(dictionary, "r");
    // check if dictionary can't be opened for reading
    if (dict == NULL)
    {
        return false;
    }
    // assign NULL to array table buckets
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    // read strings from dictionary while eof not reached
    while(fscanf(dict, "%s\n", d_word) != EOF)
    {
        //create a new node and allocate memory.
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            word_count = 0;
            return false;
        }
        // copy word into node
        strcpy(n->word, d_word);

        int hash_value; // dictionary's word hash value

        // hash word to obtain a hash value
        hash_value = hash(n->word);
        // insert node into hash table
        if (table[hash_value] == NULL)
        {
            n->next = NULL;
            table[hash_value] = n;
            word_count++;
        }
        else
        {
            n->next = table[hash_value];
            table[hash_value] = n;
            word_count++;
        }
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        table[i] = NULL;
    }

    return true;
}