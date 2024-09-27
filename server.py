from IPython.core.release import author
from flask import Flask, render_template, request, redirect, send_file, url_for
import pandas as pd

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email

from yc_webpage_scrape import YCWebpageScraper
import send_email

# Create an instance of YCWebpageScraper
yc = YCWebpageScraper()

# Global variables for contact status and author name
CONTACT_HANDSHAKE = False
AUTHOR = "Guene H."

# Initialize the Flask application
app = Flask(__name__)


# Define a route for "/yclive_scraper" to handle web scraping
@app.route("/yclive_scraper", methods=["post", "get"])
def yc_scraper():
    global name_provy
    global reversed_provy
    # Execute the scraping and save the data into a CSV file, overwriting any previous file
    saved_posts = yc.get_data()
    df = pd.DataFrame(saved_posts)
    df.to_csv("data.csv", mode='w', header=True)

    # Sort and read data for rendering
    yc.sorted_by()
    dati_letto = yc.leggi_sort()
    if request.method == "POST":
        data = request.form
        filter_name = data['selected_field']
        filter_order = data['selected_order']

        # Update sorting based on form selection
        if filter_order == 'True':
            yc.name_provy = filter_name
            yc.reversed_provy = True
        elif filter_order == 'False':
            yc.name_provy = filter_name
            yc.reversed_provy = False
        else:
            yc.name_provy = 'rank'
            yc.reversed_provy = True

        # Apply the sorting and read sorted data
        yc.sorted_by()
        dati_letto = yc.leggi_sort()

    # Render the scraped data in the template
    return render_template("yc_live_p.html", all_posts=dati_letto)


############
# CONTACT
############

# TODO: Implement a more secure and secret key for the app
app.secret_key = "yrvbrbvbkrbkjnnknkjnl86678hh88hbu.bhb"

# Define field options for the contact form
FIELD = ["job offer", "collaborazione", "altro"]


# Define a form for contact functionality
class ContactForm(FlaskForm):
    # Form fields with validation and placeholders
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    select_field = SelectField("field", validators=[DataRequired()], choices=FIELD)
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"placeholder": "Message", "rows": 4})
    submit = SubmitField('Send Message')


# Define a route for the contact page
@app.route("/contact", methods=["get", "post"])
def contact_page():
    global CONTACT_HANDSHAKE
    form = ContactForm()

    # Handle form submission
    if form.validate_on_submit():
        # Extract form data
        name = form.name.data
        email = form.email.data
        selected_field = form.select_field.data
        message = form.message.data
        # Package form data for email sending
        params_for_email = {"name": name, "email": email, "subject": selected_field, "message": message}
        send_email.SendEmail(**params_for_email)

        # Update handshake status to indicate successful form handling
        CONTACT_HANDSHAKE = True
        return redirect(url_for("home_page"))

    # Render contact form in the template
    return render_template("contact_p.html", form=form, author=AUTHOR)


# Define options for the next steps after sending email
choice_for_now = ["Donwload CV", "Home page", "Blog"]


# Form for handling actions after email submission
class EmailSuccess(FlaskForm):
    and_now_choice = choice_for_now
    and_now = SelectField("and now", validators=[DataRequired()], choices=and_now_choice)
    submit = SubmitField('Submit')
    submit_download = SubmitField('Download Guene CV')


# Route to handle post-email submission actions
@app.route("/success_send", methods=["GET", "POST"])
def success_send_page():
    global CONTACT_HANDSHAKE
    and_now_form = EmailSuccess()
    status_now_selected_1 = False

    # Check for form validation
    if and_now_form.validate():
        now_selected = and_now_form.and_now.data

        # Handle download CV option if handshake is successful
        if now_selected == choice_for_now[0]:
            if CONTACT_HANDSHAKE == True:
                path = "Guene Hassim CV.pdf"
                return send_file(path, as_attachment=True)

        # Redirect based on user selection
        elif now_selected == choice_for_now[1]:
            return redirect(url_for('home_page'))
        elif now_selected == choice_for_now[2]:
            return redirect(url_for('blog_page'))

    # Render email success page with options for further actions
    return render_template("email_sent.html", and_now_form=and_now_form, sent_email_status=CONTACT_HANDSHAKE,
                           author=AUTHOR)


### Home page route

@app.route("/", methods=['post', 'get'])
def home_page():
    global CONTACT_HANDSHAKE

    # Handle different form submissions on the home page
    if 'download_cv' in request.form:
        if CONTACT_HANDSHAKE == True:
            return redirect(url_for('download_page'))
        else:
            return redirect(url_for('contact_page'))
    elif 'visit_my_work' in request.form:
        return redirect(url_for('portfolio_page'))
    elif 'hire_me' in request.form:
        return redirect(url_for('contact_page'))
    else:
        return render_template('home_p.html', handshake_status=CONTACT_HANDSHAKE, author=AUTHOR)


### Portfolio page route
@app.route('/portfolio')
def portfolio_page():
    return render_template('portfolio_p.html', author=AUTHOR)


### Blog page route
@app.route('/blog')
def blog_page():
    return render_template('blog_p.html', author=AUTHOR)


### YC blog route with options to go to scraper or GitHub
@app.route('/ycblog', methods=["get", "post"])
def ycblog_page():
    if 'ycscraper_live' in request.form:
        return redirect(url_for('yc_scraper'))
    elif 'github' in request.form:
        return redirect('https://github.com/GueneHassim')
    return render_template('yc_blog_p.html', author=AUTHOR)


### YC live page route
@app.route('/yclive')
def yclive_page():
    return render_template('yc_live_p.html', author=AUTHOR)


### About site page route
@app.route('/aboutsite')
def aboutsite_page():
    return render_template('about_my_site_p.html', author=AUTHOR)


# Route to download CV file
@app.route("/download")
def download_page():
    path = "Guene Hassim CV.pdf"
    return send_file(path, as_attachment=True)


# Entry point to run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
