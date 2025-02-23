import mysql.connector as ms

import time
        
con,cur=None,None

name=None
typ=None
diet=''
price=None
side=None
custPhone=None


cnt=0 #variable used to iterate through numbers and printed on screen as serial numbers

dic = {} # WILL BE --> dic = {<order no.> : [<dish name>,<price>,<diet>]}
custOrd = {}#WILL BE --> custOrd = {<order no.> : [[<dish name>,<price>,<diet>],<frequency>]}

#variables for checking orders and used in order function
m=[]
mtemp=[]

#default timings set here
openBreakfast=7
closeBreakfast=12
openLunch=13
closeLunch=17
openDinner=17
closeDinner=24

#variable to check whether items show up on menu list during ordering. if not, then appropriate message will be stored in chk variable
chk=None


def nothing(inpt): # function to check whether no input is entered
    if inpt.strip()=='':
        return True
            
def nameF(): # function to input dish name
    global name
    name = input('Enter dish name: ')
    name=name.strip()
    name=name.capitalize()
    if nothing(name)==True:
        print("\nPlease enter a valid input.\nEnter values again!")
        nameF()
    

def typF(): # function to input the type of dish (i.e. whether it is breakfast,lunch,dinner,appetizer or beverage)
    global typ
    #print(typ)
    typ=None
    typ = input('Input dish type(s) seperated by a comma without space (breakfast,lunch,dinner,appetizer,beverage)\nEg: breakfast,lunch,dinner (or) lunch,dinner\nEnter: ')
    typ = typ.lower()
    
    if nothing(typ)==True:
        print("\nPlease enter a valid input.\nEnter values again!")
        typF()
        
    n = typ.split(',')# splitting the input string so that it can be iterated through by the below for loop so that it can be checked
    l=[]
    

    for i in range(len(n)):
        indish = str(n[i])
        if indish=='breakfast' or indish=='lunch' or indish=='dinner' or indish=='appetizer' or indish== 'beverage':
            continue
        else:
            print("Invalid input - Enter only given dish types without space")
            print("Enter inputs again!")
            typF()
    
            
    #converting the splitted list back into the string after checking
    for i in n:
        l+=[i.strip()]
    typ=''
    for i in range(len(l)):
        if i==(len(l)-1):
               typ=typ+l[i]
        else:
            typ=typ+l[i]+','

    

            
def dietF(): # function to input the dish nature (i.e. whether it is veg or nonveg)
    global diet
    diet = input("Enter either vegeterian or non-vegeterian (v/nv): ")
    diet=diet.strip()
    diet=diet.lower()

    if nothing(diet)==True:
        print("\nPlease enter a valid input.\nEnter values again!")
        dietF()

    # to check whether entered input is only under the given options (i.e. only veg or nonveg options)
    while diet!='v' and diet!='nv':
        print("\nInvalid Diet inputs",end='')
        print("Enter inputs again!\n")
        dietF()
        
def sideF():# funciton to input whether the dish is sidedish or not
    global side
    side = input("Enter whether side dish or not (y/n): ")

    if nothing(side)==True:
        print("\nPlease enter a valid input.\nEnter values again!")
        sideF()
        
    # to check whether entered input is only under the given options (i.e. whether it is sidedish or not)
    while side!='y' and side!='n':
        print("\nInvalid inputs")
        print("Enter inputs again!\n")
        sideF()
        
def priceF():#function to input the price of dish
    global price
    price = input("Enter price: ")

    if nothing(price)==True:
        print("\nPlease enter a valid input.\nEnter values again!")
        priceF()

    # ensuring that the given input is only a number
    while price.isnumeric()!=True:
        print("Invalid Price inputs")
        print("Enter inputs again")
        priceF()
    price=int(price)

        
