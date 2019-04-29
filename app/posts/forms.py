from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

class PostingForm(FlaskForm):
    title = StringField("Title", validators=[
        DataRequired(),
        Length(min=1, max=60, message="Must be more than 1 and less than 60 characters")])
    subtitle = StringField("Subtitle", validators=[
        Length(max=120, message="Must be less than 60 characters")])
    content = TextAreaField('Post text content', validators=[
        DataRequired(),
        Length(min=1, max=2000, message="Must be more than 1 and less than 2000 characters")])
    submit = SubmitField("Post")

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(60), nullable=False)
#     subtitle = db.Column(db.String(120), nullable=True)
#     content = db.Column(db.Text, nullable=False)
#     posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # class name with lowercase..
#
#     def __repr__(self):
#         return f"Post by user('{self.author.username}', dated '{self.posted_date}')"
# class EditPostButton(FlaskForm):
#     submit = SubmitField("Edit Post")
#     #
#     # def __init__(self, permission):
#     #     self.permission = permission
#
#     def validate_submit(self, submit):
#         pass
#
# class DeletePostButton(FlaskForm):
#     submit = SubmitField("Delete Post")
#
#     # def __init__(self, permission):
#     #     self.permission = permission
#
#     def validate_submit(self, submit):
#         pass
