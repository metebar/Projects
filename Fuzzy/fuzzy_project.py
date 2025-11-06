def rules(smallx1, smally1, largex1, largey1):
    small1 = min(smallx1, smally1)
    large1 = min(largex1, largey1)
    medium1 = min(smallx1, largey1)
    medium2 = min(smally1, largex1)

    result = (small1 * 0 + large1 * 20 + medium1 * 10 +
              medium2 * 10) / (small1 + large1 + medium1 + medium2)
    return result
def multip(smallx1, smally1, largex1, largey1):
    f1= smallx1*smally1
    f2= largex1*largey1
    f3= smallx1*largey1
    f4= largex1*smally1

    multresult= (f1*0 + f2*20 + f3*10 + f4*10)/(f1+f2+f3+f4)
    return multresult
v1 = 0.1
# ask the user for input
x = float(input("Enter a value for x: "))
y = float(input("Enter a value for y: "))
if(y>10):
    quit("y can't be bigger than 10")

smallx1 = round((1 - (x * v1)),2)
smally1 = round((1 - (y * v1)),2)
largex1 = x * 0.1
largey1 = y * 0.1

result = rules(smallx1, smally1, largex1, largey1)
multresult = multip(smallx1, smally1, largex1, largey1)
print(smallx1,largex1,smally1,largey1)
print(result)
print(multresult)