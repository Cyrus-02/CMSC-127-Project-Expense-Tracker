from pyfiglet import Figlet
from api import MariaDBAPI


def runApp():
    global api
    api = MariaDBAPI()
    showSignInSignUp()


def showSignInSignUp():
    while 1:
        print("\n==================")
        print("[1] Sign In")
        print("[2] Sign Up")
        print("[0] Exit")
        choice = input("Choice: ")
        if choice == "1":
            choice = showSignIn()
        elif choice == "2":
            showSignUp()
        elif choice == "0":
            break
        else:
            print("Wrong input!")
        if choice == "0":
            break


def showSignIn():
    global myusername
    print("\n=======SIGN-IN=======")
    myusername = input("Username: ")
    res = api.signIn(myusername)
    choice = None
    if (res):
        print("Signed In!")
        choice = showMainMenu()
    else:
        print("Wrong Username!")
    if choice == "0":
        return "0"


def showSignUp():
    print("\n=======SIGN-UP=======")
    email = input("Email: ")
    username = input("Username: ")
    # res = api.signUpEmail(email)
    res = api.signUp(username, email)
    if (res):
        print("Signed Up!")
    else:
        print("Username already taken!")


def showMainMenu():
    while 1:
        print("\n=======MAIN-MENU=======")
        print("[1] Expenses")
        print("[2] Friends")
        print("[3] Groups")
        print("[9] Sign Out")
        print("[0] Exit")
        choice = input("Choice: ")
        if choice == "1":
            showExpensesMenu()
        elif choice == "2":
            showFriendMenu()
        elif choice == "3":
            showGroupMenu()
        elif choice == "9":
            break
        elif choice == "0":
            return "0"
        else:
            print("Wrong Input!")


def showExpensesMenu():
    while 1:
        print("\n=======EXPENSE-SUMMARY=======")
        lent_money = api.cumulativeOwe()
        debt = api.cumulativeDebt()
        print(f"\nCumulatively, you are owed P{lent_money}!")
        print(f"You also have an overall debt of P{debt}.\n")
        print("[1] Owed Money with Groups ")
        print("[2] Owed Money by Friends")
        print("[3] Expenses within a month")
        print("[4] Search Expense by Name")
        print("[0] Back")
        choice = input("Choice: ")
        if choice == "1":
            showGroupDebts()
        elif choice == "2":
            showFriendDebts()
        elif choice == "3":
            showExpenseWithinMonth()
        elif choice == "4":
            searchForExpense()
        elif choice == "0":
            break
        else:
            print("Wrong Input!")


def showGroupDebts():
    while 1:
        res = api.getGroupDebts()
        if res == -1:
            print("No groups found!")
            input("\nPress ENTER to continue")
            break

        print("\n=======MY-GROUPS=======")
        for row in res:
            print("["+str(row[0]).zfill(4)+"] " +
                  row[1] + " [P"+str(row[2]) + "] ")
        input("\nPress ENTER to continue")
        break


def showFriendDebts():
    while 1:
        res = api.getFriendDebts()
        if res == -1:
            print("No friends found!")
            input("\nPress ENTER to continue")
            break

        print("\n=======MY-FRIENDS=======")
        for row in res:
            print("["+str(row[0]).zfill(4)+"] " +
                  row[1] + " [P"+str(row[2]) + "] ")
        input("\nPress ENTER to continue")
        break


def showExpenseWithinMonth():
    while 1:
        res = api.getExpenseWithinMonth()
        if len(res) == 0:
            print("No expenses found!")
            input("\nPress ENTER to continue")
            break

        print("\n=======EXPENSES-WITHIN-A-MONTH=======")
        for row in res:
            print(
                f"Paid P{row[1]} under Group {row[2]} paying the expense {row[0]} on {row[3]}")
        input("\nPress ENTER to continue")
        break


def searchForExpense():
    print("Search an expense by inputting the expense name.")
    expensename = input("Expense Name: ")
    res = api.getExpenseByName(expensename)
    while 1:
        print("\n=========SEARCHED-EXPENSES==========")
        if len(res) == 0:
            print("No expenses found!")

        else:
            print("Expense/s found:")
            for row in res:
                print(
                    f"Expense {row[0]} has a bill of {row[1]}: Created on {row[2]}")
            input("Press ENTER to continue.")
            break


def showGroupMenu():
    while 1:
        print("\n=======GROUPS=======")
        print("[1] My Groups")
        print("[2] Search Groups")
        print("[3] Create a Group")
        print("[4] Delete a Group")
        print("[0] Back")
        choice = input("Choice: ")
        if choice == "1":
            showMyGroups()
        elif choice == "2":
            searchForGroup()
        elif choice == "3":
            showCreateGroup()
        elif choice == "4":
            showDeleteGroup()
        elif choice == "0":
            break
        else:
            print("Wrong Input!")


