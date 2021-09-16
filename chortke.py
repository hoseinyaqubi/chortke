import sqlite3
import jdatetime

conx = sqlite3.connect('chortke.bak')
cursor = conx.cursor()
def create_table():
    '''this func for create table'''
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses_tbl(
        number_expenses int not null,
        expenses int not null,
        category TEXT COLLATE NOCASE null , 
        about TEXT COLLATE NOCASE  null ,
        date TEXT not null)
     ''')
    conx.commit()
def find_number():
    '''find new number for add to tbl'''
    cursor.execute('''
    SELECT number_expenses FROM expenses_tbl
    ORDER BY number_expenses DESC
    ''')
    num = cursor.fetchone()
    if type(num) is tuple :
        num = num[0] + 1
    else:
        num = 1
    return num


def add(spending ,category, about,date  ):
    findnumber = find_number()

    cursor.execute('''INSERT INTO expenses_tbl VALUES(:number_expenses , :expenses ,:category, :about , :date) ''' ,
      {'number_expenses':findnumber , 'expenses':spending ,'category':category, 'about': about ,'date' : date})
    conx.commit()
    print(f'Invoice was registered number : {findnumber}' )


def show(category ):
    '''this func is selected data in table'''
    if category != 'all':
        cursor.execute(''' SELECT * FROM expenses_tbl WHERE category = (:category) ''' , {'category':category})
        result = cursor.fetchall()
        cursor.execute(''' SELECT SUM(expenses)FROM expenses_tbl WHERE category = (:category) ''' , {'category':category})
        total_spending = cursor.fetchone()[0]
    elif category == 'all':
        cursor.execute(''' SELECT * FROM expenses_tbl ''')
        result = cursor.fetchall()
        cursor.execute(''' SELECT SUM(expenses)FROM expenses_tbl ''')
        total_spending = cursor.fetchone()[0]
    return result  , total_spending

def update_expenses(num_factor):
    entrance=int(input('''    update date 
    1 : delete factor 
    2 : edit factor 
    choice a number :  '''))

    if entrance == 1:
        cursor.execute('''DELETE FROM expenses_tbl WHERE number_expenses = :num_factor ''' , {'num_factor':num_factor})
        conx.commit()
        print('Invoice deleted')
    elif entrance == 2:
        choises = int(input('''1:expenses 2:category 3:about 4:date
choice a number :   '''))

        if choises ==1 :
            new_value = int(input('enter new value : '))
            cursor.execute('''UPDATE  expenses_tbl SET expenses= :new_value WHERE number_expenses = :num_factor ''' , {'new_value' : new_value ,'num_factor':num_factor})
            conx.commit()
            print('Invoice updated')            
        if choises ==2 :
            new_value = input('enter new value : ')
            cursor.execute('''UPDATE  expenses_tbl SET category= :new_value WHERE number_expenses = :num_factor ''' , {'new_value' : new_value,'num_factor':num_factor})
            conx.commit()
            print('Invoice updated') 
        if choises ==3 :
            new_value = input('enter new value : ')
            cursor.execute('''UPDATE  expenses_tbl SET about= :new_value WHERE number_expenses = :num_factor ''' , {'new_value' : new_value,'num_factor':num_factor})
            conx.commit()
            print('Invoice updated') 
        if choises ==4 :
            new_value = input('enter new value : ')
            cursor.execute('''UPDATE  expenses_tbl SET [date]= :new_value WHERE number_expenses = :num_factor ''' , {'new_value' : new_value,'num_factor':num_factor})
            conx.commit()
            print('Invoice updated') 



try:
    create_table()
    while True:
        entrance=int(input('''        welcome to chortke
        1 : Add invoice
        2 : Show invoice 
        3 : Update and delete invoice
        0 : exit
        choice a number :  '''))
        
        if entrance == 1 :
            expenses = input('+ spending  : ')
            category = input('+ category : ')
            about = input ('+ about spending : ')
            choises_date = input('If you want to save with today\'s, enter number 1,\n \t otherwise enter the desired date : ')
            if len(choises_date) != 1:
                date = choises_date
            else:
                date = jdatetime.date.today()

            add(expenses,category,about , str(date))
        
        elif entrance == 2:
            category = input(' category (see all send all) : ')
            expens = show(category)
            for expen in expens[0]:
                print(expen)
            print(expens[1])
        elif entrance == 3:
            num_factor = int(input('number invoice :'))
            update_expenses(num_factor)
        elif entrance == 0:
            break

except ValueError :
    print('select a number !!!!')