
import typer
import sys
import csv
import re
from markdownify import markdownify as md
from slugify import slugify

app = typer.Typer()

@app.command('demo')
def demo():
    # python cli/support.py demo

    csv.field_size_limit(sys.maxsize)

    totalLength = 0
    with open('./cli/exports/Docs_export.csv', mode ='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if len(lines[2]) == 0:
                continue

            markdown = '# ' + lines[1] + "\n\n" + md(re.sub("\n\n", "\n", lines[2]))
            
            totalLength = totalLength + len(markdown)

            f = open("./cli/transformed/docs/" + lines[0] + "-" + slugify(lines[1]) + ".md", "w")
            f.write(markdown)
            f.close()

            f = open("./cli/transformed/docs/" + lines[0] + "-" + slugify(lines[1]) + ".html", "w")
            f.write(lines[2])
            f.close()
    
    print("Total length: " + str(totalLength))

@app.command('demo2')
def demo():
    print("DEMO2!")

app()