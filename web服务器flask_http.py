from flask import Flask, render_template, request, redirect, session
from gevent.pywsgi import WSGIServer
import random, time, os

app = Flask(__name__, static_url_path="/", static_folder="./")
app.config['SECRET_KEY'] = os.urandom(24)


@app.before_request
def before_request():
    with open("users.txt", "r") as f:
        users_list = f.read().splitlines()
    user = session.get('user')
    path = request.full_path
    with open("noLog_path.txt", "r") as f:
        notLog_path_list = f.read().splitlines()
    if user not in users_list and path not in notLog_path_list:
        return redirect('/hpnt/log')

 
@app.route("/")
def i():
    return render_template('i.html')


@app.route("/hpnt")
def a():
    return render_template('index.html', a="")


@app.route("/hpnt/log")
def login():
    return render_template('login.html')


@app.route("/hpnt/login",methods=["POST"])
def logpost():
    with open("users.txt", "r") as f:
        user_list = f.read().splitlines()
    username = request.form["username"]
    password = request.form["password"]
    if username in user_list:
        with open('users/' + username, 'r') as f:
            file = f.read()
        if password == file:
            print(username, password)
            session['user'] = username
            return redirect("/hpnt")
        else:
            print("no")
            return redirect('/hpnt/log')
    else:
        return redirect("/hpnt/log")


@app.route("/hpnt/chat")
def chat():
    return render_template('chat.html')


@app.route("/hpnt/download")
def download():
    return render_template('download.html')


@app.route("/hpnt/chattext", methods=['POST'])
def chattext():
    user = session.get("user")
    text = request.form["text"]
    l = [1, 2]
    r = random.choice(l)
    lt = time.strftime(" %Y-%m-%d %H:%M", time.localtime())
    if text == '':
        return redirect("/hpnt/chat")
    else:
        with open("liaotian.txt", "a", encoding='utf-8') as fi:
            fi.write(user+"："+text+"\n")
        with open("liaotian.js", "a", encoding='utf-8') as f:
            f.write("\n"
                    "var div = document.createElement('div');\n"
                    "div.innerText = '"+user+lt+"';\n"
                    "div.className = 'jia';\n"
                    "var yn_div = document.getElementById('nr');\n"
                    "yn_div.appendChild(div);\n"                        
                    "var div = document.createElement('div');\n"
                    "div.innerText = '"+text+"';\n"
                    "div.className = 'lt';\n"
                    "var yn_div = document.getElementById('nr');\n"
                    "yn_div.appendChild(div);\n")
        return redirect('/hpnt/chat')


@app.route("/hpnt/chatimg", methods=['POST'])
def chatimg():
    user = session.get("user")
    l = [1, 2]
    r = random.choice(l)
    lt = time.strftime(" %Y-%m-%d %H:%M", time.localtime())
    img = request.files.get('img')
    try:
        path = "./static/img/user/"+img.filename
        img.save(path)
    except Exception as e:        
        return redirect('/hpnt/chat')
    else:
        with open("liaotian.txt", "a", encoding='utf-8') as fi:
            fi.write(user+"："+"（文件）"+img.filename+"\n")
        with open("liaotian.js", "a", encoding='utf-8') as f:
            f.write("\n"
                    "var div = document.createElement('div');\n"
                    "div.innerText = '"+user+lt+"';\n"
                    "div.className = 'jia';\n"
                    "var yn_div = document.getElementById('nr');\n"
                    "yn_div.appendChild(div);\n"
                    "var div = document.createElement('a');\n"
                    "div.innerHTML = '请点击';\n"
                    "div.className = 'lt';\n"
                    "var yn_div = document.getElementById('nr');\n"
                    "yn_div.appendChild(div);\n"
                    "div.onclick = function(){window.open('/static/img/user/"+img.filename+"');};\n")
        return redirect('/hpnt/chat')


@app.route('/hpnt/logout')
def logout():
    session.pop('user')
    return redirect("/hpnt/log")


@app.route("/hpnt/account")
def account():
    user = session.get("user")
    return render_template("account.html", username=user)


@app.route('/hpnt/changepw')
def change_password():
    new_pw = request.form['new_pw']
    path = './user/' + session.get('user')
    with open(path, 'w') as f:
        f.write(new_pw)
    return redirect('/hpnt/log')



@app.route('/hpnt/trans')
def trans():
    query = request.args.get('query')
    to_lang = request.args.get('to_lang')
    if not query is None and not to_lang is None:
        from trans import trans
        dst = trans(query=query, to_lang=to_lang)
        return dst
    return "None"




@app.route("/hpnt/liaotian")
def liaotian():
    return render_template("liaotian.html")


if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 2052), app)
    server.serve_forever()
