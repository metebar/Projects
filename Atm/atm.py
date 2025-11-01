import os 
with open ('pincode.txt','r') as rf:
    pincode = rf.readline()
with open ('balance.txt','r')  as rf:
    balance = int(rf.readline())
    
pin_tries = 3
login_corfirmation = False
################### 
print("Welcome to the MeteBank")
while pin_tries != 0 :
   user_given_pin = input("Please type your pin\n")
   os.system('cls')

   if user_given_pin != pincode:
     pin_tries -= 1
     print(f'Wrong pin. You have  {pin_tries}  tries left')
     if len(str(user_given_pin)) != len(str(pincode)):
       print("Your pin must be 4 digit")
   else:
       login_confirmation = True
       break

if pin_tries == 0:
    login_confirmation = False
    print("Your card is blocked")   
###########
while login_confirmation == True:
     
     menu_selection_1= int(input("1- Withdrawal\n2- Balace Inquiry\n3- Change Pin\n4- Deposit\n5- Exit\n"))
     os.system('cls')
     
     if menu_selection_1 == 1:
       amount_withdrawal =int(input("Please type the amount you want to withdraw\n$"))
       if amount_withdrawal > balance:
           print("Insufficient balance")
       else:
        balance -= amount_withdrawal
        with open ('balance.txt','w') as wf:
            wf.write(str(balance))
        print(f'${amount_withdrawal}')
###########
     elif menu_selection_1 == 2:
       print(f'You have ${balance} in your account')
###########
     elif menu_selection_1 == 3:
       new_pin_1 = int(input("Write your new pin\n"))
       new_pin_2 = int(input("Write your new pin again\n"))
       if len(str(new_pin_1)) != 4:
           print("Your pin must be 4 digit")
       elif int(pincode) == new_pin_1:
           print("Your new pin can't be same with old one")
       elif new_pin_1 == new_pin_2:
         pincode = new_pin_1
         with open ('pincode.txt','w') as wf:
             wf.write(str(pincode))
         print("You have successfully changed your pin.")
       else:
         print("Pins doesn't match")
###########
     elif menu_selection_1 == 4:
        amount_deposit = int(input("Please write the amount you want to deposit\n$"))
        balance += amount_deposit
        with open ('balance.txt','w') as wf:
            wf.write(str(balance))
###########
     elif menu_selection_1 == 5:
         print("Thanks for visiting MeteBank")
         break
     else:
       print("Incorrect Selection")
###########
     user_choice= int(input("Would you like to continue?\n1- Yes\n2- No\n"))
     if user_choice == 2:
         os.system('cls')
         print("Thanks for visiting MeteBank")
         break
###########
     elif user_choice == 1:
         os.system('cls')
         continue
     else:
         os.system('cls')
         print("Thanks for visiting MeteBank")
         break
         