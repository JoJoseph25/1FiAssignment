# User Signup



## RUN Intial Migrations
shell into the VM where app is hosted or the docker container into the root folder/working directory of the app (run.py pwd) 
Run follwing commands in case migrations not created:
    - cd ./models
    - alembic init ./migrations
    - move alembic.ini into migrations folder
    - edit env.py to have BASE_DIR at root of app and DB URL from env variables
    - cd ./models/migrations/
    - alembic revision --autogenerate
    - alembic upgrade head
Run follwing commands in case migrations exist:
    - alembic revision --autogenerate
    - alembic upgrade head
