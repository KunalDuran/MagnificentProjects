from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class WhatsappUpload(FlaskForm):
    chat = FileField('Upload file', validators=[FileAllowed(['txt'])])
    submit = SubmitField('Upload chats')
