# Project 2

Web Programming with Python and JavaScript

All of the following pages extends the layout.html which contains code for a navbar and flask alerts which changes depending if you have login or not. If you have login you will be presented with a add channel page, a channel dropdown with all of the channels, and log out button on the navbar, but if you haven't login then you will have the log in option. (layout.html)

log_in.html and authorize.html contain the code to log in. You log in using a username you select a username. If you select the username admin you will be taken to the authorize page where you will have to type a password to continue using the admin account. (log_in.html and authorize.html)

create_channel.html shows an alert containing all people online and you are able to create a channel of your choosing in the textbox under the create channel title. (create_channel.html)

In the channel.html file contains the code for the textbox where all of the messages appear in real time. Along with the chat in real time the channel will send messages when some leaves and and enter. The chat will also show past messages from the channel so if you refresh the messages will stay. Furthermore if you are on the admin account you have the permission to send a message worldwide to every channel which will be stored worldwide. Also the admin has the ability to delete a channel removing all of its messages yet storing all of the worldwide messages.

channel.js contains all of the js code for channel.html. It emits a message contain the value of the input field which is then sent to the server to display in real time through rooms in broadcast. It also emit messages on join and leave of a channel. And it deletes channel by emitting messages also.
