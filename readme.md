# MTING

### Intro
This is some program that communicates with server with encrypted communication

### Structure
* Client: In charge of the user interaction
* Server: In charge of the DB, message handling
* Mtencrypt: Provides the encryption and decryption processes
* Network: Handling the communication processes
* Mtdb: Handling the server side and DB connection

### Notes
* The server takes not much measures for the malicious attack (malicious registering, sending), but respectively lightweight
* The encryption is based on 4096 bit RSA encryption, with the simple texts I think performance is reasonable fast so the AES is not used.
* The only "vulnerable" part in the program is the signing process of the RSA key, which will sign the public key pair with the username and password to a SHA256 hash. Other than that, all other processes are secure.
* Only some proto program with not sophisticated design, never use in production or bind the ports to public ip