def admin():# admin operations function
    
    
    print('-'*153,'\n1 - Display Dishes\n\n2 - Add Dishes\n\n3 - Remove Dishes\n\n4 - Set Dish availability\n\n5 - Change availability timings\n\n6 - Order Reports\n\n7 - Switch users or to quit application\n\n',sep='')
    try:
        ask = input("Enter your choice: ") #Asking admin to pick one of the following actions <----------------------------

        if nothing(ask)==True:
            print("\nPlease enter a valid input.\nEnter values again!")
            admin()

        #checking whether entered input is only a number
        try:
            ask = int(ask)
        except ValueError:
            print("Enter a number only")
            print("Enter values again!")
            admin()
        
        if ask==1: # Displaying the dishes <---------------------------------
            cur.fetchall()#fetching all to discard any results of previous select commands that gives output
            cur.execute('select * from custMenu') #checking whether any dishes are available in menu in order to perform the above action
            n=cur.fetchall()
            if n==[]:
                print("\nNo dishes available to display")
                print("Add some dishes to be displayed\n")
                admin()
            
            print("\nDishes:\n") #Displaying the retrieved records <---------------------------------
            for i in n:
                print(i[0],' - ',i[1],end=' - ')
                    
                if i[2]=='v':
                    print("vegetarian",end='  ')
                else:
                    print("nonvegetarian",end=' ')
                    
                if i[4]==1:
                    print("side dish",end=' - ')
                else:
                    print("dish",end = ' - ')
                    
                print("price:",i[3])
                
            print('\n','-'*153,sep='')
            admin()
                 
        elif ask ==2: # Adding dishes <--------------------------------------
            add()

            ask = input("\nPress enter to go back to admin screen")
            if ' 'in ask or '' in ask:
                admin()
        elif ask ==3:#Deleting dishes <--------------------------------------
            cur.fetchall()#fetching all to discard any results of previous select commands that gives output
            cur.execute('select * from custMenu')  #checking whether any dishes are available in menu in order to perform the above action
            n=cur.fetchall()
            if n==[]:
                print("\nNo dishes available to delete")
                admin()
            delete()
            ask = input("\nPress enter to go back to admin screen")
            if ' 'in ask or '' in ask:
                admin()
            
        elif ask==4:#Changing dish availaiblity <-----------------------------------------
            cur.fetchall()#fetching all to discard any results of previous select commands that gives output
            cur.execute('select * from custMenu') #checking whether any dishes are available in menu 
            n=cur.fetchall()
            if n==[]:
                print("\nNo dishes available to change availability")
                print("Add some dishes to change their availability\n")
                admin()
            
            set_availability()
            
            ask = input("\nPress enter to go back to admin screen")
            if ' 'in ask or '' in ask:
                admin()


        elif ask==5: #Changing availability timings <--------------------------------------
            change_timings()
            ask = input("\nPress enter to go back to admin screen")
            if ' 'in ask or '' in ask:
                admin()

        elif ask==6:# ORDER REPORTS HERE <--------------------------------------
            orderReport()
            ask = input("\nPress enter to go back to admin screen")
            if ' 'in ask or '' in ask:
                admin()
        
        elif ask==7: #Switching users (admin,customer,delivary) <-----------------------------------------
            choose()
            ask = input("\nPress enter to switch users or quit application")
            if ' 'in ask or '' in ask:
                choose()
           
        else:
            print("Invalid input\nEnter inputs again!\n",'-'*153,sep='',end='')
            admin()

    except:
        print('Unknown Erorr - admin portal')
        print("Enter inputs again!\n",'-'*153,sep='',end='')
        admin()



