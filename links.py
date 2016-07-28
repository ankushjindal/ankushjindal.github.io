import requests
from lxml.html import fromstring
import sys
from time import gmtime, strftime
import os
import argparse

try:
  parser = argparse.ArgumentParser(description='Process a link.')
  parser.add_argument('link', action="store", help="Specify the link to add")
  parser.add_argument('-d', '--deploy', action="store_true", default=False, help="To deploy or not") #deploy
  parser.add_argument('-t', '--title', action="store", dest="title", default=False, help="To provide a different tilte than the page header") #title
  parser.add_argument('--dry', action="store_true", default=False, help="Dry run, no write") #dry
  arguments = parser.parse_args()
  print(arguments)
except:
  print("Arg error")
  sys.exit(0)

try:
  link = arguments.link
  r = requests.get(link)
  tree = fromstring(r.content)
  title = arguments.title
  if not title:
    title = tree.findtext('.//title')
    if not title:
        title = link
  timestr = strftime("%Y-%m-%d", gmtime())
  new = "\t\t<br><i>" + timestr + "</i> <a href='" + link + "'>" + title + "</a>\n"
  print("Link fetched")
except:
  print("Link error")
  sys.exit(0)

if not arguments.dry:
  try:
    file = open("index.html","r+")
    data = file.read()
    print(new)
    # line number read and write
    file.write(new)
    file.close()
    print("File edited")
  except:
    print("File error")
    sys.exit(0)

  # try:
  if arguments.deploy:
    commitstr = "'Added link " + str(link)+"'"
    os.system("git commit -a -m "+commitstr)
    print("deploying "+commitstr)
    passfile = open("pass.txt","r")
    passdata = passfile.read().split()
    username = passdata[0]
    password = passdata[1]
    passfile.close()
    print("getting pass")
    pushstr = "https://"+str(username)+":"+str(password)+"@github.com/ankushjindal/ankushjindal.github.io.git"
    print("pushing")
    os.system("git push -u "+pushstr+" master")
  # except:
  #   print("Git/Pass error")
  #   sys.exit(0)
else:
  print(new)
