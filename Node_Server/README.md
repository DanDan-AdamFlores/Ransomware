# RESTful API Service for use with the built Ransomware
## Table of Contents
1. [Server Requirements](#server_requirements)
2. [Node Requirements](#node_requirements)
3. [Guide](#guide)
4. [Authentication](#authentication)

<a name="server_requirements"></a>
## Server Requirements
1. Must already contain own set of private key and certificate file and modify index.js as necessary
2. Must provide own configuration folder to set up Mongo and JWT Signing
3. Preconfigure server to run on the ports specified inside index.js
	* iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080
	* iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 3000

<a name="node_requirements"></a>
## Node Project Requirements
1. [Node.js] Version 6.9.1+
2. [npm] Version 3.5.0+
3. [MongoDB] Version 3.2.10+

<a name="guide"></a>
## Guide
* Run a setup script that allows the user to create a password that is stored in MongoDB through BCrypt 
which is used for authentication

<a name="authentication"></a>
## Authentication
In order to retrieve the private key from the Server, the application must pass through two layers of authentication
1. The application must provide the proper "appKey" which restricts the access of applications trying to communicate with the server
2. The application must also provide the propper password in order to receive the private key as a response object

<a name="routes"></a>
# Routes

<a name="post-key"></a>
## Post a Key to the Server
* ROUTE: __POST__ https://api.domain.com/key
* Purpose: Store the received Keys and respond with an AppKey
* Required Parameters
	* Request Body
		* `privateKey`
			* Private Key Object from Python Hazmat Library
* Response
	* Response Body
		* `appKey`
			* The appKey generated server side that corresponds with a single run of the Ransomware application

<a name="get-key"></a>
## Retrieves a Key from the Server
* ROUTE: __GET__ https://api.domain.com/key
* Purpose: Respond with a Private Key object corresponding to the application instance
* Required Parameters
	* Request Header
		* `appKey`
			* JSON Web Token corresponding with a single run of the Ransomware application
	* Request Body
		* `password`
			* The password associated with the server
* Response
	* Response Body
		* `privateKey`
			* A private key object corresponding to the appKey received in the Header
