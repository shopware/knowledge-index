
import typer
import sys
import csv

from markdownify import markdownify as md
from slugify import slugify
from bs4 import BeautifulSoup

app = typer.Typer()

@app.command('demo')
def demo(input: str):
    # python cli/support.py demo

    csv.field_size_limit(sys.maxsize)

    files = {
        'Docs_export.csv': {
            'source': 'docs',
            'id': 0,
            'title': 1,
            'description': 2,
        },
        'Jira_Next.csv': {
            'source': 'jira-next',
            'id': 2,
            'title': 0,
            'description': 37,
        },
        'uservoice_comments.csv': {
            'source': 'uservoice-comments',
            'id': 0,
            'title': 3,
            'description': 1,
        },
        'uservoice_notes.csv': {
            'source': 'uservoice-notes',
            'id': 0,
            'title': 3,
            'description': 1,
        },
        'uservoice_suggestions.csv': {
            'source': 'uservoice-suggestions',
            'id': 0,
            'title': 1,
            'description': 2,
        },
    }

    totalLength = 0
    with open('./cli/exports/' + input, mode ='r', newline='', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        i = 0
        for lines in csvFile:
            i = i + 1

            #if i <= 2:
            #    print(lines)

            # skip first row
            if i == 1:
                continue

            fileConfig = files[input]
            endDir = "./cli/transformed/" + fileConfig["source"] + "/"

            title = lines[fileConfig["title"]]
            destination = lines[fileConfig["id"]] + "-" + slugify(lines[fileConfig["title"]])
            #print(title)
            
            content = lines[fileConfig["description"]].replace('\n\n', '\n')
            ##content = BeautifulSoup(content, "xml")
            ##content = content.prettify()

            #print(content)
            
            if len(content) == 0:
                continue

            markdown = '# ' + title + "\n\n" + md(content, heading_style='ATX').replace('\n\n', '\n')
            
            totalLength = totalLength + len(markdown)

            f = open(endDir + destination + ".md", "w")
            f.write(markdown)
            f.close()

            f = open(endDir + destination + ".html", "w")
            f.write(content)
            f.close()
    
    print("Total length: " + str(totalLength))

@app.command('demo2')
def demo():
    print("DEMO2!")

app()