def add():
    global name,typ,diet,price,side
    print('\n','-'*153,sep='')
    try:
        # first asking user to enter the inputs <-------------------------------------------
        nameF()

        #ensuring the length of the dish is not above the length limit according to the table in the database
        if len(name)>30:                                                                             
            print("Invalid input - Length of dish too long")                                                                        
            print("Enter inputs again!\n",'-'*153,sep='',end='')      
            add()                                                                                              

        #checking whether the entered input is only alphabetical characters    
        l=[]
        l=name.split()
        for i in l:  
            if i.isalpha()==False:
                print("\nPlease enter a text or string")
                print("Enter inputs again!\n",'-'*153,sep='',end='')
                add()

        #checking whether entered dish is already in the database
        cur.fetchall()#fetching all to discard any results of previous select commands that gives output
        cur.execute("select count(1) from custMenu where dish=%s;",(name,))    
        rec_cnt=cur.fetchone()
        if rec_cnt[0]>0:
            print("\nDish already exists")
            print("Enter inputs again!\n",'-'*153,sep='',end='')
            add()
        
        typF() # asking the availability of dish
        
        
        dietF()# asking the diet type of dish
  
        #asking for price of dish and checking for proper price inputs
        while True:
            try:
                priceF()
                price=round(float(price),2)
                break
            except:
                print("\nInvalid Price inputs",end='')
                print("Enter inputs again!\n")

        #asking whether dish is side dish or not and converting yes and no into 1 or 0 so it can be a boolean value that can be stored in table of database
        sideF()
        side=side.lower() 
        if side=='y':
            side=1
        else:
            side=0

        #updating the inputs to the database <-------------------------------------------   
        cur.execute('insert into custMenu(dish,availability,diet,price,side) values(%s,%s,%s,%s,%s)',(name.capitalize(),typ,diet,price,side))
        con.commit() #commiting the values stored in cursor to the database <----------------------------------------
        
        print("Added to database's table!\n",'-'*153,sep='')
        ask = input("\nPress enter to go back to admin screen")
        if ask.strip()=='':
            admin()

    
    except:
        print("\nUnknown Error - adding dish")
        print("Enter all inputs again!\n")
        add()



def delete(): #function to delete a dish from the table of database
    print('\n','-'*153,sep='')
    nameF()# first asking for dish name to be deleted
    cur.fetchall()#fetching all to discard any results of previous select commands that gives output
    cur.execute("select dish from custMenu;")
    try:
        for i in cur.fetchall():
            
            if name in i:
                cur.execute("delete from custMenu where dish = %s",(name,))
                cur.execute("commit")
                print("Dish removed\n",'-'*153,sep='',end='')
                break
                
            
        else:
            print("\nDish not found")
            print("Enter inputs again!\n",'-'*153,sep='',end='')
            delete()
    except:
            print("\nUnknown Error - deleting dish")
            print("Enter inputs again!\n",'-'*153,sep='',end='')
            delete()
            

            
def set_availability(): #funciton to change the availability of the dish
    print('\n','-'*153,sep='')
    print('-'*153,"\nEnter name of dish to change the availability",sep='')

    nameF()# first asking for name of dish so that availability can be changed
    cur.fetchall()#fetching all to discard any results of previous select commands that gives output
    cur.execute("select dish from custMenu;")
    try:
        for i in cur.fetchall():
            if name in i:  
                typF()# secondly asking for new availability of dish

                cur.execute("update custMenu set availability=(%s) where dish=%s",(typ,name) )
                print('\nDish availability changed!\n','-'*153,sep='',end='')
                cur.execute('commit')
                break
        
        else:
            print("\nDish not found")
            print("Enter inputs again!\n",sep='',end='')
            set_availability()
       
    except:
            print("Unknown Error - setting availability")
            print("Enter inputs again!\n",'-'*153,sep='',end='')
            set_availability()

    

def orderAgain():#function to ask whether the customer would like to order again
    while True:
        ask = input("Would you like to order again (y/n)?: ")

        if nothing(ask)==True:
            print("\nPlease enter a valid input.\nEnter values again!")
            orderAgain()

        if ask in 'yY':
            customer()

        elif ask in 'nN':
            
            bill()
        
        else:
            print("\nInvalid inputs")
            print("Enter inputs again!\n",'-'*153,sep='')
            orderAgain()
        break


def anotherOrder():#function to ask whether another order can be taken on device again after an order has been billed
    while True:
        again = input("\n\nWould you like the device to taken another order again (y/n)?: ")

        if nothing(again)==True:
            print("\nPlease enter a valid input.\nEnter values again!")
            anotherOrder()

        if again in 'yY':
            print('\n'*50)
            customer()

        elif again in 'nN':
            pass
        
        else:
            print("\nInvalid inputs")
            print("Enter inputs again!\n",'-'*153,sep='')
            anotherOrder()
        break    

