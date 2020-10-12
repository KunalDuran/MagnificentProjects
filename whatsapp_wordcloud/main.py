from flask import Flask, render_template, redirect, url_for, request
from forms import WhatsappUpload
from whatsapp_analysis import analyze
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'alskdfhgljxcl13513'


@app.route('/', methods=['GET', 'POST'])
def whatsapp_upload():
    form = WhatsappUpload()
    if form.validate_on_submit():
        uploaded_chat = form.chat.data
        print(uploaded_chat.filename)
        filename = uploaded_chat.filename
        with open('uploaded_files/'+filename, 'wb') as file:
            file.write(uploaded_chat.read())
            analyze(filename)
        return redirect(url_for('whatsapp_output', filename=filename))
    return render_template('whatsapp_upload.html', form=form)


@app.route('/whatsapp_output', methods=['GET', 'POST'])
def whatsapp_output():
    print(request.args)
    print(request.args.get('filename'))
    filename = request.args.get('filename')
    imagename = os.path.splitext(filename)[0]
    imagename = imagename+'_image.jpg'
    print(imagename)
    return render_template('whatsapp.html', imagename=imagename)


if __name__ == "__main__":
    app.run(debug=True)
