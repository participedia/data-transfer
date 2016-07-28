from bs4 import BeautifulSoup
import os, json
dirname = 'www.participedia.net'
for f in os.listdir(dirname):
    html_doc = open(dirname+'/'+f).read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    titles = soup.select("#page-title")
    if titles:
        title = titles[0].string
        if title == "Page not found": continue
        bodies = soup.select('.field-name-body .field-items .field-item')
        if bodies:
            body = bodies[0]
            blob = {'title': title, 'htmlbody': body.renderContents()}
            open(dirname+'/'+f+'.json', 'w').write(json.dumps(blob))
            print title
