list=[1,7,4,3,5,6]
print("enter the searching value")
search=input()
i=0 
while i < len(list):
    if list[i] == search:
        i=i+1
        print("element is found ")
        break
    else:
         print("element is not found")
         break