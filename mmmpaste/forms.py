from wtforms import Form, BooleanField, TextField, TextAreaField
from wtforms import validators

class NewPaste(Form):
    content = TextAreaField(None, [validators.Required()])
    filename = TextField("Filename")
    highlight = BooleanField("Syntax highlighting?", default = True)
    convert_tabs = BooleanField("Convert tabs to spaces?", default = True)
