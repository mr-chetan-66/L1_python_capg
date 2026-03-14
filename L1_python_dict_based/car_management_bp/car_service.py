# Please do not change the skelecton code given here
# You can add any number of methods and attributes as you required without changing the given template
import utility as ut
import car as cr
import sqlite3
from datetime import datetime,timedelta


##Creating Connection String
conn = sqlite3.connect("cardatabase.db")  # or :memory:
cursor = conn.cursor()

class CarService:
    
    def __init__(self):
        self.__discount_dict={}
    
    
    def read_data(self,file_obj):
       
        
        return None ##TODO: RETURN VALUE AS PER THE DESCRIPTION
    
    
    
    def add_car_details(self,car_obj):
        
        return None##TODO: RETURN VALUE AS PER THE DESCRIPTION
    
    
    
    
    def find_top3_rentals(self):
        # Write your code
        
        
        
        return None ##TODO: RETURN VALUE AS PER THE DESCRIPTION
    
    
    
    def find_closing_date(self,start_date,end_date):
        # Write your code
       
        return None##TODO: RETURN VALUE AS PER THE DESCRIPTION
    
    
    
    
   
        
	
