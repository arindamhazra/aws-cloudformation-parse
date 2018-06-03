from __future__ import print_function
import yaml
import os,json,webbrowser
import platform
import tempfile
import sys
import pydot

TEMPLATE_FRAGMENTS = ['AWSTemplateFormatVersion','Description','Metadata','Parameters','Mappings','Conditions','Transform','Resources','Outputs']
POWERFUL_ACTIONS = ["config:DeleteConfigRule","lambda:AddPermission","lambda:DeleteFunction","lambda:InvokeFunction",
                    "kms:CreateKey","kms:Decrypt","kms:DisableKey","athena:DeleteNamedQuery","dynamodb:CreateBackup",
                    "dynamodb:DeleteBackup","dynamodb:DeleteItem","dynamodb:DeleteTable","dax:DeleteCluster","dax:DeleteItem",
                    "dax:DeleteParameterGroup","dax:DeleteSubnetGroup","dax:RebootNode","ec2:CreateCustomerGateway",
                    "ec2:CreateDefaultSubnet","ec2:CreateDefaultVpc","ec2:CreateDhcpOptions","ec2:CreateEgressOnlyInternetGateway",
                    "ec2:CreateNetworkAcl","ec2:CreateNetworkAclEntry","ec2:CreateRoute","ec2:CreateRouteTable","ec2:CreateSubnet",
                    "ec2:CreateVpc","ec2:CreateVpcEndpoint","ec2:DeleteCustomerGateway","ec2:DeleteDhcpOptions","ec2:DeleteEgressOnlyInternetGateway",
                    "ec2:DeleteFlowLogs","ec2:DeleteNetworkAcl","ec2:DeleteNetworkAclEntry","ec2:DeleteRoute","ec2:DeleteRouteTable",
                    "ec2:DeleteSecurityGroup","ec2:DeleteSubnet","ec2:DeleteVpc","ec2:DeleteVpcEndpoints","ec2:DeleteVpcPeeringConnection",
                    "ec2:DeleteVpnConnection","ec2:DeleteVpnConnectionRoute","ec2:DeleteVpnGateway","cloudformation:DeleteStack","iam:DeleteSAMLProvider",
                    "iam:DeleteSSHPublicKey","config:*","lambda:*","kms:*","athena:*","dynamodb:*","dax:*","ec2:*","cloudformation:*","iam:*","s3:*"]
AWS_RESOURCES =     ["*","arn:aws:ec2:*:*:*","arn:aws:config:*:*:*","arn:aws:kms:*:*:*","arn:aws:lambda:*:*:*","arn:aws:dynamodb:*:*:*","arn:aws:iam:*:*:*",
                    "arn:aws:cloudformation:*:*:*"]

os.environ["PATH"] += os.pathsep + 'C:\\Program Files (x86)\\Graphviz2.38\\bin\\'
cfnFilePath = sys.argv[1]
filename = 'file:///'+tempfile.gettempdir()+'\\CloudFormationSummary.html'
outFilePath = tempfile.gettempdir()+'\\CloudFormationSummary.html'
imgPath = tempfile.gettempdir()+'\\cfn-resource-mapping.png'
htmlFile = open(outFilePath,'w')


def draw_graph(g_dict,imgPath):
    try:
        if (len(g_dict) > 10):
            graph = pydot.Dot(graph_type='digraph',rankdir='LR',dpi = 150)
        else:
            graph = pydot.Dot(graph_type='digraph',dpi = 150)
        root_node = pydot.Node("Main Stack", color="red",shape='box',fontname='Courier', fontsize='8',height=".5")
        graph.add_node(root_node)
        for k,v in g_dict.items():
            resourceType = "'"+v['ResourceType']+"'"
            node = pydot.Node(v['ResourceName'], color="green",shape='box',fontname='Courier', fontsize='8',height=".5")
            graph.add_node(node)
            if (v['DependsOn'] != 'NA'):
                dependsOn = (v['DependsOn'])
                if (isinstance(dependsOn, list)):
                    for d in dependsOn:
                        graph.add_edge(pydot.Edge(d,node, labelfontcolor="#f00", fontsize="6.5", color="red",style="dashed"))
                else:
                    graph.add_edge(pydot.Edge(dependsOn,node, labelfontcolor="#f00", fontsize="6.5", color="red",style="dashed"))
            graph.add_edge(pydot.Edge(root_node, node, label= resourceType, labelfontcolor="#fff", fontsize="6.5", color="blue"))
        graph.write(imgPath, format='png')
    except pydot.Error as e:
        print(e)

