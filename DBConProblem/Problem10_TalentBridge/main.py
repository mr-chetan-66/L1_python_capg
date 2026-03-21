# Please do not change the skeleton code given here.

import utility as ut
import talent_exception as ex
import talent_service as sr

def display(o):
   print("\n")
   print(f"Application Id: {o.get_application_id()}")
   print(f"Job Code: {o.get_job_code()}")
   print(f"Applicant Name: {o.get_applicant_name()}")
   print(f"Experience Grade: {o.get_experience_grade()}")
   print(f"Years Experience: {o.get_years_exp()}")
   print(f"Job Title: {o.get_job_title()}")
   print(f"Base Salary: {o.get_base_salary()}")
   print(f"Experince Bonus: {o.get_experience_bonus()}")
   print(f"Offered Salary: {o.get_offered_salary()}")
     
   
def main():
   record=ut.read_file("JobApplications.txt")
   obj=sr.TalentService()
   obj_l=obj.read_data(record)
   obj.add_application_details(obj_l)
   
   print("Top 3 Job Codes:")
   top=obj.find_top3_jobs()
   for k,v in top.items():
      print(f"{k} : {v}")
   
   aid=input("Enter the application id to search: ")
   try:
      ut.validate_application_id(aid)
      id_obj=obj.search_application(aid)
   
      if id_obj is None:
         print("Application not found")
      else:
         display(id_obj)
   except ex.InvalidApplicationIdException as e:
      print(e.get_message())
      
   s=ut.convert_date(input("Enter the start application date (DD/MM/YYYY): ")) 
   e=ut.convert_date(input("Enter the end application date (DD/MM/YYYY): "))  
   
   sr_obj=obj.find_senior_applicants(s,e)
   if sr_obj is None:
      print("No Applicant found with 7+ yr experience")
   else:
      print("Applicants with more than 7 years of experience: ")
      for k,v in sr_obj.items():
         print(f"{k} : {v}")
         
   gd=input("Enter the experience grade for salary update: ")
   g_obj=obj.update_offered_salary(gd)
   if g_obj is None:
      print("No update")
   else:
      print("The upgraded application details are: ")
      for o in g_obj:
         display(o)
         
   print("--------------Thanks You!--------------") 
   
if __name__ == "__main__":
    main()
