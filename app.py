import cohere
import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) 


class Form(FlaskForm):
    text = StringField('Enter text to search', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = Form()

    if form.validate_on_submit():
        cohere_api_key = os.getenv("COHERE_API_KEY")

        if not cohere_api_key:
            return "Missing Cohere API key. Please set the COHERE_API_KEY environment variable."

        co = cohere.Client(cohere_api_key)

        text = form.text.data
        response = co.generate(
            model='command-nightly',
            prompt=text,
            max_tokens=300,
            temperature=0.9,
            k=0,
            p=0.75,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        output = response.generations[0].text
        return render_template('home.html', form=form, output=output)

    return render_template('home.html', form=form, output=None)


if __name__ == "__main__":
    app.run(debug=True)
