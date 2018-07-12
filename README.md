# aws-cloudformation-parse
This is a python based AWS cloudformation stack parsing script.This script will parse through any cloudformation stack/template (JSON/YAML) and provide you am html report with following:
1. Validates input JSON/YAML file and reports it in the report
1. Summarize report of all the Parameters,Resources and other Template Fragments
1. A diagram to visualize all resources and their dependency mappings
1. Checks for powerful actions and highlights it in the report

# Pre-requisites:
1. Install graphviz from http://www.graphviz.org/download/. The module `pydot` relies on this application, for graphing
1. Add GraphViz `bin` directory to environment `PATH` (on Windows, and for v2.38, for example, this bin directory is at `C:\Program Files (x86)\Graphviz2.38\bin` by default)
1. pip install pydot, graphviz, pyaml

# Input:
AWS cloudformation file path
Example:
```PowerShell
PS C:\> python.exe cfn_parser_visualizer.py 'c:\test\example-cloudformation.yaml'
```

# Output:
Report Summary:
![Report Summary](https://github.com/arindamhazra/aws-cloudformation-parse/blob/master/Images/report.png)

Stack Diagram:
![Stack Diagram](https://github.com/arindamhazra/aws-cloudformation-parse/blob/master/Images/diagram.PNG)

# ToDo
- add `--verbose` support to function to improve potential experience for the curious