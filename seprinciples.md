## Encapsulation: Data structure

For iteration 2, our data was held in a nested dictionary and list structure. However, for iteration 3 we wanted to store our data structure in classes for the purpose of encapsulation.

We have multiple classes in separate files. In ***Data_class.py***, we keep functions that interact with the data structure as a whole. Then, we have 3 other files for classes that encapsulate interactions with the specific aspects of the data structure, i.e. user, message and channel. For example, ***user_class.py*** has helper functions which create a user, login, logout and change user information, through accessing parts of the user data structure directly. This is a good use of the encapsulation design principle, as using the class structure restricts the accessing of the data structure within the routes and functions themselves.

# DRY: 
## Combining functions that have similar functionality

In iteration 2, one function holds only one responsibility, but there were other functions doing the same or similar things.
According to the software design theory **DRY**(don’t repeat yourself), we combined functions together which have similar functionality (using a parameter to distinguish). For example:
* In the channel function, there are add owner and remove owner functions. These two take the same parameters and doing similar things, so we’ve merged them as one function and added one parameter ‘action’ to indicate whether the add owner command has been called or the remove owner one. It is the same for the channel join and leave functions.
- Initially, in the ***Data_class.py*** file, there are a lot of repeat functions for getting a single item. E.g. **get_u_id()**, **get_token()**, **get_name_first()**, etc. Then we combined them all together as a single function called **__getattribute__(self, item)**, which makes life easier to access one single item by using *.token, *.u_id, etc.
- By the same reason, in the Data_class.py file, there are a lot of repeat functions for get user by something,  E.g. get_user_by_token(), get_user_by_u_id(), get_user_by_email(), etc. Then we combined them all together as a single function called __getuser__(self, key, value), it can identify the attribute it need to search and get the user, just put the token, u_id or something else in the key. It is much more easy to access and modify.
## Helper functions and decorators

Furthermore, we wrote more helper functions where we noticed that there was repetition of code logic. We also made a decorator in ***server.py*** in order to collect all of the arguments from the user. This aligns with the **DRY** software design theory as it limited the existence of the same or similar code in multiple places. Instead, a helper function or decorator allowed us to decrease the lines of code, increase the readability of our code and ensure that it is maintainable.

## KISS: Breaking big logic into smaller pieces

According to the software design theory **KISS** (keep it simple stupid), large logic pieces should be broken into smaller ones. We worked on **KISS** during iteration 3 by simplifying our code. This included the incorporation of the class data structures, the addition of single-responsibility helper functions, and by minimising repetition. Our aim was to ensure that if another human (such as another member of our group or a marker) was to read our code, it would be easy to follow and understand what it was trying to achieve.

## Single Responsibility Principle

Similar to KISS, we incorporated the **Single Responsibility Principle** by ensuring that complicated logic was broken down into smaller helper functions, which each only had one purpose. It ensures the readability and modularity of the code. For instance, check if a user is existed in the user list by using token or u_id.
