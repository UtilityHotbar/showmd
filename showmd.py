import argparse
import art
import markdown
from bs4 import BeautifulSoup
import colorama
from numpy import True_
from termcolor import colored
import shutil

colorama.init()
TERM_WIDTH = shutil.get_terminal_size((80, 20)).columns

def findstuff(elem):
    newstr = ''
    for child in elem.children:
        if child.name == 'a':
            newstr += colored(child.text + ' (' + child.get('href') + ')', 'white', 'on_yellow', attrs=['underline'])
        elif child.name == 'b' or child.name == 'strong':
            newstr += colored(child.text, attrs=['bold'])
        elif child.name == 'i' or child.name == 'em':
            newstr += colored(child.text, attrs=['underline'])
        elif child.name == 'pre' or child.name == 'code':
            newstr += colored(child.text, attrs=['reverse'])
        elif child.name == 'img':
            newstr += colored('[Image] ' + child.get('alt'), 'yellow', attrs=['reverse'])
        else:
            newstr += child.text
    return newstr

def makeart(text, font='medium', do_art=True):
    if not do_art:
        return colored(text, attrs=['reverse'])
        # return text
    # Base case, just try to turn the text into art and see if it's too wide
    baseart = art.text2art(text, font=font)
    if len(baseart.split('\n')[0]) <= TERM_WIDTH:
        return baseart
    # Now go line by line, editing until its under terminal width
    lines = text.split('\n')
    i = 0
    finished_art = ''
    while True:
        curr_line = lines[i]
        curr_art = art.text2art(curr_line, font=font)
        next = ''
        done = len(curr_art.split('\n')[0]) <= TERM_WIDTH
        while not done:
            if not curr_line:
                break
            next = curr_line[-1] + next
            curr_line = curr_line[:-1]
            curr_art = art.text2art(curr_line, font=font)
            if len(curr_art.split('\n')[0]) <= TERM_WIDTH:
                done = True
        if next:
            lines.insert(i+1, next)
        finished_art += curr_art+'\n'
        i += 1
        if i == len(lines):
            break      
    return finished_art  


parser = argparse.ArgumentParser(description='Display MD files.')
parser.add_argument('filename', help='name of the file to display.')
parser.add_argument('--a', dest='ascii', action='store_false', default=True, help='removes ascii art headers')

args = parser.parse_args()

with open(args.filename) as f:
    result = BeautifulSoup(markdown.markdown(f.read()), features="html.parser")
print(result.contents)
for elem in result.contents:
    if elem == '\n':
        continue
    if elem.name == 'h1':
        print(colored(makeart(elem.text, font='medium', do_art=args.ascii), 'blue'))
    elif elem.name == 'h2':
        print(colored(makeart(elem.text, font='small', do_art=args.ascii), 'green'))
    elif elem.name == 'h3':
        print(colored(makeart(elem.text, font='small', do_art=args.ascii), 'yellow'))
    elif elem.name.startswith('h'):
        print(colored(makeart(elem.text, font='straight', do_art=args.ascii), 'yellow'))
    elif elem.name == 'ul':
        for child in elem.children:
            if child.text != '\n':
                print(colored('* ' + findstuff(child), 'blue'))
    elif elem.name == 'ol':
        i = 1
        for child in elem.children:
            if child.text != '\n':
                print(colored(str(i) + '. ' + findstuff(child), 'blue'))    
                i += 1
    elif elem.name == 'p':
        print('\n'+findstuff(elem))
    else:
        print(findstuff(elem))