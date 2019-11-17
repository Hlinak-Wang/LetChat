Encapsulation: Data structure
For iteration 2, our data was held in a nested dictionary and list structure. However, for iteration 3 we wanted to store our data structure in classes for the purpose of encapsulation.

We have multiple classes in separate files. In Data_class.py, we keep functions that interact with the data structure as a whole. Then, we have 3 other files for classes that encapsulate interactions with the specific aspects of the data structure, i.e. user, message and channel. For example, user_class.py has helper functions which create a user, login, logout and change user information, through accessing parts of the user data structure directly. This is a good use of the encapsulation design principle, as using the class structure restricts the accessing of the data structure within the routes and functions themselves.

DRY: Combining functions that have similar functionality
In iteration 2, one function holds only one responsibility, but there were other functions doing the same or similar things.
According to the software design theory DRY(don’t repeat yourself), we combined together functions which have similar functionality (using a parameter to distinguish). For example:
In the channel function, there are add owner and remove owner functions. These two take the same parameters and doing similar things, so we’ve merged them as one function and added one parameter ‘action’ to indicate whether the add owner command has been called or the remove owner one. It is the same for the channel join and leave functions.
Initially, in the Data_class.py file, there are a lot of repeat functions for getting a single item. E.g. get_u_id(), get_token(), get_name_first(), etc. Then we combined them all together as a single function called __getattribute__(self, item), which makes life easier to access one single item by using *.token, *.u_id, etc.