def visualize_file(fname):
    webbrowser.open_new_tab(fname)

def general_constructor(loader, tag_suffix, node):
    return node.value

def validate_yaml(fPath):
    with open(fPath, 'r') as stream:    
        try:
            yaml.safe_load(stream)
            return True
        except:
            return False

def validate_json(fPath):
    with open(fPath, 'r') as stream:    
        try:
            json.load(stream)
            return True
        except:
            return False

def save_html(htmlMessage):
    htmlFile.write(htmlMessage)
    htmlFile.close() 

def cfn_parsing(fType,cfnFPath,htmlMessage):
    graph_dict = {}
    htmlMessage += """<p>Click <a img href="""+imgPath+""" target = '_blank' > here </a> for Cloudformation stack diagram</p>
    <table><tr><th colspan='5'>General Information</th></tr>"""
    with open(cfnFPath, 'r') as stream:    
        try:
            if(fType == "json"):
                cfn_data = json.load(stream)
            else:
                cfn_data = yaml.safe_load(stream)

            for k,v in cfn_data.items():
                if(k == 'AWSTemplateFormatVersion'):
                    cfnVersion = v
                    htmlMessage += "<tr><td>AWS Template Format Version</td><td colspan='4'>"+cfnVersion+"</td></tr>"
                elif(k == 'Description'):
                    cfnDescription = v 
                    htmlMessage += "<tr><td>AWS Template Description</td><td colspan='4'>"+cfnDescription+"</td></tr>"
                elif(k == 'Parameters'):            
                    paramCount = len(v)
                    if (int(paramCount) > 0):
                        htmlMessage += "<tr style='text-align:center'><th colspan='5'>Parameters("+str(paramCount)+")</th></tr>"
                        htmlMessage += "<tr><th>Parameter Name</th><th colspan='4'>Parameter Type</th></tr>"
                    for param_key,param_val in v.items():
                        for param_key_1,param_val_1 in param_val.items():
                            cfnParamName = param_key
                            if (param_key_1 == 'Type'):                            
                                cfnParamType = param_val_1
                                htmlMessage += "<tr><td>"+cfnParamName+"</td><td colspan='4'>"+cfnParamType+"</td></tr>"
                elif(k == 'Resources'):
                    resouceCount = len(v)
                    if (int(resouceCount) > 0):
                        htmlMessage += "<tr style='text-align:center'><th colspan='5'>Resources("+str(resouceCount)+")</th></tr>"
                        htmlMessage += "<tr><th>Resource Type</th><th>Resource Logical Name</th><th>Depends On</th><th>Comments</th><th>Properties</th></tr>"               
                    for res_key,res_val in v.items():
                        cfnResType = cfnResDependsOn = cfnResProperties = "NA"
                        prohibitedAction = False
                        for res_key_1,res_val_1 in res_val.items():
                            cfnResVarName = res_key
                            graph_dict[cfnResVarName] = {}                                        
                            if (res_key_1 == 'Type'):                            
                                cfnResType = res_val_1
                            if (res_key_1 == 'DependsOn'):
                                cfnResDependsOn = res_val_1
                            if (res_key_1 == 'Properties'):
                                cfnResProperties = res_val_1
                                if(cfnResType == 'AWS::IAM::Role'):
                                    for poldoc in res_val_1['Policies']:
                                        for polstatement in (poldoc['PolicyDocument']['Statement']):
                                            if(polstatement['Effect'] == 'Allow' and (polstatement['Resource'] in AWS_RESOURCES)):
                                                for act in polstatement['Action']:
                                                    if act in POWERFUL_ACTIONS:
                                                        prohibitedAction = True

                            graph_dict[cfnResVarName]['ResourceName'] = cfnResVarName
                            graph_dict[cfnResVarName]['ResourceType'] = cfnResType
                            graph_dict[cfnResVarName]['DependsOn'] = cfnResDependsOn
                        if (prohibitedAction):
                            htmlMessage += "<tr style='color:#f00' ><td><div style='word-break:break-all;'>"+cfnResType+"</div></td><td>"+cfnResVarName+"</td><td>"+str(cfnResDependsOn)+"</td><td>warning:Powerful Action </td><td><div style='word-break:break-all;'>"+str(cfnResProperties)+"</div></td></tr>"
                        else:
                            htmlMessage += "<tr><td><div style='word-break:break-all;'>"+cfnResType+"</div></td><td>"+cfnResVarName+"</td><td>"+str(cfnResDependsOn)+"</td><td></td><td><div style='word-break:break-all;'>"+str(cfnResProperties)+"</div></td></tr>"
                elif(k == 'Outputs'):
                    outputCount = len(v)
                    if (int(outputCount) > 0):
                        htmlMessage += "<tr style='text-align:center'><th colspan='5'>Outputs("+str(outputCount)+")</th></tr>"
                        htmlMessage += "<tr><th>Output Logical Name</th><th colspan='4'>Output Value</th></tr>" 
                    for out_key,out_val in v.items(): 
                        cfnOutName = out_key
                        for out_key_1,out_val_1 in out_val.items():                            
                            if(out_key_1 == 'Value'):
                                cfnOutValue = out_val_1
                        htmlMessage += "<tr><td>"+str(cfnOutName)+"</td><td colspan='4'>"+str(cfnOutValue)+"</td></tr>"
                elif(k == 'Conditions'):
                    conditionsCount = len(v)
                    if (int(conditionsCount) > 0):
                        htmlMessage += "<tr style='text-align:center'><th colspan='5'>Conditions("+str(conditionsCount)+")</th></tr>"
                        htmlMessage += "<tr><th>Condition Name</th><th colspan='4'>Condition Value</th></tr>" 
                    for con_key,con_val in v.items(): 
                        htmlMessage += "<tr><td>"+str(con_key)+"</td><td colspan='4'>"+str(con_val)+"</td></tr>"                                            
                else:
                    pass
            htmlMessage += "</table></div></body></html>"
            draw_graph(graph_dict,imgPath)
            save_html(htmlMessage)
            visualize_file(filename)
        except:
            htmlMessage += "<h3 style='color:red;text-align:left'>Error: Something went wrong.Please try later!</h3></div></body></html>"
            save_html(htmlMessage)
            visualize_file(filename)



