from app import app 
from flask import render_template, request, redirect, url_for, jsonify, session, make_response
from app.utils.api import Api 

@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    api = Api()
    if api.logged_in():
        return redirect(url_for('.home'))
    return render_template('login_page.html')

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    api = Api()
    if request.method == 'POST':
        login_json = request.get_json()
        username = login_json["username"]
        password = login_json["password"]
        data, status_code = api.authenticate_user(username, password)
        if not status_code in [200, 201]:
            return data
        resp = make_response(jsonify({"redirect":"/home"}), 200)
        return resp


@app.route('/company/<company_name>/<repo_name>/<page_num>', methods=['POST', 'GET'])
def company_issues(company_name, repo_name, page_num):
    api = Api()

    if not api.logged_in():
        return redirect(url_for('.login'))

    base = app.config['BASE_URL']
    endpoint = f"{base}/{company_name}/{repo_name}"

    num_issue_data, status_code = api.get_num_issues(endpoint)

    if not status_code in [200, 201]:
        return num_issue_data 

    if not num_issue_data:
        resp = make_response(jsonify({'error':'No Issues'}), 400)
        return resp 

    num_pages, remainder = divmod(num_issue_data, 10)
    if not num_pages:
        total_pages = 1
    elif num_pages and remainder:
        total_pages = num_pages + 1
    else:
        total_pages = num_pages

    endpoint += f"/issues?page={page_num}&per_page=10"
    issue_data, status_code = api.get_data(endpoint)

    if not status_code in [200, 201]:
        return issue_data

    intro_text = f"{company_name}/{repo_name} -> {num_issue_data} Open Issues"

    return render_template(
        "company.html", 
        issue_data=issue_data, 
        total_pages=total_pages, 
        intro_text=intro_text)

@app.route('/issues/<company>/<repository>/<issue_id>', methods=['GET', 'POST'])
def issues(company, repository, issue_id):
    api = Api()

    if not api.logged_in():
        return redirect(url_for('.login'))

    base = app.config['BASE_URL']
    endpoint = f"{base}/{company}/{repository}/issues/{issue_id}"

    issue_data, status_code = api.get_data(endpoint)
    if not status_code in [200, 201]:
        return issue_data 

    comment_endpoint = endpoint + '/comments'
    
    comment_data, status_code = api.get_data(comment_endpoint)
    if not status_code in [200, 201]:
        return comment_data

    return render_template('issue_page.html', issue_data=issue_data, comment_data=comment_data)

@app.route('/home')
def home():
    api = Api()
    if not api.logged_in():
        return redirect(url_for('.login'))
    return render_template('homepage.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        resp = make_response(jsonify({"redirect":"/login"}), 200)
        return resp