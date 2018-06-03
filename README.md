# aws-cloudformation-parse
This is a python based AWS cloudformation stack parsing script.This script will parse through any cloudformation stack/template (JSON/YAML) and provide you am html report with following:
1. Validates input JSON/YAML file and reports it in the report
2. Summarize report of all the Parameters,Resources and other Template Fragments
3. A diagram to visualize all resources and their dependency mappings

# Pre-requisites:
1. install graphviz from http://www.graphviz.org/download/
2. Add C:\Program Files (x86)\Graphviz2.38\bin to PATH
3. pip install pydot
4. pip install graphviz

# Input:
AWS cloudformation file path
Example: python.exe cfn_parser_visualizer.py 'c:\test\example-cloudformation.yaml'

# Output:
Report Summary:
![Report Summary](https://github.com/arindamhazra/aws-cloudformation-parse/Images/report.png)

Stack Diagram:
![Report Summary](https://github.com/arindamhazra/aws-cloudformation-parse/Images/diagram.png)
