from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,TextAreaField, SubmitField,ValidationError
from wtforms.validators import Required,Email
from flask_login import current_user
from ..models import User

class UpdateProfile(FlaskForm):
  username = StringField('Enter Your Username', validators=[Required()])
  email = StringField('Email Address', validators=[Required(),Email()])
  bio = TextAreaField('Write a brief bio about you...',validators = [Required()])
  submit = SubmitField('Update')

  def validate_email(self,email):
    if email.data != current_user.email:
      if User.query.filter_by(email = email.data).first():
        raise ValidationError("The Email has already been taken!")
    
  def validate_username(self, username):
    if username.data != current_user.username:
      if User.query.filter_by(username = username.data).first():
        raise ValidationError("The username has already been taken")

class CreateBlog(FlaskForm):
  title = StringField('Title',validators=[Required()])
  description = TextAreaField('Blog Description',validators=[Required()])
  content = TextAreaField('Blog Content',validators=[Required()])
  submit = SubmitField('Post')