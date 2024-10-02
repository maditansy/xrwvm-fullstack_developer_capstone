# IBM Full Stack Developer Professional Certificate Capstone Project
Car dealership website using Django and MongoDB - users can log in, log out, view and filter dealerships, and add/see reviews of the dealerships. A sentiment analyzer is incorporated to show the emotion behind each review as well.

## Topics Covered:
- Designing applications and their architecture 
- Creating web frontends with static and dynamic pages using HTML, CSS, JavaScript and REACT
- Implementing user management and authentication  
- Developing backend services and communicating with databases 
- Continuously Integrating and Deploying changes using CI/CD pipelines  
- Deploying serverless applications on Code Engine 
- Creating and invoking RESTful microservices

## To run:
3 Terminals needed:
1) MongoDB:
   - cd xrwvm-fullstack_developer_capstone/server/database
   - docker build . -t nodeapp
   - docker-compose up
     
2) Build the frontend:
  - cd xrwvm-fullstack_developer_capstone/server/frontend
  - npm install
  - npm run build
    
3) Run the server:
  - cd xrwvm-fullstack_developer_capstone/server
  - pip install virtualenv
  - virtualenv djangoenv
  - source djangoenv/bin/activate
  - python3 -m pip install -U -r requirements.txt
  - python3 manage.py makemigrations
  - python3 manage.py migrate
  - python3 manage.py runserver
