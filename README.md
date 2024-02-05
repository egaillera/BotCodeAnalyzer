# BotCodeAnalyzer
Simple Python script that receives as an argument a file with the source code of a Microsoft Bot Framework Bot dialog, written in TypeScript or C#, and generates an image with the flow of such dialog. It uses two LLM models working in a chain: first one analyzes the code and provide a description of the flow dialog; and the second one that takes the description provided by the first one, and write mermaid code to draw the diagram with the flow.

The script expects to find the OPENAI_API configuration parameters as environment variables, and the _mmdc_ executable (to generate the image through a mmd file) installed in the system.

```
usage: gen_diag.py [-h] [-f FILE] [-l {Typescript,C#}]

Code analyzer of bot dialogs

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File name with the code to analyze
  -l {Typescript,C#}, --language {Typescript,C#}
                        Programming language in which the code is written
```