def customer():#function that shows customer view of the menu
    global chk
    
    print('\n','-'*153,sep='')

    global cnt
    cnt=0
    
    menu()

    if chk==False:
        print("Sorry no dishes available. We apologize for the inconvenience. Please report this to the manager")
        ask = input("\nPress enter to go back to main screen")
        if ask.strip()=='':
            choose() 
        
    
    order()
    
    orderAgain()

    anotherOrder()
    
    ask = input("\nPress enter to go back to main screen")
    if ask.strip()=='':
        choose()          

def breakfastTimings():#function to change the breakfast timings
    global openBreakfast,closeBreakfast
    
    try:
        openBreakfast = input("Enter breakfast open time hour (24 hour time format): ")
        if openBreakfast.isnumeric=='False':
            print("Enter a number only!")
            print("Enter input again\n")
            breakfastTimings()
        if len(openBreakfast)>2:
            print("No. of hours cannot be more than 24!")
            print("Enter input again\n")
            breakfastTimings()
            
        closeBreakfast = input("Enter breakfast close time hour (24 hour time format): ")
        
        if closeBreakfast.isnumeric=='False':
            print("Enter a number only!")
            print("Enter input again\n")
            breakfastTimings()
        if len(closeBreakfast)>2:
            print("No. of hours cannot be more than 24!")
            print("Enter input again\n")
            breakfastTimings()
            
        if int(openBreakfast)>int(closeBreakfast):
            print("Opening time cannot be more than closing time! ")
            print("Enter input again\n")
            breakfastTimings()

    except:
        print("Unencountered Error occurred! - Changing breakfast timings")
        print("Please enter inputs again")
        breakfastTimings()

    openBreakfast = int(openBreakfast)
    closeBreakfast = int(closeBreakfast)

    
def lunchTimings():#function to change the lunch timings
    global openLunch, closeLunch
    
    try:
        openLunch = input("Enter lunch open time hour (24 hour time format): ")
        if not openLunch.isnumeric():
            print("Enter a number only!")
            print("Enter input again\n")
            lunchTimings()
        if len(openLunch) > 2:
            print("No. of hours cannot be more than 24!")
            print("Enter input again\n")
            lunchTimings()
            
        closeLunch = input("Enter lunch close time hour (24 hour time format): ")
        
        if not closeLunch.isnumeric():
            print("Enter a number only!")
            print("Enter input again\n")
            lunchTimings()
        if len(closeLunch) > 2:
            print("No. of hours cannot be more than 24!")
            print("Enter input again\n")
            lunchTimings()
            
        if int(openLunch) > int(closeLunch):
            print("Opening time cannot be more than closing time! ")
            print("Enter input again\n")
            lunchTimings()
        #breakfast and lunch timings can be coincided because of peculier timing called "brunch" where breakfast and lunch are eaten at once
        if int(openLunch) < int(openBreakfast):
            print("Lunch Timings are conflicting with breakfast timings!")
            print("Enter input again\n")
            lunchTimings()
        if int(closeLunch) < int(closeBreakfast):
            print("Lunch Timings are conflicting with breakfast timings!")
            print("Enter input again\n")
            lunchTimings()

        
    except:
        print("An unexpected error occurred! - Changing lunch timings ")
        print("Please enter inputs again")
        lunchTimings()
    openLunch = int(openLunch)
    closeLunch= int(closeLunch)

