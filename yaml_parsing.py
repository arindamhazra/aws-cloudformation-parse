from __future__ import print_function
import yaml
import os,json,webbrowser
import platform
import tempfile
import sys

TEMPLATE_FRAGMENTS = ['AWSTemplateFormatVersion','Description','Metadata','Parameters','Mappings','Conditions','Transform','Resources','Outputs']

cfnFilePath = sys.argv[1]

def general_constructor(loader, tag_suffix, node):
    return node.value

# yaml.SafeLoader.add_multi_constructor(u'!',general_constructor)
yaml.SafeLoader.add_multi_constructor(u'!Ref',general_constructor)
yaml.SafeLoader.add_multi_constructor(u'!Join',general_constructor)
yaml.SafeLoader.add_multi_constructor(u'!GetAtt',general_constructor)


outFilePath = tempfile.gettempdir()+"/CloudFormationSummary.html"
htmlFile = open(outFilePath,'w')
htmlMessage = """<html><head><title>Cloudformation Template Summary Report</title><style>table, th, td {
                border: 1px solid black;    border-collapse: collapse;} .content { max-width: 1000px;
                margin: auto; background: white; padding: 10px;}</style></head><body><div class="content">
                <h1 style="text-align:center"> Cloudformation Template Summary Report</h1>
                <h3>Cloudformation Template File =  """+cfnFilePath+"""</h3><table><tr><th colspan='4'>General Information</th></tr><tr><td>"""

with open(cfnFilePath, 'r') as stream:    
    try:
        yaml_data = yaml.safe_load(stream)
        for k,v in yaml_data.items():
            if(k == 'AWSTemplateFormatVersion'):
                cfnVersion = v
                htmlMessage += "AWS Template Format Version</td><td colspan='3'>"+cfnVersion+"</td></tr><tr><td>"
            elif(k == 'Description'):
                cfnDescription = v 
                htmlMessage += "AWS Template Description</td><td colspan='3'>"+cfnDescription+"</td></tr>"
            elif(k == 'Parameters'):            
                paramCount = len(v)
                if (int(paramCount) < 1):
                    paramCount = 0
                    htmlMessage += "<tr style='text-align:center'><th colspan='4'>Parameters("+str(paramCount)+")</th></tr>"
                else:
                    htmlMessage += "<tr style='text-align:center'><th colspan='4'>Parameters("+str(paramCount)+")</th></tr>"
                    htmlMessage += "<tr><th>Parameter Name</th><th colspan='3'>Parameter Type</th></tr>"
                for param_key,param_val in v.items():
                    for param_key_1,param_val_1 in param_val.items():
                        cfnParamName = param_key
                        if (param_key_1 == 'Type'):                            
                            cfnParamType = param_val_1
                            htmlMessage += "<tr><td>"+cfnParamName+"</td><td colspan='3'>"+cfnParamType+"</td></tr>"
            elif(k == 'Resources'):
                resouceCount = len(v)
                if (int(resouceCount) < 1):
                    resouceCount = 0
                    htmlMessage += "<tr style='text-align:center'><th colspan='4'>Resources("+str(resouceCount)+")</th></tr>"
                else:
                    htmlMessage += "<tr style='text-align:center'><th colspan='4'>Resources("+str(resouceCount)+")</th></tr>"
                    htmlMessage += "<tr><th>Resource Type</th><th>Resource Logical Name</th><th>Depends On</th><th>Properties</th></tr>"               
                for res_key,res_val in v.items():
                    cfnResType = cfnResDependsOn = cfnResProperties = "NA"
                    for res_key_1,res_val_1 in res_val.items():
                        cfnResVarName = res_key                      
                        if (res_key_1 == 'Type'):                            
                            cfnResType = res_val_1
                        if (res_key_1 == 'DependsOn'):
                            cfnResDependsOn = res_val_1
                        if (res_key_1 == 'Properties'):
                            cfnResProperties = res_val_1                                                    
                    htmlMessage += "<tr><td>"+cfnResType+"</td><td>"+cfnResVarName+"</td><td>"+cfnResDependsOn+"</td><td>"+str(cfnResProperties)+"</td></tr>"    
            elif(k == 'Outputs'):
                outputCount = len(v)
                if (int(outputCount) < 1):
                    outputCount = 0
                    htmlMessage += "<tr style='text-align:center'><th colspan='4'>Outputs("+str(outputCount)+")</th></tr>"
                else:
                    htmlMessage += "<tr style='text-align:center'><th colspan='4'>Outputs("+str(outputCount)+")</th></tr>"
                    htmlMessage += "<tr><th>Output Logical Name</th><th colspan='3'>Output Value</th><th></tr>" 
                for out_key,out_val in v.items(): 
                    cfnOutName = out_key
                    for out_key_1,out_val_1 in out_val.items():
                        
                        if(out_key_1 == 'Value'):
                            cfnOutValue = out_val_1
                    htmlMessage += "<tr><td>"+str(cfnOutName)+"</td><td colspan='3'>"+str(cfnOutValue)+"</td></tr>"                       
            else:
                print("Unknown Template Fragment")
        htmlMessage += "</table></div></body></html>"        
    except yaml.YAMLError as exc:
        print(exc)

htmlFile.write(htmlMessage)
htmlFile.close()

# filename = 'file:///'+os.getcwd()+'/' + 'CloudFormationSummary.html'
filename = 'file:///'+tempfile.gettempdir()+'/' + 'CloudFormationSummary.html'
webbrowser.open_new_tab(filename)