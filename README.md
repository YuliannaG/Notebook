To instal this bot you have to download this repositiry and in folder with file "setup.py" open terminal and type "pip install -e .".

This bot has 3 functions:
1. Addressbook - with Addressbook you can save such information as name, phone, date of bitrhday, email and address.
2. Notes - with Notes you can save notes and sort them by tags.
3. Sorter - with Sorter you can sort all your files in folder by types.

To activate one of functions press number or type full name of function. 

The following functions are available in the Addressbook:
"add contact [note name of contact] [phone number]" - create a new contact with one phone number, 
also you can add profile without phone number;
    *Name of contact shouldn`t consist of any spaces. If you want add contact with more than 1 
    word use _ except space.
    *This bot get phone number only in +38 format.
"add phone [name of contact] [phone number]" - you can add more than one phone number to contact;
"add bitrhday [name of contact] [date of bitrhday in format dd.mm.yyyy]" - you can add birthday 
to contact, to change contact birthday also use this command;
"add email [name of contact] [email in format johnsmith@gmail.com/.org/.edu]" - you can add 
email to contact, to change contact email also use this command;
"add home [name of contact] [home address]" - you can add home address to contact, to change 
contact home address also use this command;

"show all" - this comand show all profiles in database;
"show contact [name of contact]" - show contact profile;
"delete contact [name of contact]" - delete contact from datebase;
"delete phone [name of contact] [phone number]" - delete number from contacts profile;
"change phone [name of contact] [old phone number] [new phone number]" - change phone number which
 already in db into new;
        
"days to birthday [name of contact]" - this command shows how many days to birthday of contact;
"birthday after [number]" - this command shows who have birthday in number of days from tomorrow;

"good bye", "close", "exit" - back to main menu.


The following functions are available in the Notebook:
"add note [note text]" - create a new note with follow up tag request.
"delete note [number]" - delete note by the number from the previous search results 
 from show all or search function.
"help" - see all available commands.
"change note [number] [new note text]" - change note by the number from the previous search results 
 from show all or search function to new note. Tags change will follow.
"show all" - Show all notes records with tags.
"tags" - show all saved tags. 
"search note [text]" - Search notes and tags by text.
"search note by tag [text]" - Search tags only by text.
"sort notes" - Sort notes by tags.
"good bye", "close", "exit" - exit from the bot.