def dinnerTimings():#function to change the dinner timings
    global openDinner, closeDinner
    
    try:
        openDinner = input("Enter dinner open time hour (24-hour time format): ")
        if not openDinner.isnumeric():
            print("Enter a number only!")
            print("Enter input again\n")
            dinnerTimings()
        if len(openDinner) > 2:
            print("No. of hours cannot be more than 24!")
            print("Enter input again\n")
            dinnerTimings()
            
        closeDinner = input("Enter dinner close time hour (24-hour time format): ")
        
        if not closeDinner.isnumeric():
            print("Enter a number only!")
            print("Enter input again\n")
            dinnerTimings()
        if len(closeDinner) > 2:
            print("No. of hours cannot be more than 24!")
            print("Enter input again\n")
            dinnerTimings()
            
        if int(openDinner) > int(closeDinner):
            print("Opening time cannot be more than closing time! ")
            print("Enter input again\n")
            dinnerTimings()

        if int(openDinner) in range(int(openBreakfast),int(closeBreakfast)):
            print("Dinner Timings are conflicting with breakfast timings!")
            print("Enter input again\n")
            dinnerTimings()
        if int(closeDinner) in range(int(openBreakfast),int(closeBreakfast)):
            print("Dinner Timings are conflicting with breakfast timings!")
            print("Enter input again\n")
            dinnerTimings()

        if int(openDinner) in range(int(openLunch),int(closeLunch)):
            print("Dinner Timings are conflicting with lunch timings!")
            print("Enter input again\n")
            dinnerTimings()
        if int(closeDinner) in range(int(openLunch),int(closeLunch)):
            print("Dinner Timings are conflicting with lunch timings!")
            print("Enter input again\n")
            dinnerTimings()

        if int(openDinner) < int(openLunch) or int(openDinner) < int(closeLunch):
            print("Lunch Timings are conflicting with breakfast timings!")
            print("Enter input again\n")
            dinnerTimings()
        if int(closeDinner) < int(openBreakfast) or int(closeDinner) < int(closeLunch):
            print("Lunch Timings are conflicting with breakfast timings!")
            print("Enter input again\n")
            dinnerTimings()

    except:
        print("An unexpected error occurred! - Changing dinner timings")
        print("Please enter inputs again")
        dinnerTimings()

    openDinner = int(openDinner)
    closeDinner = int(closeDinner)


  
def change_timings(): #function to change the timings
    print('\n','-'*153,sep='')
    breakfastTimings()
    lunchTimings()
    dinnerTimings()



def breakfast(n):#function to display the breakfast items
    global dic
    global cnt
    global chk
    
    print("BREAKFAST\n")
    chk="No breakfast available - We apologize for the inconvenience\n\n"
    for i in range(len(n)):
        if "breakfast" in n[i][1]:
            cnt += 1
            print(cnt, '. ', n[i][0], ' - \u20B9', n[i][3], end=' - ')
            if n[i][4] == 1:
                print("sidedish - ", end='')
            if n[i][2] == 'v':
                print("veg")
                dic[cnt] = [n[i][0], n[i][3], 'veg']
            else:
                print('nonveg')
                dic[cnt] = [n[i][0], n[i][3], 'nonveg']
                
        if i == len(n) - 1:
            cnt = i

        if "breakfast" in n[i][1]:
            chk=None
            continue

        
        
        
    print()

def lunch(n):# function to display the lunch items
    global cnt
    global dic
    global chk

    print("LUNCH\n")
    chk="No lunch available - We apologize for the inconvenience\n\n"
    
    for i in range(len(n)):
        if "lunch" in n[i][1]:
            cnt += 1
            print(cnt, '. ', n[i][0], ' - \u20B9', n[i][3], end=' - ')
            if n[i][4] == 1:
                print("sidedish - ", end='')
            if n[i][2] == 'v':
                print("veg")
                dic[cnt] = [n[i][0], n[i][3], 'veg']
            else:
                print('nonveg')
                dic[cnt] = [n[i][0], n[i][3], 'nonveg']
       
        if i == len(n) - 1:
            cnt = i

        if "lunch" in n[i][1]:
            chk=None
            continue
        
            
        
    print()

def dinner(n):# function to display the dinner items
    global cnt
    global dic
    global chk

    print("DINNER\n")
    chk="No dinner available - We apologize for the inconvenience\n\n"
    for i in range(len(n)):
        
        if "dinner" in n[i][1]:
            cnt += 1
            print(cnt, '. ', n[i][0], ' - \u20B9', n[i][3], end=' - ')
            if n[i][4] == 1:
                print("sidedish - ", end='')
            if n[i][2] == 'v':
                print("veg")
                dic[cnt] = [n[i][0], n[i][3], 'veg']
            else:
                print('nonveg')
                dic[cnt] = [n[i][0], n[i][3], 'nonveg']
            
        if i == len(n) - 1:
            cnt = i
            
        if "dinner" in n[i][1]:
            chk=None
            continue

        
        
            
        
    
        
    print()