def searchForGroup():
    print("Search a group you belong to by inputting its groupname.")
    groupname = input("Groupname: ")
    res = api.getGroupbySearch(groupname)
    print("\n=========SEARCHED-GROUPS==========")
    if len(res) == 0:
        print("No groups found!")

    else:
        print("Group/s found:")
        for row in res:
            print(f"{str(row[0]).zfill(4)}: {row[1]}")


def showMyGroups():
    while 1:
        res = api.getMyGroups()
        if len(res) == 0:
            print("No groups found!")
            input("\nPress ENTER to continue")
            break

        print("\n=======MY-GROUPS=======")
        groupids = []
        for row in res:
            print("["+str(row[0]).zfill(4)+"] "+row[1])
            groupids.append(str(row[0]).zfill(4))
        print("\n[0] Back ")
        choice = input("\nChoice: ")
        if (choice in groupids):
            showGroup(choice)
        elif choice == "0":
            break
        else:
            print("Wrong Input!")


def showGroup(groupid):
    while 1:
        res = api.getGroupName(groupid)
        print("\n======="+res[0][0]+"=======")
        res = api.getDebtsInGroup(groupid)
        print("Members:")
        for member in res:
            if member[2].lower() == myusername.lower():
                print("  "+member[2]+" (You)")
            elif member[1] < 0:
                print("  "+member[2]+" (You owe "+str(member[1]*-1)+")")
            elif member[1] > 0:
                print("  "+member[2]+" (Owes you "+str(member[1])+")")
            else:
                print("  "+member[2])

        print("\n[1] Add a member")
        print("[2] Add an expense")
        print("[3] Delete an expense")
        print("[4] Pay a member")
        print("[5] Expenses")
        print("[0] Back")
        choice = input("\nChoice: ")
        if choice == "1":
            showAddMember(groupid)
        elif choice == "2":
            showAddExpense(groupid)
        elif choice == "3":
            showDeleteExpense(groupid)
        elif choice == "4":
            showPayMember(groupid)
        elif choice == "5":
            showGroupExpenses(groupid)
        elif choice == "0":
            break
        else:
            print("Wrong Input")


def showGroupExpenses(groupid):
    res = api.getGroupExpenses(groupid)
    print("\n=======EXPENSES=======")
    total = 0
    if len(res) == 0:
        print("There are no expenses in this group!")
    else:
        for expense in res:
            print("P"+str(expense[1])+"\t"+expense[0]+" ("+expense[2]+")")
            total += expense[1]
        print("\nTotal: P"+str(total))
    input("\nPress ENTER to continue.")


def showPayMember(groupid):
    print("\n=======PAY=======")
    res = api.getDebtsInGroup(groupid)
    hasdebt = False

    print("Members you owe to:")
    for member in res:
        if member[1] < 0 and member[2].lower() != myusername.lower():
            print("  "+member[2]+" (You owe "+str(member[1]*-1)+")")
            hasdebt = True
    if hasdebt:
        username = input("\nUsername: ")
        amount = input("Amount: ")
        res = api.payMemberInGroup(amount, groupid, username)
        print(res)

    else:
        print("You do not owe to any member to this group!")
        input("\nPress ENTER to continue.")


def showAddExpense(groupid):
    print("\n=======ADD-AN-EXPENSE=======")
    expensename = input("Expense Name: ")
    amount = int(input("Amount: "))
    date = input("Date (Month DD, YYYY): ")
    api.createExpense(expensename, amount, groupid, date)


def showDeleteExpense(groupid):
    print("\n=====DELETE-AN-EXPENSE======")
    expensename = input("Expense Name: ")
    api.deleteGroupExpense(expensename, groupid)


def showAddMember(groupid):
    res = api.friendsNotInGroup(groupid)
    print("\n=======ADD-A-MEMBER=======")
    print("Friends:")
    if len(res) == 0:
        print("All of your friends are in this group!")
        input("\nPress ENTER to continue.")
    else:
        for friend in res:
            print("  "+friend[0])
        username = input("\nUsername: ")
        status = api.addFriendToGroup(username, groupid)
        if status:
            print(f"Successfully added {username}!")
        else:
            print("Friend not found!")


def showCreateGroup():
    print("\n=======CREATE-A-GROUP=======")
    groupname = input("Group Name: ")
    res = api.createGroup(groupname)
    if res:
        print("Successfully created "+groupname+" group!")
    else:
        print("Error creating "+groupname+" group!")


def showDeleteGroup():
    while 1:
        res = api.getMyGroups()
        if len(res) == 0:
            print("There are no groups to delete!")
            input("\nPress ENTER to continue")
            break

        print("\n=======DELETE-GROUP=======")
        groupids = []
        for row in res:
            print("["+str(row[0]).zfill(4)+"] "+row[1])
            groupids.append(str(row[0]).zfill(4))
        print("\n[0] Back ")
        choice = input("\nChoice: ")
        if (choice in groupids):
            status = api.deleteGroup(choice)
            if status:
                print(f"Deleted group with id: {choice}")
            else:
                print("Group not found!")
        elif choice == "0":
            break
        else:
            print("Wrong Input!")


