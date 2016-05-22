import requests
from lxml.html import fromstring
import sys
from time import gmtime, strftime
from subprocess import call

try:
  link = sys.argv[1]
  r = requests.get(link)
  tree = fromstring(r.content)
  title = tree.findtext('.//title')
  if not title:
      title = link
  timestr = strftime("%Y-%m-%d %H:%M:%S", gmtime())
  try:
    file = open("index.html","r+")
    data = file.read()
    new = "<br><i>" + timestr + "</i><a href='" + link + "'>" + title + "</a>\n"
    file.write(new)
    try:
      try:
        deploy = sys.argv[2]
      except:
        deploy = False
      if deploy=="-d":
        commitstr = "Added link "+link
        call(["git","add","*"])
        call(["git","commit","-m",commitstr])
        try:
          passfile = open("pass.txt","r")
          passdata = passfile.read().split()
          username = passdata[0]
          password = passdata[1]
          pushstr = "https://"+str(username)+":"+str(password)+"@github.com/ankushjindal/ankushjindal.github.io.git"
          call(["git","push","-u",pushstr,"master"])
        except:
          print("Pass error")
    except:
      print("Git error")
  except:
    print("File error")
except:
  print("Link error")
