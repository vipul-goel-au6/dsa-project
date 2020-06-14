from requests import get, post
from time import sleep
from argparse import ArgumentParser
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from os import system
from config import gmail_address, gmail_password
from re import search, I

# To run the current system
system("")


# Webhooks and Api URL
bitcoin_url = "https://api.coindesk.com/v1/bpi/currentprice/INR.json"
base_url = "https://maker.ifttt.com/trigger/"
key = "/with/key/l9VIJOaT5Vh6OHIH-5GA7tMTIrrSPCwfLi-KALeJmj6"
ifttt_phone = base_url + "Bitcoin_Alert" + key
ifttt_telegram = base_url + "Bitcoin_Price" + key
ifttt_twitter = base_url + "Bitcoin_Update" + key


# To get Current Bitcoin price in INR
def bitcoin_price():
    # get response from api and convert to json
    response = get(bitcoin_url)
    response_json = response.json()

    bitcoin_price = float(response_json["bpi"]["INR"]["rate_float"])

    # return float price with 1 decimal
    return round(bitcoin_price, 1)


# To send email for threshold price alert
def threshold_price_alert(email, bitcoin_data, threshold):
    # First sending the alert email to user

    # constructing the message to be sent by email
    message = """From:bitcoin.notifier.vipul@gmail.com
To: {}
Subject: !! Alert !! Bitcoin Price Below Threshold
Bitcoin Price is below {}\n
Bitcoin Price reached ₹{} at {},\n
Stay Tune for further updates\n\n
Regards Vipul Goel
""".format(email, threshold,
           bitcoin_data["current_bitcoin_price"],
           bitcoin_data["date"])

    msg = MIMEMultipart()
    # assigning sender and receiver emails
    msg["From"] = gmail_address
    msg["To"] = email

    # Configuring gmail sever to send mails
    gmail_server = SMTP('smtp.gmail.com: 587')

    gmail_server.starttls()

    # Login into gmail with email and password
    gmail_server.login(gmail_address, gmail_password)

    # Sending the mail alert email
    gmail_server.sendmail(msg["From"], msg["To"], message.encode("utf-8"))

    # Closing the gmail server
    gmail_server.quit()

    # Second sending the ifttt phone notification

    # assigning vslues to be send in json format
    value = {"value1": threshold,
             "value2": bitcoin_data["current_bitcoin_price"],
             "value3": bitcoin_data["date"]}

    # Posting the ifttt phone notification
    post(ifttt_phone, json=value)

    print("Alert Email and Phone Notification Successfully Sent\n")


# To post the price notification to resp. destination
def post_notification(data, dest):

    # assigning vslues to be send in json format
    data = {"value1": data["date"],
            "value2": data["current_bitcoin_price"]}

    # Checking if destination is twitter or telegram
    if dest == "twitter":
        dest_url = ifttt_twitter
    else:
        dest_url = ifttt_telegram

    # POST request to the destination URL with data
    post(dest_url, json=data)
    print("Bitcoin Price Notification Sent on {}\n".format(dest))


# Function which collects price and send a notification to dest
def bitcoin_notification(interval_time, threshold, destination, email):
    interval_time = int(interval_time[0])
    threshold = float(threshold[0])
    destination = destination.lower()

    try:
        while True:
            # getting current bitcoin price
            current_bitcoin_price = bitcoin_price()

            # Print current bitcoin price
            print("\nCurrent Bitcoin Price is {}\n"
                  .format(current_bitcoin_price))

            date = datetime.now()
            # creating required data in json format
            bitcoin_data = {
                "date": date.strftime("%H:%M %d.%m.%Y"),
                "current_bitcoin_price": current_bitcoin_price}

            # Sending alert notifications if price is below threshold
            if current_bitcoin_price <= threshold:

                print("!!!...Bitcoin Price Below Threshold...!!!\n")
                print("Sending alert email and phone notification\n")

                threshold_price_alert(email, bitcoin_data, threshold)

                print("Next notification in {} minutes".format(interval_time))
                sleep(interval_time*60)
                continue

            post_notification(bitcoin_data, destination)

            # Delay for the next price notification
            print("Next notification in {} minutes".format(interval_time))
            sleep(interval_time*60)

    # Terminating the program
    except KeyboardInterrupt:
        print('-------------------------------------')
        print("")
        print("Terminating The Process!!!!")
        print("Thank You supporting")
        print("")
        print('--------------------------------------')
        return


# Main function for all arguements
def main():
    # Adding description and epilog in parser
    parser = ArgumentParser(description="""
Bitcoin Price Notification App.""",  epilog="""
Welcome Bitcoin Price Notification App""")

    # Adding the required arguments done by user
    parser.add_argument("-i", "--interval_time", type=int, nargs=1,
                        default=[1], metavar="interval_time",
                        help="Time interval for updates, default is 1 min")

    parser.add_argument("-t", "--threshold", type=int, nargs=1, default=[
                        300000], metavar="threshold",
                        help="Threshold price, default is ₹ 3 lakhs")

    parser.add_argument("-d", "--destination", default="telegram",
                        metavar="destination",
                        help="""
Destination for price update (telegram/twitter),
default is telegram""")

    args = parser.parse_args()

    # Welcome message and instructions
    print("""
:::..WELCOME..::\n
This app gives the price of 1 Bitcoin in INR(₹).
Destination (-d) is by default telegram.
To recive notification from IFTTT install IFTTT mobile app.\n
To recive price update on Twitter follow this account
https://twitter.com/BitcoinNotifier\n
To recive price update on Telegram join this channel
https://t.me/bitcoinnotifier

Ctrl+C to terminate the app\n\n""",
          "\nBitcoin Notification App started\n",
          "Regular Updates after every", args.interval_time[0],
          "Minutes\n Threshold Price is ₹", args.threshold[0],
          '\n Destination for regular updates is', args.destination, '\n\n')

    # email from user for alert message and check if its valid email
    while True:
        email = input("Enter Your Email to Recieve Alert Mails: \n")
        regex = r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"
        if(search(regex, email, I)):
            break
        else:
            print("Invalid Email, Enter again\n")
            continue

    print("\nFollow on Twitter : https://twitter.com/BitcoinNotifier\n")
    print("Join channel on Telegram : https://t.me/bitcoinnotifier\n")

    # calling the function for further notification processes
    bitcoin_notification(args.interval_time,
                         args.threshold,
                         args.destination,
                         email)


if __name__ == '__main__':
    main()
