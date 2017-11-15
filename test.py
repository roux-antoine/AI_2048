a = 2048

nbrDigits = 1
power = 10

while a//power > 0.5 :
    nbrDigits+=1
    power *= 10

print(nbrDigits)
