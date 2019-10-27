##software verification and validation
User acceptance criteria is developed from user stories and requirements to ensure the system meets specifications and that it fulfills its intended purpose.

##acceptance criteria
#####As a slackr user, I want to send a message, so that I can share my thoughts with the other members of the channel.
- There will be a text field at the bottom once the user enters a channel.
- There will be a send button at the right of the text field once the user enters a channel.
- The text field contains a placeholder with a grey-colored text: “Send a message”.
- The placeholder moves to the top left corner of the text field once the user starts typing.
- The message is sent to the current channel once the user clicks the send button.
- The user can’t send a message with length over 1000 characters.

#####As a slackr user, I want to edit a message, so that I can keep my message up to date.
- There will be a button that has an image of a black-colored pen placed at the right of every message.
- Once the user clicks the black-colored pen, a pop-up which has a text field and two buttons will appear.
- The text field contains a placeholder with grey-colored text: “Enter to replace message”.
- The placeholder disappears once the user starts typing.
- One of the buttons contains a placeholder with a blue-colored text:”Confirm”. 
- The other button contains a placeholder with grey-colored text:”Cancel”.
- Once the user clicks the text “Confirm”, the pop-up will disappear and the text entered will replace the original text on the message which is associated with that edit button.
- Once the user clicks the button has a text “Cancel”, the pop-ups will disappear, and there will be no change in the text of the original message.
- The text used to replace the original text can’t be empty or more than 1000 characters.
- Only the user who sent the message or admin of slackr can edit the message.

As a slackr user, I want to delete a message, so that I can remove my message if it is no longer relevant.
- There will be a button with an image of a grey-colored garbage bin placed at the right of every message.
- Once the user clicks on that button, the message associated with that button will disappear.
- Only the user who sent the message or admin of slackr can delete the message.

#####As a channel owner, I want to Pin and unpin messages, so that the other members of the channel can be easily informed about important information and announcements.
- There will be a button has an image of a grey-colored thumbtack on the right of the message.
- Once the button is clicked, the image on the button will change to a black-coloured thumbtack.
- Once the button is clicked, the message will be moved to the top on the channel page.
- Once the message is pinned, the user can click on the button that has a black-colored thumbtack to unpin the message.
- The unpinned message will be removed from the top of channel page, but a user can still find it in the message field of the channel.

#####As a slackr user, I want to react and unreact to messages, so that others may know how I feel about certain messages.
- There will be a button that has an image of a black-colored thumbs up on the right of the message, and there will be a number on the bottom right corner of the figure.
- The number on the bottom right corner of the figure represent the number of user been react on this message.
- Once the button is clicked, the number on the bottom right corner of the figure increase by 1.
- One user can only react once for a message.
- If the user has already clicked on the thumbs up, the number on the bottom right corner will decrease by 1 if the user clicks again.

#####As a slackr user, I want to send a delayed message, so that I can prepare my messages in advance of when they need to be sent.
- A button has an image of a grey-colored clock placed on the bottom right corner.
- A pop-up with a text field and two buttons will appear.
- The text field at the centre of the pop-up contains a placeholder with a grey-colored text: “Enter a time to send”.
- The placeholder disappears once the user starts typing.
- One of the buttons at the bottom contains a placeholder with blue-colored text: “Cancel”.
- The other button at the bottom contains a placeholder with blue-colored text: “Set time”.
- Once the user clicks “Cancel”, the pop-up will disappear, and have no effect on the next message.
- Once the user clicks “Set time”, the pop-up will disappear, and the next message will be sent at the time the user entered.
- The message can’t send to the next day and to the past.
- The message will be sent at the time which was entered by user.

#####As a slackr user, I want to search for messages, so that I may find a particular message that I am looking for.
- The search field is placed on the top bar.
- The field contains a placeholder with a grey-colored text: “Message keyword”. 
- The placeholder disappears once the user starts typing. 
- Search starts once the user clicks “Search”, and the result of searching will appear in channel message field.

