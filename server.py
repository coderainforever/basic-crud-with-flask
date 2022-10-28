from flask import Flask, request, redirect

app = Flask(__name__)

nextId=4
topics = [
    {'id':1, 'title':'HTML', 'body': "I think html is awesome..."},
    {'id':2, 'title':'CSS', 'body': "I think css is awesome..."},
    {'id':3, 'title':'JS', 'body': "I think js is awesome..."}
]
# Template
def template(contents, content, id=None):
    contextUI= ''
    if id!=None:
        contextUI=f'''
        <li><a href="/update/{id}/">Update</a></li>
        <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></li>
        '''
    return f'''<!doctype html> 
        <html>
            <head>
                <title>My Flask Website</title>
            </head>
            <body>
                <h1><a href="/">Homepage</a></h1>
                <ol>
                    {contents}
                </ol>
                {content}
                <ul>
                    <li><a href="/create/">Create</a></li>
                    {contextUI}
                </ul>
            </body>
        </html>
        '''
def getContents():
    liTags=''
    for topic in topics:
        liTags = liTags+ f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags
# Root        
@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome!</h2>Hello world!')
# Read
@app.route('/read/<int:id>/')
def read(id):
    title=''
    body=''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}', id)
# Create   
@app.route('/create/', methods=['GET', 'POST'])
def create():
    if(request.method == 'GET'):
        content=''' 
        <form action="/create/" method="POST">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit" value="create"></p>
        </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title=request.form['title']
        body=request.form['body']
        newTopic={'id': nextId, 'title':title, 'body':body}
        topics.append(newTopic)
        url ='/read/'+str(nextId)+'/'
        nextId=nextId+1
        return redirect(url)
# Update
@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if(request.method == 'GET'):
        title=''
        body=''
        for topic in topics:
            if id==topic['id']:
                title=topic['title']
                body=topic['body']
                break
        content=f''' 
        <form action="/update/{id}/" method="POST">
            <p><input type="text" name="title" placeholder="title" value={title}></p>
            <p><textarea name="body" placeholder="body">{body}</textarea></p>
            <p><input type="submit" value="update"></p>
        </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title=request.form['title']
        body=request.form['body']
        for topic in topics:
            if id==topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url ='/read/'+str(id)+'/'
        return redirect(url)
# Delete    
@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id==topic['id']:
           topics.remove(topic)
           break
    return redirect("/")

app.run(debug=True)