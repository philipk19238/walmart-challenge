import requests 
from requests.auth import HTTPBasicAuth
from flask import make_response, jsonify, session


class Api:

    def logged_in(self):
        if not session.get("username") or not session.get("password"):
            return False
        return True

    def get_login(self):
        return (session['username'], session['password'])

    def authenticate_user(self, username, password):
        authURL = "https://api.github.com/users"
        res = requests.get(authURL, auth=HTTPBasicAuth(username, password))
        res_json, status_code = res.json(), res.status_code
        if not status_code in [200, 201]:
            return self.get_error_resp(res_json, status_code)

        session['username'] = username
        session['password'] = password

        return res_json, status_code
        

    def get_data(self, URL):
        username, password = self.get_login()
        res = requests.get(URL, auth=HTTPBasicAuth(username, password))
        res_json, status_code = res.json(), res.status_code 
        if not status_code in [200, 201]:
            return self.get_error_resp(res_json, status_code), status_code
        return res_json, status_code 

    def get_num_issues(self, URL):
        data, status_code = self.get_data(URL)
        if not status_code in [200, 201]:
            return data, status_code
        if not data:
            return self.get_error_resp(data, status_code, manual_error="Invalid Company/Repository")
        num_issues = data["open_issues_count"]
        return int(num_issues), status_code        
        
    def parse_error(self, error):
        for key in error:
            curr = error[key]
            if isinstance(curr, dict):
                self.parse_error(curr)
            elif isinstance(curr, list):
                return curr[0]
            else:
                return curr

    def get_error_resp(self, res_json, status_code, manual_error=None):
        error = self.parse_error(res_json) if not manual_error else manual_error
        status_code = status_code if not manual_error else 400
        resp = make_response(jsonify({'error':error}), status_code)
        return resp, status_code


    