import requests, os, glob, json, base64, time
import openai
from utils import delete, upload_file, gpt, dalle1, dalle2, convertFromSeconds # API AI
openai.api_key = os.getenv("API_KEY")
try:
  REPLURL = f"{os.environ['REPL_SLUG']}.{os.environ['REPL_OWNER']}.repl.co" # used to get the images from an URL.
except: REPLURL = "0.0.0.0"

# FLASK
try:
  with open("config.json") as f: # config
    data = json.load(f)
    print("\033[32m[config] Loaded\033[0m")
except: print("\033[1[config] Unable to load\033[0")

from flask import Flask, render_template, request, send_from_directory # webserver imports
from waitress import serve

app = Flask(__name__)

@app.route('/')
def index():
  """Renders the index page"""
  if data['lockdown']: return render_template("msg.html", shortmsg="Lockdown mode",msg="The server is currently in lockdown. Please come back later!", buttons=False, favi=data["favicon"], title=data["title"])
    
  return render_template("index.html", favi=data["favicon"], title=data["title"])

@app.route('/editor')
def editor():
  """Renders the editor page"""
  if data['lockdown']: return render_template("msg.html", shortmsg="Lockdown mode",msg="The server is currently in lockdown. Please come back later!", buttons=False, favi=data["favicon"], title=data["title"])
      
  return render_template("editor.html", favi=data["favicon"], title=data["title"])
@app.route('/generate')
def generate():
  """Generates images and renders them"""
  if data['lockdown']: return render_template("msg.html", shortmsg="Lockdown mode",msg="The server is currently in lockdown. Please come back later!", buttons=False, favi=data["favicon"], title=data["title"], mark=data["downloadMark"])
  else:
    
    start = time.time()
    prompt = request.args.get('desc')
    if prompt is not None: #check if a prompt was given
      icon = gpt(prompt)
      #delete()
      list1 = dalle1(2, icon)
      list2 = dalle2(2, icon)
      for i in list1:
        list2.append(i)
      logo1, logo2, logo3, logo4 = list2
    
      return render_template("generate.html", favi=data["favicon"], title=data["title"], url=REPLURL, logo1=logo1, logo2=logo2, logo3=logo3, logo4=logo4, time=round(time.time()-start))
    else: return render_template("msg.html", shortmsg="No prompt",msg="No prompt was given. Please provide a prompt so I can generate logo's!", buttons=True, favi=data["favicon"], title=data["title"])

@app.route('/images/<path:path>')
def send_image(path):
    if data['lockdown']: return render_template("msg.html", shortmsg="Lockdown mode",msg="The server is currently in lockdown. Please come back later!", buttons=False, favi=data["favicon"], title=data["title"])
      
    return send_from_directory('images', path)

@app.route('/assets/<path:path>')
def send_asset(path):
    if data['lockdown']: return render_template("msg.html", shortmsg="Lockdown mode",msg="The server is currently in lockdown. Please come back later!", buttons=False, favi=data["favicon"], title=data["title"])
      
    return send_from_directory('assets', path)

@app.errorhandler(404)
def page_not_found(e):
    if data['lockdown']: return render_template("msg.html", shortmsg="Lockdown mode",msg="The server is currently in lockdown. Please come back later!", buttons=False, favi=data["favicon"], title=data["title"])
    return render_template("msg.html", shortmsg="404",msg="It looks like the page you were looking for is not here D:", buttons=True, favi=data["favicon"], title=data["title"])

if __name__ == "__main__":
  #app.run('0.0.0.0',port=server_port)
  started=round(time.time())
  print(f"\033[32m[Waitress] serving on \033[0;36m\"{REPLURL}\"\033[0m at {convertFromSeconds(started)}")
  
  serve(app, port=8080)