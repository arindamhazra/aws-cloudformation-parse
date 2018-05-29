from __future__ import print_function
import yaml
import os,json,webbrowser
import platform
import tempfile

TEMPLATE_FRAGMENTS = ['AWSTemplateFormatVersion','Description','Metadata','Parameters','Mappings','Conditions','Transform','Resources','Outputs']

def general_constructor(loader, tag_suffix, node):
    return node.value

yaml.SafeLoader.add_multi_constructor(u'!',general_constructor)

filePath = tempfile.gettempdir()+"/CloudFormationSummary.html"
print(filePath)
htmlFile = open(filePath,'w')
htmlMessage = """<html><head><title>Cloudformation Template Summary Report</title><style>table, th, td {
                border: 1px solid black;    border-collapse: collapse;} .content { max-width: 1000px;
                margin: auto; background: white; padding: 10px;}</style></head><body><div class="content">
                <h1 style="text-align:center"> Cloudformation Template Summary Report</h1>
                <table><tr><th>Template Fragment Type</th><th>Fragment Value(s)</th></tr><tr><td>"""

with open("c:\\code\\test.yaml", 'r') as stream:    
    try:
        yaml_data = yaml.safe_load(stream)
        # print(yaml_data)
        for k,v in yaml_data.items():
            if(k == 'AWSTemplateFormatVersion'):
                cfnVersion = v
                htmlMessage += "AWS Template Format Version</td><td>"+cfnVersion+"</td></tr><tr><td>"
            elif(k == 'Description'):
                cfnDescription = v 
                htmlMessage += "AWS Template Description</td><td>"+cfnDescription+"</td></tr>"
            elif(k == 'Parameters'):
                paramCount = len(v)
                Parameters = ""
                for param_key,param_val in v.items():
                    for param_key_1,param_val_1 in param_val.items():
                        if (param_key_1 == 'Type'):
                            Parameters = Parameters + param_key + "(" + param_val_1 + ")" "\n"
                print(paramCount)
                print(Parameters)
            elif(k == 'Resources'):
                resouceCount = len(v)
                print(v)
            else:
                print("Unknown Template Fragment")
        htmlMessage += "</table></div></body></html>"        
        # print("Version = %s , Description = %s , Parameters = %s" %(cfnVersion,cfnDescription,Parameters))
    except yaml.YAMLError as exc:
        print(exc)

htmlFile.write(htmlMessage)
htmlFile.close()

# filename = 'file:///'+os.getcwd()+'/' + 'CloudFormationSummary.html'
filename = 'file:///'+tempfile.gettempdir()+'/' + 'CloudFormationSummary.html'
webbrowser.open_new_tab(filename)