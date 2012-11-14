from wtforms import Form, BooleanField, TextField, TextAreaField
from wtforms import validators

def none(data):
    return None if data == "" else data

class NewPaste(Form):
    content = TextAreaField(None, [
        validators.Required("The paste cannot be empty.")
    ])
    filename = TextField("Filename", filters = [none])
    highlight = BooleanField("Syntax highlighting?", default = True)
    convert_tabs = BooleanField("Convert tabs to spaces?", default = True)
