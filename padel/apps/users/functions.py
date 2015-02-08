from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage

def Login(request, username, password):
	user = authenticate(username = username, 
							password = password)
	if user:
		login(request, user)

def send_email(subject ,template,
							email,  token=None , name_content=None, content=None):
	msg = EmailMessage(subject=subject,from_email="PadelApp <mjeanc.104@gmail.com>",
            to=[email])
	msg.template_name = template
	if name_content:
		msg.template_content = {                  
				name_content : content 
			}
	msg.send()