from art import logo
import random


def sum_of_cards(who):
    card_sum = 0
    for card in game_cards[f"{who} Cards"]:
        card_sum += card
    return card_sum


def draw_cards(get_card,c_card_sum):
    if get_card == "y":
        game_cards["User Cards"].append(cards[random.randint(0, 12)])
        u_card_sum == sum_of_cards("User")
        if c_card_sum <= 17:
            game_cards["Computer Cards"].append(cards[random.randint(0, 12)])
            print("Computer gets a card.")
            c_card_sum = sum_of_cards("Computer")
    else:
        if c_card_sum <= 17:
            print("Computer gets a card.")
            game_cards["Computer Cards"].append(cards[random.randint(0, 12)])
            c_card_sum = sum_of_cards("Computer")
    
       


def win_con(get_card):
    if u_card_sum > 21:
        return False
    elif c_card_sum > 21:
        return True
    elif u_card_sum == 21:
        return True
    elif c_card_sum == 21:
        return False
    if c_card_sum <= 17:
        draw_cards(get_card,c_card_sum)
        
    if get_card == "n" and u_card_sum > c_card_sum :
        return True
    if get_card == "n" and u_card_sum < c_card_sum :
        return False
    if get_card == "n" and u_card_sum < c_card_sum :
        return "Tie"

        



cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

game_cards = {
    "User Cards": [cards[random.randint(0, 12)], cards[random.randint(0, 12)]],
    "Computer Cards": [cards[random.randint(0, 12)], cards[random.randint(0, 12)]]
} 
######################################
print(logo)
start_game = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ")

if start_game == "y":

    user_cards = game_cards["User Cards"]
    computer_cards = game_cards["Computer Cards"]
    u_card_sum = sum_of_cards("User")
    c_card_sum = sum_of_cards("Computer")
    c_first_sum = sum_of_cards("Computer")

    print(f"Your cards: {user_cards}, current score: {u_card_sum}")
    print(f"Computer's first card: [{computer_cards[0]}]")

    keep_going = True
    while keep_going == True:
        
        get_card = input("Type 'y' to get another card, type 'n' to pass: ")
        draw_cards(get_card,c_card_sum)
        
        u_card_sum = sum_of_cards("User")
        c_card_sum = sum_of_cards("Computer")
        
        print(f"Your cards: {user_cards}, current score: {u_card_sum}")
        print(f"Computer's first card: [{computer_cards[0]}]")

       
        if win_con(get_card) == True:
            print(f"Your final hand: {user_cards}, your final score score: {u_card_sum}")
            print(f"Computer's final hand: {computer_cards}, computer's final score: {c_card_sum}")
            print("You win")
            keep_going = False
        elif win_con(get_card) ==False:      
            print(f"Your final hand: {user_cards}, your final score score: {u_card_sum}")
            print(f"Computer's final hand: {computer_cards}, computer's final score: {c_card_sum}")
            print("You lost")
            keep_going = False
        elif win_con(get_card) =="Tie":
            print(f"Your final hand: {user_cards}, your final score score: {u_card_sum}")
            print(f"Computer's final hand: {computer_cards}, computer's final score: {c_card_sum}")
            print("Tie")
            