#####As a slackr admin, I want to Add other admins, so that others may also have administrative powers over my workspace. 
- A button at the top right corner of the home page contains a placeholder with a text “Admin”
- Once a user click on that button, a pop-up containing a text field and three buttons will appear.
- The text field contains a placehold with a text “Enter u_id”
- The placeholder will disappear once the user start typing.
- Three buttons contain  placeholders “Member”, “Adim”, and “Owner” repectively.
- Once the user clicks on one of these buttons, the pop-up will close, and the permission of the user (based on u_id) will be changed.
- Only the admin and owner can change a user’s permission.

#####As a slackr user, I want to be able to use standup to summarise a particular discussion, so that me and the other members of the channel can easily view the results and key points of the discussion.
- A button at the top right corner of channel page contains a placeholder with text “Standup”.
- Standup starts once the user clicks on that button.
- Once the standup starts, every message sent will go in to message-queue instead of directly send to the channel.
- Once the standup end, user who start standup will send all the messages in message-queue.
- Messages sent can’t be longer than 1000 characters

#####As a slackr user, I want my account to come with a profile page and a handle, so that other slack users can learn about me.
- There will be a Profile button at the left once the user login correctly.
- Profile details will show up in the main page once the user clicks the Profile button.
- There are four text boxes cotaining user’s 'first name', 'last name', 'email', and 'handle' with an edit button on the right.

#####As a slack user, I want to edit my profile, such as updating my email address, first name and last name, so that I can keep my profile up-to-date.
- There will be an edit button at the right of text box in the main page once the user clicks the Profile button.
- There will be a save button and a cancel button at the right of a text box on the main page once user clicks the edit button and user can rewrite the first name last name or email address.
- The user can’t set the First name or last name more than 50 character or 0.
- The user can’t set the email address to be a invalid email or email which it is already used by another user.

#####As a slack user, I want to view my handle name, so I can customising my slack handle and make it what I like.
- There will be an edit button at the right of the text box in the main page once the user clicks the Profile button.
- There will be a edit button at the right of the handle box in the main page once the user clicks the Profile button.
- There will be a save button and a cancel button at the right of text box in the main page once user click the edit button and user can modify the handle as they like.
- The user can’t set the handle more than 20 character or less than 3 character.
- The user can’t set the handle to be handle which it is already used by user.

#####As a slackr user, I want to register a slackr account using my email, so that I can easily track the slackr content that is relevant to me.
- There will be a button called ‘Don’t have an account? Register’ on the slackr website/app login page.
- When this button is pressed, the user is taken to a page with 4 blank boxes labelled ‘email’, ‘first name’, ‘last name’ and ‘password’.
- Once the user has entered these details, they can click the blue ‘sign up’ button.
- If the user enters a password with less than 6 characters long, an error message will appear to tell the user that this password is invalid and that they should enter a longer password.
- If the user enters an invalid email address, they will be told to enter a valid one.
- If the user enters an email address that already belongs to a registered user, they will be asked to enter an email address that does not already belong to a user.
- If the user leaves the first/last name box blank or enters a first/last name over 50 characters, they will be told that they should enter a valid first/last name.
- Once the user has entered their details correctly, they will have successfully created a new slackr account (and will be automatically logged in to their account).


#####As a slackr user, I want to be able to log in with my email and password, so that I can keep my account protected from others that may want to hack my account.
- On slackr’s login page, there will be two blank boxes labelled ‘email’ and password’.
- Once the user has entered these details, they can press the blue ‘sign in’ button.
- If the email that the user has entered is an invalid email address, there will be an error message telling the user to enter a valid email address.
- If the email entered does not belong to a user, they will be told that they should enter an email belonging to a registered slackr account.
- If the password entered does not match the email entered, the user will be told that their password is invalid.
- If the user has entered an email and password that match, they will be successfully logged in to their slackr account.


#####As a slackr user, I want to be able to log out of my account, so that other people that use the same device do not have access to it.
- There will be a ‘logout’ button in the top right-hand corner visible to a logged-in slackr user.
- If a user clicks on this button, they will be logged out of their account and redirected to the login page.


#####As a slackr user, I want to be able to reset my password using my email, so that I can recover my account in the case that I forget my password.
- On the slackr login page, underneath the ‘Don’t have an account? Register’ button there is a button underneath labelled ‘Forgot password?’.
- If the user clicks on this button, they will be taken to a page with a blank box labelled ‘email’.
- If the user enters an email address which is connected to a slackr account, they will be sent an email with a password reset code once they press the blue ‘send recovery email button’.
- The user can then click on a link sent with the recovery code which will direct them to a page where they can enter their code and a new password in two white boxes.
- The user can click the ‘reset password’ button, and their old password will be changed to the new password that they have entered.

