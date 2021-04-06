# MTing Client

This is the GUI of MTing client, with it you can register and send message, fetch your message to other users.

### Prereq
Install all dependencies by
`pip install -r .\requirements.txt`

### Input box:
* Username: User id
* Password: Where to input the password
* Sevrer Addr: The ip address of the server for MTing server
* Send: First box is for the message, second box is for the uid to send to

### Button:
* Connect: You will exchange your signed RSA public key with the server
* Fetch: You will fetch all the message sent to you
* Clear: You will delete all the messages in the server database, can't be undone.
* Register: Regester the user and password to server(if username is not in the db)
* Exit: Quit the program