htmlMessage = """<html><head><title>Cloudformation Template Summary Report</title><style>table, th, td {
                    border: 1px solid black;border-collapse: collapse;} th { background: #F5B041;color: #1C2833} 
                    main_th { background: #D35400;} th,td,h1,h3 {font-family:  Arial, Helvetica, sans-serif;} table { table-layout: fixed;} 
                    td { border: 1px solid; word-wrap: break-all} .content { max-width: 80%;
                    margin: auto; background: #FDEBD0;padding: 8px; text-align:left;font-family: Arial, Helvetica, sans-serif;}
                    </style></head><body><div class="content">
                    <h1 style="text-align:center"> Cloudformation Template Summary Report</h1>
                    Cloudformation Template File =  """+cfnFilePath

if (not(os.path.exists(cfnFilePath))):
    htmlMessage += "<p style='color:red;text-align:left'>Error: File "+cfnFilePath+" does not exist.Please check file path and try again!</p></div></body></html>"
    save_html(htmlMessage)
    visualize_file(filename)
    sys.exit(1)

file_extension = (os.path.splitext(cfnFilePath))[1]
if(file_extension == ".yaml"):
    yaml.SafeLoader.add_multi_constructor(u'!',general_constructor)
    if(validate_yaml(cfnFilePath)):
        htmlMessage += "<p style='color:green;text-align:left'> "+cfnFilePath+" is a valid YAML file.</p>"
        cfn_parsing("yaml",cfnFilePath,htmlMessage)
    else:
        htmlMessage += "<p style='color:red;text-align:left'>Error: "+cfnFilePath+" is not a valid YAML file.Please check the file and try again!</p></div></body></html>"
        save_html(htmlMessage)
        visualize_file(filename)
        sys.exit(1)
elif(file_extension == ".json" or file_extension == ".template"):
    if(validate_json(cfnFilePath)):
        htmlMessage += "<p style='color:green;text-align:left'> "+cfnFilePath+" is a valid JSON/Template file.</p>"
        cfn_parsing("json",cfnFilePath,htmlMessage)        
    else:
        htmlMessage += "<p style='color:red;text-align:left'>Error: "+cfnFilePath+" is not a valid JSON/Template file.Please check the file and try again!</h3></div></body></html>"
        save_html(htmlMessage)
        visualize_file(filename)
        sys.exit(1)
else:
    htmlMessage += "<p style='color:red;text-align:left'>Error: "+cfnFilePath+" is not a valid Cloudformation Stack file.Please check the file and try again!</p></div></body></html>"
    save_html(htmlMessage)
    visualize_file(filename)
    sys.exit(1)



