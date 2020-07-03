from flask import Flask, render_template, redirect, url_for
from forms import WhatsappUpload
from whatsapp_analysis import analyze


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Somethingsecret'


@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_upload():
    form = WhatsappUpload()
    if form.validate_on_submit():
        uploaded_chat = form.chat.data
        with open('uploaded_files/uploaded_chat.txt', 'wb') as file:
            file.write(uploaded_chat.read())
            analyze()
        return redirect(url_for('whatsapp_output'))
    return render_template('whatsapp_upload.html', form=form)


@app.route('/whatsapp_output')
def whatsapp_output():
    return render_template('whatsapp.html')


if __name__ == "__main__":
    app.run(debug=True)
