# proj6-Gcal
Snarf appointment data from a selection of a user's Google calendars 

## What is here

I've provided code for the authorization (oauth2) protocol for Google
calendars.  There is also a picker for a date range. 

## What you'll add

You'll need to read the Google developer documentation to learn how to
obtain information from the Google Calendar service.

Your application should allow the user to choose calendars (a single
user may have several Google calendars, one of which is the 'primary'
calendar) and list 'blocking'  (non-transparent)
appointments between a start date and an end date
for some subset of them.

## Hints

You'll need a 'client secret' file of your own.  It should *not* be
under GIT control.  This is kind of a
developer key, which you need to obtain from Google.  See
https://auth0.com/docs/connections/social/google and
https://developers.google.com/identity/protocols/OAuth2 .
The applicable scenario for us is 'Web server applications'  (since
we're doing this in Flask).  

Your client secret will have to be registered for the URLs used for 
the oauth2 'callback' in the authorization protocol.  This URL includes
the port on which your application is running, so you you will need to 
use the same port each time you run your application. You can register 
the same key for multiple URLs, so for example I have registered mine
for localhost:5000/oauth2callback, localhost:8000/oauth2callback, 
roethke.d.cs.uoregon.edu:5000/oauth2callback, and 
roethke.d.cs.uoregon.edu:8000/oauth2callback. (Roethke is my raspberry Pi
at school.)  When we test your code, our grader and I will use our own 
admin_secrets.py and google credentials files, but we will use your 
client_secrets.py file.  As in the last project, your client_secrets.py
file should include a reference to your repository and to your name, 
so that our friendly (but clumsy) robots can use it to install your code. 

I have noticed that getting the list of calendars from Google is very very 
slow when running on my laptop at home, and snappier when accessing through
roethke.  I suspect that is because roethke.d.cs.uoregon.edu is is 
a routable IP address, while "localhost" on my home network requires some
behind-the-curtains magic from my home router.  I don't know that for sure. 

Whether or not you already have a Google calendar, it's a good idea to
create one or two 'test' calendars with a known set of appointments
for testing.