def showFriendMenu():
    while 1:
        print("\n=======FRIENDS=======")
        print("[1] My Friends")
        print("[2] Search a friend")
        print("[3] Show Friend Requests")
        print("[4] Add friend")
        print("[5] Delete friend")
        print("[0] Back")
        choice = input("Choice: ")
        if choice == "1":
            showMyFriends()
            break
        elif choice == "2":
            searchForFriend()
        elif choice == "3":
            showFriendRequests()
            break
        elif choice == "4":
            username = input("Enter username: ")
            showAddFriend(username)
            break
        elif choice == "5":
            showDeleteFriend()
            break
        elif choice == "0":
            break
        else:
            print("Wrong Input!")


def searchForFriend():
    print("Search a friend by inputting his/her groupname.")
    username = input("Friend Name: ")
    res = api.getFriendbySearch(username)
    print("\n=========SEARCHED-FRIENDS==========")
    if len(res) == 0:
        print("No friends found!")

    else:
        print("Friend/s found:")
        for row in res:
            print(f"[{str(row[0]).zfill(4)}]: {str(row[1])} - {str(row[2])}")


def showMyFriends():
    while 1:
        res = api.getFriends()
        if len(res) == 0:
            print("You have no friends!")
            input("\nPress ENTER to continue")
            break

        print("\n=======MY-FRIENDS=======")
        friendids = []
        for row in res:
            print(f"[{str(row[0]).zfill(4)}]: {row[1]} - {row[2]}")
            friendids.append(str(row[0]).zfill(4))
        print("\n[0] Back ")
        choice = input("\nChoice: ")
        if (choice in friendids):
            showFriend(choice)
        elif choice == "0":
            break
        else:
            print("Wrong Input!")


def showFriend(friendid):
    res = api.getFriend(friendid)
    if len(res) == 0:
        print("No expenses to show!")
        input("Press ENTER to continue")

    print("\n=======EXPENSE-WITH-FRIEND=======")
    for row in res:
        print(f"> Agreed to split bills for {row[0]} on {row[1]}")


def showFriendRequests():
    while 1:
        res = api.getFriendRequests()
        if len(res) == 0:
            print("You have no pending friend requests")
            input("\nPress ENTER to continue")
            break
        print("\n=======FRIEND-REQUESTS=======")
        frusernames = []
        for row in res:
            print("["+str(row[0]).zfill(4)+"] "+row[1])
            frusernames.append(row[1])
        print("\n[0] Back ")
        choice = input("\nAdd by username: ")
        if (choice in frusernames):
            showAddFriend(choice)
        elif choice == "0":
            break
        else:
            print("User not found!")


def showAddFriend(username):
    res = api.addFriend(username)
    if res:
        print(f"Successfully added {username}")
    else:
        print("Username not found!")


def showDeleteFriend():
    while 1:
        res = api.getFriends()
        if len(res) == 0:
            print("You have no friends!")
            input("\nPress ENTER to continue.")
            break

        print("\n=======MY-FRIENDS=======")
        frusernames = []
        for row in res:
            print("["+str(row[0]).zfill(4)+"] "+row[1])
            frusernames.append(row[1])
        print("\n[0] Back ")
        choice = input("Delete by username: ")
        if choice in frusernames:
            status = api.deleteFriend(choice)
            if status:
                print(f"Removed {choice} as friend.")
            else:
                print("Friend not found!")
        elif choice == "0":
            break
        else:
            print("Friend not found!")


f = Figlet(font="slant")
print(f.renderText("Expense Tracker"))

runApp()


# print(api.signIn("jerico"))
# print(api.addFriendToGroup("jane",2))
# print(api.signIn("jane"))
# print(api.getFriendRequests())
# print(api.acceptFriendRequest("jerico"))
# print(api.getFriends())
# print(api.getMyGroups())
# print(api.createGroup("nagits"))
# print(api.signIn("jerico"))
# print(api.getFriends())
# print(api.getFriendRequests())
# print(api.createGroup("Era"))
# print(api.getMyGroups())
# print(api.signUp("jane"))
# print(api.signIn("jerico"))
# print(api.createGroup("KDA"))
# print(api.signUp("Era"))
# print(api.addFriend("jane"))


# print(api.signUp("jerico"))
# print(api.signUp("jane"))
# print(api.signIn("jerico"))
# print(api.addFriend("jane"))
# print(api.signIn("jane"))
# print(api.createGroup("nagits"))
# print(api.getMyGroups())
# print(api.getFriends())
# print(api.getFriendRequests())
# print(api.acceptFriendRequest("jane"))
# print(api.getFriendRequests())
# print(api.getFriends())
# print(api.signup("jane"))
# print(api.test())
# print(api.userid)
# print(api.userid)
# print(api.signup("jerico"))
# print(api.userid)
