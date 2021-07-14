# flask-half-full
<h3>Boiler plate Flask app ready with SQLAlchemy (+ User model), migration support, email Support, jQuery ready.</h3>
<p>Minimal work necessary to get connected to Postgres / start working.</p>

<p>To finish this you need: <br>
• A (free) Heroku account.</p>

<b>Step 1:</b><br>
Download this project / clone into this repository.

<b>Step 2:</b><br>
Create a free account with <a href="https://www.heroku.com/">Heroku</a>, or sign in with your existing account.

<b>Step 3:</b><br>
Create an app with Heroku. Give the app a relevent name.

<b>Step 4:</b><br>
Go to addons and search for and add Heroku Postgres. This is free up to a generous # of records / amount of storage.

<b>Step 5:</b><br>
Click on your Heroku Postgres addon go to Settings > View Credentials. You should see a URI that looks something like:
```postgres://randomstuff:morerandomstuff@some-ec2.amazonaws.com:random/stuff.```
Copy this URI.

<b>Step 6:</b><br>
Inside our application, find .env, and open it with a text editor.

You should see ```SQLALCHEMY_DATABASE_URI = ... ```. Set this variable equal to your URI with one fix... Change ```postgres``` to ```postgresql```.
In this same file, change the value assigned ```SECRET_KEY``` and ```SECURITY_PASSWORD_SALT``` to anything. 

Finally, this setup allows for email support through a private gmail account of your own. So use any gmail email / password for the ```MAIL_USERNAME``` and ```MAIL_PASSWORD``` environment variables. (You will probably have to configure this email account to "allow for less secure apps".)
It's important to note: This .env should be included in your .gitignore file. The purpose of this .env file is to keep your 
sensisitve information out of any remote repositories. These values are used in ```/config.py.```

<b>Step 7:</b><br>
Next go to the root directory of the project in your terminal and run ```pip install -r requirements.txt```.

<b>Step 8:</b><br>
Run ```flask db init```. A migrations folder should have been added to the project.

<b>Step 9:</b><br>
Run ```flask db migrate -m "First migration!"``` with the optional message after ```-m``` to add the User model in ```models.py``` to our database and prep this intial change for a commit / upgrade.

<b>Step 10:</b><br>
Run ```flask db upgrade```. Our updated database should get pushed to PostgreSQL.

<b>Step 11:</b><br>
Run ```flask run```.
The app should run on ```http://127.0.0.1:5000```.
It should look like this: 

<b>Step 12:</b><br>
Make an account with the register tab.

<b>Step 13:</b><br>
Make yourself an admin. In your terminal, run ```flask shell```.
This launches a python shell which we'll use to make you an admin. Do the following: 
```
from app.models import db, User
users = User.query.all()
users[0].admin = True
db.session.commit()
exit()
```
Now, once logged in, refresh the page and you should now see a link saying "admin".
Here is where you can display backend data if you choose to.

<b>Step 14:</b><br>
From here... You're ready to make changes to the contents of the project.
You'll notice in 'index.html', there is an example showing how to use jQuery to make ajax calls.
There's also some FlaskForms, a file upload route, ready for use. I will post more about the contents of this project soon.

Here is a working example of a website made with this basic structure: <a href='https://hannahisaband.herokuapp.com/'>HANNAH website</a>.






