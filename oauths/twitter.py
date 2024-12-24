import os
from flask import Flask, redirect, url_for, session, request, render_template_string
import tweepy

app = Flask(__name__)

# Secret key for Flask session
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the credentials from the form
        consumer_key = request.form['consumer_key']
        consumer_secret = request.form['consumer_secret']
        access_token = request.form['access_token']
        access_token_secret = request.form['access_token_secret']

        # Save credentials to session
        session['consumer_key'] = consumer_key
        session['consumer_secret'] = consumer_secret
        session['access_token'] = access_token
        session['access_token_secret'] = access_token_secret

        # Redirect to log in route to initiate the OAuth flow
        return redirect(url_for('login'))

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fomo Radio AI - Twitter OAuth</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f7f6;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: white;
                padding: 20px 40px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 600px;
                text-align: center;
            }
            h1 {
                color: #333;
                margin-bottom: 20px;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            label {
                text-align: left;
                font-weight: b;
                color: #555;
            }
            input {
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
                width: 100%;
                box-sizing: border-box;
            }
            button {
                background-color: #1DA1F2;
                color: white;
                font-size: 16px;
                padding: 12px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #0d95e8;
            }
            .form-group {
                display: flex;
                flex-direction: column;
                gap: 10px;
                align-items: flex-start;
            }
            .footer {
                margin-top: 20px;
                font-size: 14px;
                color: #888;
            }
            
            .note {
                margin-top: 30px;
                padding: 15px;
                background-color: #fdf8e7;
                border-left: 5px solid #f0a500;
                font-size: 16px;
                color: #333;
                text-align: left;
                box-sizing: border-box;
            }
            .note h4 {
                margin: 0;
                font-size: 18px;
                color: #333;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>Fomo Radio AI - Twitter OAuth</h1>
            <h4>Enter Your Twitter API Credentials</h4>
            <form method="POST">
                <div class="form-group">
                    <label for="consumer_key">Consumer Api Key:</label>
                    <input type="text" name="consumer_key" required>
                </div>
                <div class="form-group">
                    <label for="consumer_secret">Consumer Secret:</label>
                    <input type="text" name="consumer_secret" required>
                </div>
                <div class="form-group">
                    <label for="access_token">Client ID:</label>
                    <input type="text" name="access_token" required>
                </div>
                <div class="form-group">
                    <label for="access_token_secret">Client Secret:</label>
                    <input type="text" name="access_token_secret" required>
                </div>
                <button type="submit">Submit</button>
            </form>
            <div class="footer">
                <p>Enter your credentials to connect with Twitter API.</p>
            </div>
            <div class="note">
                <h4>Note:</h4>
                <ul>
                    <li><p>Ensure that the credentials you enter here are correct and match the keys generated in your Twitter Developer account. If you do not have an account, you can create one <a href="https://developer.twitter.com/en/apps" target="_blank">here</a>.</p></li>
                    <li><p>App Permissions should be set to <b>Read and write and Direct message</b> and type of app should be set to <b>Web App / Bot</b>.</p></li>
                    <li><p>Make sure that the callback URL is set to <b>http://127.0.0.1:5000/callback</b> and Website of your choice</p></li>
                </ul>
            </div>
        </div>

    </body>
    </html>
    """)


@app.route('/login')
def login():
    # Get credentials from session
    consumer_key = session.get('consumer_key')
    consumer_secret = session.get('consumer_secret')
    access_token = session.get('access_token')
    access_token_secret = session.get('access_token_secret')

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        return redirect(url_for('home'))  # Redirect to home if credentials are missing

    # Set up Tweepy OAuth handler with user-provided credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    try:
        # Get the URL for the Twitter OAuth authentication
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
        return redirect(redirect_url)
    except tweepy.TweepyException as e:
        return f'Error! Failed to get request token: {e}'


# Callback route that Twitter redirects to after the user authenticates
@app.route('/callback')
def callback():
    # Get credentials from session
    consumer_key = session.get('consumer_key')
    consumer_secret = session.get('consumer_secret')
    access_token = session.get('access_token')
    access_token_secret = session.get('access_token_secret')

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        return redirect(url_for('home'))  # Redirect to home if credentials are missing

    auth = tweepy.OAuthHandler(session['consumer_key'], session['consumer_secret'])
    auth.set_access_token(session['access_token'], session['access_token_secret'])
    request_token = session.get('request_token')
    auth.request_token = request_token

    verifier = request.args.get('oauth_verifier')

    try:
        auth.get_access_token(verifier)
        session['access_token'] = auth.access_token
        session['access_token_secret'] = auth.access_token_secret
        return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Fomo Radio AI - Twitter OAuth</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f7f6;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        background-color: white;
                        padding: 20px 40px;
                        border-radius: 8px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        width: 100%;
                        max-width: 900px;
                        text-align: center;
                    }
                    h1 {
                        color: #333;
                        margin-bottom: 20px;
                    }
                    pre {
                        background-color: #f4f4f4;
                        padding: 15px;
                        border-radius: 5px;
                        font-size: 16px;
                        white-space: pre-wrap;
                        word-wrap: break-word;
                        text-align: left;
                        margin-bottom: 20px;
                    }
                    button {
                        background-color: #1DA1F2;
                        color: white;
                        font-size: 16px;
                        padding: 12px 20px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        transition: background-color 0.3s;
                    }
                    button:hover {
                        background-color: #0d95e8;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Fomo Radio AI - Twitter OAuth</h1> 
                    <h4>Twitter API Credentials</h4>
                    <h4 style="text-align: left"> For Mac / Linux Users - Copy this to <b style="color: blue">env_mac.sh</b></h4>
<pre id="snippet">
export x_api_key="{{ session['consumer_key'] }}"
export x_api_secret="{{ session['consumer_secret'] }}"
export x_access_token="{{ session['access_token'] }}"
export x_access_token_secret="{{ session['access_token_secret'] }}"
</pre>
                    <button onclick="copyToClipboard()">Copy to Clipboard</button>
                    <h4 style="text-align: left"> For Windows Users - Copy this to <b style="color: blue">env_win.sh</b></h4>
<pre id="snippet-win">
set x_api_key="{{ session['consumer_key'] }}"
set x_api_secret="{{ session['consumer_secret'] }}"
set x_access_token="{{ session['access_token'] }}"
set x_access_token_secret="{{ session['access_token_secret'] }}"
</pre>
                    <button onclick="copyToClipboardWin()">Copy to Clipboard</button>
                </div>

                <script>
                    function copyToClipboard() {
                        const snippet = document.getElementById("snippet");
                        const range = document.createRange();
                        range.selectNode(snippet);
                        window.getSelection().removeAllRanges(); 
                        window.getSelection().addRange(range);
                        document.execCommand("copy");
                        alert("Credentials copied to clipboard!");
                    }
                    function copyToClipboardWin() {
                        const snippet = document.getElementById("snippet-win");
                        const range = document.createRange();
                        range.selectNode(snippet);
                        window.getSelection().removeAllRanges(); 
                        window.getSelection().addRange(range);
                        document.execCommand("copy");
                        alert("Credentials copied to clipboard!");
                    }
                </script>
            </body>
            </html>
            """)
    except tweepy.TweepyException as e:
        return f'Error! Failed to get access token: {e}'


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
