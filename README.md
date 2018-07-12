# aws-cloudformation-parse
This is a python based AWS cloudformation stack parsing script.This script will parse through any cloudformation stack/template (JSON/YAML) and provide you am html report with following:
1. Validates input JSON/YAML file and reports it in the report
1. Summarize report of all the Parameters, Resources, and other Template Fragments
1. A diagram to visualize all resources and their dependency mappings
1. Checks for powerful actions and highlights it in the report

# Pre-requisites:
1. If GraphViz binaries are not available from some path, install (or extract portable) GraphViz from http://www.graphviz.org/download/. The module `pydot` relies on this application, for graphing
1. `pip install pydot, graphviz, pyaml`

Note: if the GraphViz `bin` folder is not in your `PATH`, you can either:
- leverage the `--graphvizBinFilespec` argument to specify the path to the GraphViz `bin` folder (useful if, say, the binaries are available on a network share or something); see Examples for an example

or

- add it to your `PATH`
    - on Windows, and for v2.38, for example, this bin directory is at `C:\Program Files (x86)\Graphviz2.38\bin` by default

# Input:
AWS cloudformation file path
Example:
```PowerShell
## evaluate the given config; assumes that GraphViz bin folder is in PATH
PS C:\> python.exe cfn_parser_visualizer.py 'c:\test\example-cloudformation.yaml'

## evaluate the given config, using the given GraphViz binaries folder
PS C:\> python.exe cfn_parser_visualizer.py 'c:\test\example-cloudformation.yaml' --graphvizBinFilespec \\someserver.dom.com\shared\GraphViz\bin
```

# Output:
Report Summary:
![Report Summary](https://github.com/arindamhazra/aws-cloudformation-parse/blob/master/Images/report.png)

Stack Diagram:
![Stack Diagram](https://github.com/arindamhazra/aws-cloudformation-parse/blob/master/Images/diagram.PNG)

# ToDo
- add `--verbose` support to function to improve potential experience for the curious