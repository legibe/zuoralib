from bs4 import BeautifulSoup
from tagfinder import TagFinder, TagNotFound

def readfile(filename):
    with open(filename) as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        return soup

def extractContents(tag):
    contents = []
    for e in tag.contents:
        if hasattr(e,'contents'):
            contents += ' ' + extractContents(e) + ' '
        else:
            e = e.strip()
            if len(e):
                contents.append(e)
    return ''.join(contents)

def extractText(text):
    description = []
    for paragraph in text.find_all('p'):
        if hasattr(paragraph, 'contents'):
            t = extractContents(paragraph)
        else:
            t = paragraph
        if t.find('Type') != -1:
            break
        description.append(t)
    return '\n'.join(description)



text = readfile('/Users/claude/Desktop/sub.html')
table = TagFinder.find_at_least_one(text, 'table')
current = table[0]
rows = current.find_all('tr')
for row in rows:
    columns = row.find_all('td')
    if len(columns):
        fieldName = extractContents(columns[0])
        print fieldName
        description = columns[3]
        text = extractText(description)
        print text
        print
