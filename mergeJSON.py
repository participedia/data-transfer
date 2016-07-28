import os, json

dirname = 'www.participedia.net'
title2body = {}
for f in os.listdir(dirname):
    if '.json' in f:
        htmlData = json.loads(open(dirname+'/'+f).read())
        title2body[htmlData['title']] = htmlData['htmlbody']

def despacify(blob):
    newblob = {}
    for (k,v) in blob.items():
        newblob[k.replace(' ', '_')] = v
    return newblob

casedata = json.loads(open('newcases.json').read())
newcases = []
num = 0
for case in casedata['cases']:
    title = case['CaseID']
    if title in title2body:
        num += 1
        case['ArticleHTML'] = title2body[title]
    else:
        print "UNMATCHED CASE", title.encode('utf-8')
    newcases.append(despacify(case))
print "For Cases, Found", num, "matches out of", len(casedata['cases']), len(title2body.keys())
open('mergedcases.json', 'w').write(json.dumps({'cases': newcases}))


methoddata = json.loads(open('methods.json').read())
newmethods = []
num = 0
for method in methoddata['methods']:
    title = method['Title']
    if title in title2body:
        num += 1
        # print 'found match', title
        method['ArticleHTML'] = title2body[title]
    else:
        print "UNMATCHED METHOD", title.encode('utf-8')
    newmethods.append(despacify(method))
print "For Methods, Found", num, "matches out of", len(methoddata['methods']), len(title2body.keys())
open('mergedmethods.json', 'w').write(json.dumps({'methods': newmethods}))

orgdata = json.loads(open('organizations.json').read())
neworgs = []
num = 0
for org in orgdata['organizations']:
    title = org['Title']
    if title in title2body:
        num += 1
        # print 'found match', title
        org['ArticleHTML'] = title2body[title]
    else:
        print "UNMATCHED ORG", title.encode('utf-8')
    neworgs.append(despacify(method))
print "For Organizations, Found", num, "matches out of", len(orgdata['organizations']), len(title2body.keys())
open('mergedorgs.json', 'w').write(json.dumps({'organizations': neworgs}))
