SQL Databes:

Table users:
# Query used to create this table
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, savings NUMERIC NOT NULL, 'city' text)

Table income:
# Query used to create this table
CREATE TABLE 'income' (user_id INTEGER, amount NUMERIC NOT NULL, budget_nr INTEGER NOT NULL, 'date' text NOT NULL , 'description' text NOT NULL )

Table expense:
# Query used to create this table
CREATE TABLE 'expense' (user_id INTEGER, categorie TEXT NOT NULL, amount NUMERIC NOT NULL, budget_nr INTEGER NOT NULL, 'date' text NOT NULL )