def appetizer(n):# function to display the appetizer items
    global cnt
    global dic
    global chk
    
    print("APPETIZERS\n")
    chk="No appetizers available - We apologize for the inconvenience\n\n"
    for i in range(len(n)):
        if "appetizer" in n[i][1]:
            cnt += 1
            print(cnt, '. ', n[i][0], ' - \u20B9', n[i][3], end=' - ')
            if n[i][4] == 1:
                print("sidedish - ")
            if n[i][2] == 'v':
                print("veg")
                dic[cnt] = [n[i][0], n[i][3], 'veg']
            else:
                print('nonveg')
                dic[cnt] = [n[i][0], n[i][3], 'nonveg']
        
        if i == len(n) - 1:
            cnt = i

        if "appetizer" in n[i][1]:
            chk=None
            continue

            
        
    print()

def beverage(n):#funciton to display the beverage items
    global cnt
    global dic
    global chk
    
    print("BEVERAGES\n")
    chk="No beverage available - We apologize for the inconvenience\n\n"
    for i in range(len(n)):
        if "beverage" in n[i][1]:
            cnt += 1
            print(cnt, '. ', n[i][0], ' - \u20B9', n[i][3], end=' - ')

            if n[i][2] == 'v':
                print("veg")
                dic[cnt] = [n[i][0], n[i][3], 'veg']
            else:
                print('nonveg')
                dic[cnt] = [n[i][0], n[i][3], 'nonveg']
        
        if i == len(n) - 1:
            cnt = i

        if "beverage" in n[i][1]:
            chk = None
            continue

        
        
    print()
   
    
def menu():#function that shows the menu to the customer
    
    cur.fetchall()#fetching all to discard any results of previous select commands that gives output
    cur.execute('select * from custMenu')
    fetchAll = cur.fetchall()
    
    
    print("\n------------------------------------------------------------------------MENU------------------------------------------------------------------------\n")


    curr_time = time.strftime("%H:%M:%S", time.localtime())
    
    #displaying appropriate availibities at appropriate timings
    
    global chk

    count=0
    chkCount=0
    
    while True:
     
        if openDinner<=int(curr_time[:2])<=closeDinner :
            dinner(fetchAll)
            count+=1
            if chk==None:
                
                chk=''
            else:
                
                chkCount+=1
            print(chk)
            appetizer(fetchAll)
            count+=1
            if chk==None:
                
                chk=''
            else:
                
                chkCount+=1
            print(chk)
            beverage(fetchAll)
            count+=1
            if chk==None:
                
                chk=''
            else:
                
                chkCount+=1
            print(chk)
            
            break  
        elif openLunch<=int(curr_time[:2])<closeLunch : 
            lunch(fetchAll)
            count+=1
            
            if chk==None:
                
                chk=''
            else:
                
                chkCount+=1
                print(chk)
            appetizer(fetchAll)
            count+=1
            if chk==None:
             
                chk=''
            else:
               
                chkCount+=1
            print(chk)
            beverage(fetchAll)
            count+=1
            if chk==None:
                
                chk=''
            else:
            
                chkCount+=1
            print(chk)
            
            break

        elif closeBreakfast<=int(curr_time[:2])<openLunch : 
            breakfast(fetchAll)
            count+=1
            if chk==None:
              
                chk=''
            else:
             
                chkCount+=1
            print(chk)
            lunch(fetchAll)
            count+=1
            if chk==None:
              
                chk=''
            else:
         
                chkCount+=1
            print(chk)
            appetizer(fetchAll)
            count+=1
            if chk==None:
                chk=''
            print(chk)
            beverage(fetchAll)
            count+=1
            if chk==None:

                chk=''
            else:
                chkCount+=1
            print(chk)
            break   
        elif openBreakfast<=int(curr_time[:2])<closeBreakfast :
            breakfast(fetchAll)
            count+=1
            if chk==None:
                chk=''
            else:
                chkCount+=1
            print(chk)
            beverage(fetchAll)
            count+=1
            if chk==None:
                chk=''
            else:

                chkCount+=1
            print(chk)
            break

        
        
        else:
            print("No dishes available - We apologize for the inconvenience")
            break

    if chkCount ==0 and count==0:
        pass
    elif chkCount==count:
        chk=False


