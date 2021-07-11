# **Badili** 
 >> *Borderless payments, simplified*

Blockchain technology has the ability to solve many problems faced in Africa. The problem is, for the majority, it's such a hussle to get started. There is a huge learning curve understanding all the bells and whistles. This makes it difficult for the adoption of most products widely accepted globally. Badili sets out to make it easy for the average person in Afica to participate in the blockchain revolution. 

```Badili is a USSD based blockchain wallet that makes it simple for anyone on the African continent to send, receive and hold any financial assets from any part of the world, right on their phones. Feature phone or smartphone.```
    
:point_up: 1 more thing...

Just like mobile banking solutions like MPESA that have achieved massive scale. The secret is in opening up the API's to developers to build on top of. We provide interfaces to augment other blockchain services, maintaining the simplicity and ease of use for the normal user.

## Features of Badili
Let's say Bob from a rural village in Kenya wants to receive money from Alice based in USA. 
All he has to do is:

    1. Register for a Badili account.
    2. Share his mobile number he used with Alice.
    3. Choose the currencies he would like to hold on his account.
    4. Wait for Alice to send the money, which he receives instantly.
    

Let's say now Bob needs to send some upkeep money to his kid studying in Rwanda, how does he do it?
He needs to:

    1. Deposit money to his local mobile money account and transfer to his Badili account.
    2. Ask his kid to sign up Badili
    3. Send money to his kid who receives it immediately.
    
What if Bob wants to buy an NFT on Litemint (or just anything), what does he do?

    1. Get the Litemint address/account he needs to pay to.
    2. Send money (in whatever currency) to that address/account.
    3. Done! (He can verify he owns the NFT on Litemint)
    
What if now Bob needs some liquid cash, how does he withdraw from his wallet?

    1. Go to the USSD menu 
    2. Select Withdraw option.
    3. Done. Money is transfered to his local mobile money account.
    
## What is going on behind the scenes?

For ever country Badili is available, this is how the set up looks.

    1. Badili has integrated with a local mobile money provider that allows Badili users for that country to conviniently liquidate assets and transfer money to Badili.
    2. Badili receives money deposited by the users and in turn transfers stable coin of the same value to the user.
    3. For all the currencies the user holds, Badili establishes trustlines between the user's blockchain account and the assset's issuing account.
    4. For cross currency payements, Badili utilizes path payments made possible by the underlining blockchain.
    5. Sending money from one account holder to another, Badili fetches the 2 blockchain accounts of the users and facilitates the money transfer, through the established trustlines.
    6. Users can also send money directly to an accounts blockchain address if they already have the recipient's address. The receipient doesn't have to own a Badili account. 
    7. Users could also receive funds from other blockchain addresses directly if they share their addresses. (Not made obvious for simplicity's sake.)
    8. Other applications can send any currency to a Badili account holder by going through Badili's public apis.
    
![Image of badili stack](/badili.jpg)

# What's under the hood
Badili consist of the following components working together behind the scenes.

### **1.USSD Application**
Built on top of [Africa's Talking](https://africastalking.com/ussd). This handles communication between Badili's servers and the USSD platform.
### **2.Backend Database**
We only store user's account information to handle all the complexity behind the scenes. Users' private information like secret keys and account passwords are encrypted and stored securely. Only the users have access to their private information, not even us.
We use Postgres database btw.
### **3.Middleware**
This handles all the communication between the blockchain and other services Badili uses to offer the service. This layer is supposed to be modular so that we are able to easily add, replace or remove service Badili uses for different countries it is available in.



#### **Services used**
##### 1. Blockchain
We use the [Stellar blockchain](https://stellar.org/) as our blockchain of choice for the obvious reasons. It is crazy cheap and fast to make crossboarder payments.
##### 2. KYC
It is different for the different countries we offer, but as of our current version these are the different KYC providers we use.
1. Appruve - This is used for Kenya, Ghana, Uganda and Nigeria.

##### 3. Local Mobile Money Providers
We use these providers for users to easily offramp and fund their accounts as explained [*here*]()
Like all the services, it is different for the different countries we are available.
1. [MPESA](https://www.safaricom.co.ke/m-pesa) - This is used in Kenya
2. [TigoPesa](https://www.tigo.co.tz/tigo-pesa-for-developers) - Used in Tanzania
3. [MTN](https://momodeveloper.mtn.com/) - Used in Uganda
4. [Flutterwave](https://flutterwave.com/ke/) - This is used in Nigeria, Ghana, Rwanda and Zambia
To be discussd further.

##### 4. Africa's talking 
For SMS based communication between Badili and our clients, we use [Africa's Talking](https://africastalking.com/sms) messaging service.

## Hosting
For testing we are using the following services to deploy our application to the public
1. [Heroku](https://heroku.com/)
2. 

*This document is used internally at Badili to keep different teams in sync with all things Badili.*
*All chsnge contributions are welcomed.*
















    
