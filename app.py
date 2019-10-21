# -*- coding: utf-8 -*-
from flask import Flask,render_template, request, abort, make_response
from flask_limiter import Limiter
import json
from flask_limiter.util import get_remote_address
app = Flask(__name__)
limiter = Limiter(app,key_func=get_remote_address)
#
#
#
#
@app.route('/')
@limiter.limit('1/2second')
def main():
    Dict={}
    Dict["message1"]="Python FLASKのテンプレート"
    Dict["message2"]=["FLASKでサイトをつくるとapp.pyの行数が多くなりがちです。","そこでgetを利用し、HTMLを表示することにしました。"]
    return render_template("index.html",Dict=Dict)
#
#
#getを利用し、他ページへ遷移します
#Using "GET" method, the page will be navigated
@app.route('/trGet', methods=['GET'])
def transit_get():
    Dict={}
    import appTranstionPathwayGet
    if request.args.get("pathID"):
        print (request.args.get)
        Dict,html=appTranstionPathwayGet.pathwayFromGet(request.args)
    else:
        html="message.html"
        Dict["message1"]="Error1"
        Dict["message2"]="Error2"
    return render_template(html,Dict=Dict)
#
#
#Using "POST" method, the page will be shown
@app.route('/trPost', methods=['POST'])
@limiter.limit('1/2second')
def transit_post():
    if request.method == 'POST' :
        import appTranstionPathwayPost
        Dict={}
        for i in request.form.keys():
            Dict[i]=request.form[i]
        html,Dict=appTranstionPathwayPost.pathwayFromPost(Dict)
        ####if data contains cookie, let them eat
        #### クッキーがあったらいただきます。
        if "cookieName" in Dict.keys():
            print ("cookie done")
            responsePage=make_response(render_template(html,Dict = Dict))
            responsePage.set_cookie(Dict["cookieName"], json.dumps(Dict["cookieData"]))
            return responsePage
    else:
        print ("直接アクセス")
        Dict["message1"]="エラー"
        Dict["message2"]=["こちらは直接アクセスできません","ホームページからアクセスしてください"]
        html='message.html'
    return render_template(html,Dict=Dict)
###########################################################
#Error Transaction
#
#
@app.route('/403')
def abort403():
    abort(403)
@app.route('/404')
def abort404():
    abort(404)
@app.route('/500')
def abort500():
    abort(500)

@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    msg = 'Error: {code}\n'.format(code=error.code)
    return msg, error.code
@app.errorhandler(404)
def page_not_found(error):
    Dict={}
    Dict["message1"]="エラー"
    Dict["message2"]=["ページがみつかりません"]
    html='message.html'
    return render_template(html,Dict=Dict), 404
#
#
#
#############################################################
"""
"""
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
"""
########
"""
#http://127.0.0.1:5000/
"""
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
"""