def order():#function to store the customer order inputs
    global dic
    global custOrd
    global m,mtemp
    mtemp=m.copy()
    
    inp=input("\n-------------------------------------------------------------------------\n\nPlease enter order numbers seperated by a comma without any spacing\nFor more than one item of same order,simply enter the numbers again in the same way!: ")

    if nothing(inp)==True:
        print("\nPlease enter a valid input.\nEnter values again!")
        order()
    
    if inp.strip()=='':
        print("\nPlease provide a valid input")
        mtemp=[]
        order()

    #Below code is to verify if the customer entered values are in the menu list from DB
    mtemp += inp.split(',')
    if mtemp[-1]=='':
        mtemp.pop()
    x = None

 
    for i in mtemp:
        if i=='':
            mtemp.remove(i)
        if i.isnumeric()==False:
            print("\nEnter numbers only seperated by a comma without any spacing! ")
            print("Enter values again\n")
            mtemp=[]#Check if we to use mtemp later
            order()

    menuNos = list(dic.keys())
    
    for i in mtemp:
        if int(i) not in menuNos:
            print("\nDish no. not in menu!")
            print("Please enter all inputs again!")
            mtemp=[]
            order()

    m=mtemp.copy()

    for i in m:
        if m.count(i)>1:
            x=dic[int(i)]
            custOrd[int(i)]=[x,m.count(i)] #<------------------- takes cares of quantity 
            continue
        
        
        x=dic[int(i)]
        custOrd[int(i)]=[x,1]
        
    


def phone():#function to store customer phone number
    global custPhone
    custPhone = input("\n\nPlease Enter your Phone Number without any space: ")
    if nothing(custPhone)==True:
        print("\nPlease enter a valid input.\nEnter values again!")
        phone()
    if custPhone=='0000000000':
        print("Enter a correct phone number")
        phone()
        
    if (custPhone.isnumeric and len(custPhone)==10) == False:
        print("Enter a correct phone number")
        phone()



def bill():# function to bill the customer orders

    print('\n','-'*153,sep='')
    print('Dishes Ordered                 Price                         Quantity                      Subtotal')
    x = 0
    for i in custOrd:
        x+=1
        print(x,'. ',custOrd[i][0][0],' '*(24-len(custOrd[i][0][0])),'\u20B9',custOrd[i][0][1],' '*(28-len(str(custOrd[i][0][1]))),custOrd[i][1],'                          ','\u20B9',(custOrd[i][0][1])*custOrd[i][1])

    phone()

    cur.execute('insert into custorder(custPhone) values(%s)',(custPhone,))
    
    cur.fetchall()#fetching all to discard any results of previous select commands that gives output   
    cur.execute('select max(ordID) from custorder where custPhone=%s and ordDate',(custPhone,))
    ordID=cur.fetchone()[0]

        
        
    for i in custOrd:
        
        cur.execute('insert into custOrddetail(ordId,dish,price,quantity) values(%s,%s,%s,%s)',(ordID,custOrd[i][0][0],custOrd[i][0][1],custOrd[i][1]))
            
            
    con.commit() #commiting the values stored in cursor to the database <----------------------------------------
    print("Your order number is ",ordID)
        



