# django-book-library

Practice django project based on the Mozilla Developers Network introductory tutorial on Django.
This repo deals with a basic CRUD application that allows both the librarian(or staff) and students to view the books present in the 
local library. The students can see their borrowed books and the librarian has the access to renew a particular book.

Things I tried to experiment with on my own.
1. Added authentication for different groups of user and the admin panel.
2. The UI, used the django-widget-tweaks package along with bootstrap to redesign the UI.
3. Added the functionality for the students to view and write their own reviews about a book.

Steps to run:-
1. Clone the repo and redirect to that directory 
2. Initialise a virtual network
3. Install django and widget-tweaks
  
  ->pip install django
  ->pip install django-widget-tweaks
  
4. To run -> django manage.py runserver 