#####As a slackr user, I want to create a new channel and give it a name, so that I can keep different discussion topics separate.
- On the left hand side of the slackr surface, there is a “+” sign besides “My Channel”, so the user could create a new channel by simply click on the “+” sign.
- After click on the “+” sign button, a message window will pop up and require you to enter the name of this new create channel.
- If the user enters a channel name longer than 20 characters, then an error message would pop up, and informs the user.
- After create a new channel, it will be placed under the ‘My Channel’ topic and has a hollow circle button, so the user can click on this button, and changes to the channel they want.

#####As a channel creator, I want to be able to set my channel to public or private, so that I can ensure that only the users that I allow access to the channel can view it.
- When creating a new channel, on the message window pop up, there is a switch button with ‘eye-open’ indicates public on the left and with ‘eye-closed’ indicates private on the right. The channel creator can choose whether public or private of the new create-channel.
- If the channel is private, other users rather than admin or the member inside the channel, cannot find the channel in the “Other Channel” list.
- If the channel is public, then all the slackr user can find this channel.

#####As a slackr user, I want to be able to view all of the channels I’m a part of, so that I can easily change between them to check if there are any new important messages.
- There is a “My Channel” list on the left hand side of the slackr surface, so the user can easily change to the channels they want
- There is also a number shows how many unread messages which sits above the channel name, so the user can easily check new messages received by visualising.
- A hollow circle button sits on the left hand side of a channel name, so the user can click on this button, and change to the channel they would like to share information with or read new messages.
- As a channel owner, I want to be able to add other channel owners, so that others can acquire ownership powers of my channel.
- There is a button with a shaded portrait, if the member is not an owner, then there is a backslash symbol above the shaded portrait, so the channel owner can easily click on that button to set a member to be the owner of this channel, and the backslash symbol will disappear.
- An owner of a particular channel will be placed at the to.p of the member list, so each member can easily find out who is/are the owner/s
- If the member is already an owner of this channel, then an error message would send to the channel owner, indicates that this member has acquired ownership of this channel.
- If the channel owner is not an owner of other channels that he/she is a member of, then set a member to an owner is impossible.

#####As a channel member, I want to be able to view information about the channel (such as its name, the other members of the channel, and the owner of the channel), so that I can learn who is receiving the message/s that I send on the channel.
- As the channel members click into the channel they are belonged to, they will see a list of members showing at the top of the surface of the messages. 
- There is a shaded portrait with a backslash or without it, to represent the ownership of a particular member.
- If a channel member is not a member of a certain channel, then he/she won’t be able to see the channel information and may also get an error message of trying to see the information of that channel.
- The name of each member would also show up, so every channel member can read each other’s name 

#####As a channel member, I want to be able to add other slackr users to a channel by searching for their name, so that I may easily add someone who is relevant to the channel discussion.
- There is a square button with the text “Invite”, so the channel member can add a new user to this channel.
- If the channel member is not a member of a certain channel, then he/she cannot add a user to that channel.
- Every member of the channel can add other slackr users to this channel.
- If the invite slackr users don’t exist, then an error message will pop up and shows to the member that the user id type in is invalid.
- As a slackr user, I want to be able to automatically join a public channel that I search for, or a private channel that I have been invited to, so that I can stay up-to-date with messages that are relevant to me.
- If the channel is public, then it will appear in the “Other Channel” list, so if a slackr user would like to join to it, just simply click on the channel name and a button with the text “Join” would appear at the right side of the channel list. 
- By clicking on the “Join” button, the slackr user becomes a member of that channel and can send messages.
- If the channel is private, the slackr user cannot find it, it can only be added to the channel through the invitation of the member inside that private channel.

#####As a channel member, I want to be able to leave a channel, so that I don’t receive messages that are no longer relevant to me.
- There is a button with the text “Leave”, so click on it, the channel member can quit this channel, and no longer receive the messages from this channel.
- The history messages received would also disappear.
- The channel that the user is quitted will also remove from the list of “My Channel”.
