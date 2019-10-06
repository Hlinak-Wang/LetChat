ASSUMPTIONS

Assumptions about user stories:

-Assumed that UNSW's version of slackr would be quite similar to the real slack in terms of its functionality, and possibly its interface.

-Assumed that the features mentioned in Hayden's "Stakeholder requirements interview" video are a good overview of the requirements of UNSW's Slackr (and that UNSW has a good understanding of what the customers want).

-Assumed that the user stories written include almost all of the possible user stories for creating Slackr.

Assumptions about plan:

-We should plan iteration 1 and iteration 2, decide the order of implementing the functions and the roles of each member of the group.

-We also assume that we should include a diagram to show the timeline week per week (and also that we have 3 weeks to finish this iteration).

-Assumed that we would keep up the motivation and continue to work well as a term throughout the duration of the project (i.e. not leave it all to the last moment).

Assumptions about functions:

-The first user registered using "auth_register()" is assumed to be the admin of slackr.

-"auth_passwordreset_request" will get a reset code from registered email and use "auth_passwordreset_reset" to check all the information is valid to reset password.

-The user creating a channel using channel_create is assumed to be the owner of that channel.

-"channels_listall" will provide a list of channels which are not private.

-"channel_messages" can be used to get the newest message from a channel.

-"channel_invite" can invite user to a channel if you are already in there, and "channel_addowner" or "channel_removeowner" can manage the rights of users.

-When the user wants to send a message to a certain channel using "message_send" or "message_sendlater", assume that the user is already in that channel.

-When calling "message_edit()", assume the message used to replace the original message is no more than 1000 characters.

-Assume the valid range of "react_id" in "message_react()" and "message_unreact()" is between 0 to 100.

-Assume the "user_profile()" will return a handle of the form firstname and lastname (combined in lower case) if the handle hasn't been changed by the user yet.