def orderReport():# function to display all the orders that have been undertaken for the admin
    print('\n','-'*153,sep='')
    cur.fetchall()#fetching all to discard any results of previous select commands that gives output
    cur.execute('select o.ordId, o.custPhone,o.ordDate, d.dish,d.price,d.quantity, d.price*d.quantity as "Line total" from custorder o, custorddetail d where o.ordid=d.ordid;')
    print('+-------+------------+---------------------+------------------------------+---------+----------+------------+')
    print('| ordId | custPhone  | ordDate             | dish                         | price   | quantity | line total |')
    print('+-------+------------+---------------------+------------------------------+---------+----------+------------+')



    allRec=cur.fetchall()
    recCount=0
    repTotal=0
    linetotlen=10

    for i in allRec:      
        print(f"| {' '*(4-len(str(i[0])))}{i[0]}  | {i[1]} | {i[2]} | {i[3]}{' '*(28-len(i[3]))} | {' '*(8-len(str(i[4])))}{i[4]}| {' '*(8-len(str(i[5])))}{i[5]} | {' '*(linetotlen-len(str(i[6])))}{i[6]} |")
        repTotal+=i[6]
    print('+-------+------------+---------------------+------------------------------+---------+----------+------------+')        
    print(f"|       |            |                     |   {' '*26} |         | TOTAL    | {' '*(linetotlen-len(str(repTotal)))}{repTotal} |")
    print('+-------+------------+---------------------+------------------------------+---------+----------+------------+')

def choose():#function to choose between admin mode and customer view mode
    global cnt,dic,custOrd,m
    cnt=0
    dic = {} # dic = {<order no.> : [<dish name>,<price>,<diet>]}
    custOrd = {}#custOrd = {<order no.> : [[<dish name>,<price>,<diet>],<frequency>]}
    m=[]
    cur.fetchall()#fetching all to discard any results of previous select commands that gives output
    cur.execute("select * from custMenu;")
    n = cur.fetchone()
    
    print('\n'*45)
    print('\n------------------------------------------------------------- RESTAURANT MANAGEMENT SYSTEM --------------------------------------------------------------\n')
    
    print('\n1 - Admin\n\n2 - Customer\n\n3 - Quit')

    
    print()
    ask = input("Enter your choice: ")

    if nothing(ask)==True: 
        print("\nPlease enter a valid input.\nEnter values again!")
        choose()

    try:
        ask = int(ask)
    except ValueError:
        print("Enter a number only")
        print("Enter values again!")
        choose()
    
        
    if ask==1:
        pass #<----------------- use admin function here

        admin()
    elif ask ==2:
        if n==None:
            print("\nNo dishes available")
            print("Enter some dishes onto the menu in order to display to customers\n")
            ask = input("\nPress enter to go back to admin screen")
            if ' 'in ask or '' in ask:
                admin()
        pass #<------------------ use customer function here

        customer()
    elif ask==3:
        quit()#<----------------- quitting the program option
    
    else:
        print("\nInvalid input\n",'-'*153,sep='')
        choose()
    

def start():#start of program and connecting to database. if database doesnt exists, it will create one on the device, if the program is newly executed on the device
    global con,cur
    try:
        pw=input("Enter MySQL password: ")
        con = ms.connect(host = 'localhost', user = 'root', password = pw,auth_plugin='mysql_native_password')
        cur = con.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS hotel;")
        cur.execute("USE hotel;")
        cur.execute("CREATE TABLE IF NOT EXISTS custMenu (dish varchar(30) NOT NULL PRIMARY KEY, availability varchar(35), diet varchar(2), price float, side tinyint(1));")
        cur.execute("CREATE TABLE IF NOT EXISTS custorddetail (ordID int NOT NULL, dish varchar(30) NOT NULL, price float NOT NULL, quantity int NOT NULL, PRIMARY KEY (ordID, dish));")
        cur.execute("CREATE TABLE IF NOT EXISTS custOrder (ordId int NOT NULL AUTO_INCREMENT, custPhone bigint NOT NULL, ordDate datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (ordId));")
        choose()

    except ms.errors.Error as error:
        if error.errno == ms.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Password incorrect - Access Denied")
            print("Please enter password again!\n")
            start()

        else:
           print(f"Error: {error}")
           print("Unknown Error")

#Whole program starts here    
start()
