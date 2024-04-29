from flask import Flask, render_template, request
import strength_checker  # Import the module you created earlier

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        password = request.form['password']
        common_passwords = strength_checker.load_common_passwords()
        strength_ok, strength_message = strength_checker.check_password_strength(password)
        common_ok, common_message = strength_checker.check_common_passwords(password, common_passwords)

        if not strength_ok or not common_ok:
            message = strength_message if not strength_ok else common_message
        else:
            message = "Your password is strong and uncommon."

    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
