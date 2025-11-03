import os

logo = '''
                         ___________
                         \         /
                          )_______(
                          |"""""""|_.-._,.---------.,_.-._
                          |       | | |               | | ''-.
                          |       |_| |_             _| |_..-'
                          |_______| '-' `'---------'` '-'
                          )"""""""(
                         /_________\\
                       .-------------.
                      /_______________\\
'''

bidders = []

def blind_auction():
    other_bidders = True
    max_bidder = ""
    max_bid = 0
    print(f"{logo}Welcome to the Secret Auction Program")
    
    while other_bidders == True:
        name_bidder = input("What is your name?: ")
        bid_amount = int(input("What's your bid?: $"))

        temp_bidders = {}
        temp_bidders["name"] = name_bidder
        temp_bidders["bid"] = bid_amount
        
        bidders.append(temp_bidders)
        
        for current_bidder in bidders:

                if max_bid < current_bidder['bid']  :
                    max_bid = current_bidder['bid'] 
                    max_bidder = current_bidder['name']
        
        answer = input("Are there any other bidders? Type 'yes' or 'no'.")
        
        if answer == "yes":
            os.system('cls')

        else:
            os.system('cls')
            print(f"The winner is {max_bidder} with a bid of ${max_bid}.")
            other_bidders =False
            
blind_auction()
