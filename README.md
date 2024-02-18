1. DESCRIPTION
2. HOWT TO USE
3. USED TECHNOLOGIES/LIBRARIES AND IT'S VERSIONS
4. WHAT I LEARNED
________________________________________

## 1. DESCRIPTION
  My first projest using Django framework.
  
  It is a simple TO-DO web app with HTML/CSS frontend and django backend. 
  Project contains all CRUD functionalities. Data is stored in simple sqlite database for easier use.
  
  Project has task, comment and user objects. Each task status can be changed to done or not done by it's assigned user.
  Only assigned user can change status of task or edit it.
  
  Besides graphic interface there is built in API with JWT token authorization through cookie. Token is generated when user logs in and has a 60 minutes of validity period.

## 2. HOW TO USE
   
   2.1 WEB PAGE
   
     - You can run server locally from \to_do\todo_project directory using command 'python manage.py runserver localhost:[free port]
       
   2.2 API DOCUMENTATION
   
     Available operations:

      2.2.1:
   
         /api/register -> to register new user
         method: post
         required parameters: {'username','email','password'}
       
      2.2.2

        /api/login -> to login. It generates JWT token and stores it in a cookie.
         method: post
         required parameters: {'username','password'}
   
      2.2.3

         /api/task_list -> presents all tasks in JSON format
         method: get
         required parameters: {NONE}
   
      2.2.4

         /api/task_details/[task.id] -> presents task details in JSON
         method: get
         required parameters: {NONE}
   
      2.2.5

         /api/create_task -> allows you to create task.
         method: post
         required parameters: {'author.id','title','description','assigned_user.id'}
   
      2.2.6

         /api/update_task/[task.id] -> allows assigned user or superuser to update task
         method: post
         required parameters: {'author.id','title','description','assigned_user.id'}
   
      2.2.7

         /api/delete_task/[task.id] -> allows assigned user or superuser to delete task
         method: delete
         required parameters: {NONE}
   
      2.2.8

         /api/logout -> logs out user, and by that it means clearing cookie.
         method: post
         required parameters: {NONE}

  ## 3. USED TECHNOLOGIES/LIBRARIES AND IT'S VERSIONS


        Python 3.11.4
        Django version 4.2.4
        HTML, CSS
        django_rest_framework 3.14.0
        jwt
        datetime
        django-crispy-forms
        django-cors-headers
        django-widget-tweaks
      
  ## 3. WHAT I LEARNED 

        Project is actually my first ever touch with DJANGO, creating API and JWT tokens. 
        I learned that token can store id of user that authenticates with api, and thanks to that we can specify that some users can do specific operations and some don't
        For example in my project deleting and editing task should be only possible by user that is assigned to it. It is possible thanks to payload in JWT token.

        I had an opportunity to use Postman for the first time to test my API's and i think its a very pleasant to use tool.

        For the first time in a long time i worked with html/css and I remembered how to style my html a little, and adjust it for smaller devices like phones etc.

        
         
  
    
     
  
