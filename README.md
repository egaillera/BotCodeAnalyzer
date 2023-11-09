# BotCodeAnalyzer
Simple Python script that receives as an argument a file with the source code of a Microsoft Botframework Bog dialog, written in TypeScript or C#, and generates an image with the flow of such dialog
```
usage: gen_diag.py [-h] [-f FILE] [-l {Typescript,C#}]

Code analyzer of bot dialogs

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File name with the code to analyze
  -l {Typescript,C#}, --language {Typescript,C#}
                        Programming language in which the code is written
```
