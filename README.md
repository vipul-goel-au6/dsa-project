====================================Bitcoin Price Notifier=============================================

### Bitcoin Notifier

As we all know, the Bitcoin price is a fickle thing. You never really know where it’s going to be at the end of the day. So, instead of constantly checking various sites for the latest updates, let’s make a Python app that runs as a command-line tool to do the work for you.

Although many alternatives exist such as Firebase/Custom Web Sockets, we recommend using the popular automation website IFTTT. IFTTT (“if this, then that”) is a web service that bridges the gap between different apps and devices.

### Prerequisite

  => Python3 
  => Install the IFTTT App to receive the notifications 
  => Telegram App and follow this channel 
  => Twitter account and follow this account 
  => An email account for emergency price alert
   
### Installation

    As we this scipt will fetch the data from an API so install requests for that by using

    ----------------------------------
       => pip install requests
    ----------------------------------


### Usage

Bitcoin notifier is a python script which will be used for bitcoin notification.By running this script user will get regular and emergancy updates of bitcoin according to the choosen and default parameters.

Bitcoin notifier have two IFTTT applets:
1. One for emergency notification when Bitcoin price falls under a certain threshold

    The emergancy notifications will be sent to the user's email address.
    And on the IFTTT

2. Second for regular  updates on the Bitcoin price

    The regular updates by default will be sent to user on telegram upon following the channel.
    User can also choose the destination of regular notification from Telegram and twitter.

    Follow links: 

    Telegram : https://t.me/bitcoinnotifier

    Twitter: https://twitter.com/BitcoinNotifier

    -------------------------------------------
    => -d (twitter or telegram)
    -------------------------------------------

### Time-Interval:
    By default the user will receive one notification per minute but user can cutomize that by entering a time interval in minutes

    ---------------------------------------------
    => -i (preferred interval in minutes(eg. 10))
    ---------------------------------------------

### Threshold:
    By default the threshold for the emergancy notification is 700000INR.
    User will receive a notification on his/her email whenever the price drops from this threshold.
    User can also customize threshold by entering threshold in INR

    ---------------------------------------------
    => -t (preferred threshold in INR(eg. 500000)
    ---------------------------------------------

    For all the customized options user can enter as shown below after running the program

    ---------------------------
    -i 1 -t 700000 -d twitter
    ---------------------------

    Here:
    i => time interval
    t => threshold in INR
    d => destination of regular notifications