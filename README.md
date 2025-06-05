# Expense Tracker 

## CMSC 127 S4L Group 2 Members
- Barilea, Cyrus Jade 
- Joyosa, Jenzzo  
- Luñeza, Marcel Luiz G.  
- Sabile, Jerico  


## Program Description 
#### Project Title
Expense Tracker

### Terms to Know
#### Users
Users of the app refers to accounts that have been signed in in the program.

#### Friend
Users can initiate a friend request by searching for other users' usernames.

#### Group
Groups are collection of users that presumably agreed to "split" the bill
of their expense.

#### Expense
An expense refers to an entry or payment done by a group. This will be divided
evenly among the users inside the group whereas the only one not paying was the 
user that initially (and fully) paid their bill.


## Project Rundown
Expense Tracker is a terminal-based program created using Python and MariaDB that stores 
user data regarding money lending or payment splitting.

The program:
   * lets users add other users as friend
   * lets users add, update and delete groups 
   * lets users add and update expenses within the group
   * keeps track of individual outstanding balances

## Installation Guide
1. Download or clone the repository.
2. Download the necessary python packages by running ```pip install mariadb``` and ```pip install pyfiglet```.
3. Move the ```expensetracker.sql``` file into your MariaDB directory.
4. Unpack the sql file to set up the database.
5. Make sure to change the ```user``` and ```password``` in the connect function in ```api.py```
to mirror your personal MariaDB environment.
6. Run the command ```python project.py```.

## How To Use Expense Tracker
1. An authentication page will pop-up as soon as you run the program. All users are required to sign up first 
before using the program. Sign-ins are done through usernames. No password is required

2. After signing in, users will be met by menu: with options Friends, Groups, Sign Out and Exit (program).

3. Users can view their friend list, view their friend requests, add and delete friends in the Friends menu.
This requires a username to be inputted. The user must know the username of his/her friend.

4. Groups can be created, viewed, modified and deleted. 
    * Creating a group requires a group name.
    * Modifying and deleting a group needs a group ID.
    * In viewing of the user's belonging groups, he/she can input the Group ID to open up the console, editing
    the Group. Here, the user can add a member (should be a friend), add or pay an expense and view the total
    expense done within the Group.
