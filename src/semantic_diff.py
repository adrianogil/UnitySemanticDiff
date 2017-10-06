
import sys, subprocess
import os
import fnmatch
from os.path import join

import yaml_parser
import parser_utils

unity_directory = "/Applications/Unity2017.2/Unity2017.2.app"
unity_merge_tool = unity_directory + "/Contents/Tools/UnityYAMLMerge"

print(unity_merge_tool)

scene_1 = sys.argv[1]
scene_2 = sys.argv[2]

print("Scene1: " + scene_1)
print("Scene2: " + scene_2)

diff_cmd = unity_merge_tool + ' diff "' + scene_1 + '" "' + scene_2 + '"'
print(diff_cmd)
diff_output = subprocess.check_output(diff_cmd, shell=True)
print(diff_output)


###### ########################
# Get all GUIDs from Metafiles
# Assumes that scene_1 and scene_2 are from the same project
for i in xrange(0,len(scene_1)):
    if scene_1[i:i+8] == '/Assets/':
        unity_path = scene_1[:i]
        break
print(unity_path)

assets_path = join(unity_path,"Assets");
project_settings_path = join(unity_path,"ProjectSettings");

files_by_guid = {}
guid_used = {}

print("Searching files in "+unity_path)

for root, subFolders, files in os.walk(assets_path):
    for filename in fnmatch.filter(files, '*.meta'):
        with open(join(root, filename)) as f:
            content = f.readlines()

        guid = ''
        for line in content:
            if line.find('guid:') != -1:
                guid = line[6:(len(line)-1)]
        # print(filename + ": " + guid)
        files_by_guid[guid] = join(root, filename)[:-5]
        guid_used[guid] = False

print("Found "+str(len(guid_used))+" guids")

###### ###############################
# Get all YAML section IDs from Metafiles
scene_1_data = {}
scene_1_data['yaml'] = yaml_parser.get_all_guid_files(unity_path, parser_utils.parse_project)
scene_1_data = yaml_parser.parse_yaml(scene_1, scene_1_data)

# import pdb; pdb.set_trace() # Start debugger

########################################
# Parse Yaml Diff
# 1) Get nested content
# 2) Parse numbers
# 3) Identify which number is a 


diff_lines = diff_output.split('\n')
for line in diff_lines:
    nested_level = 0
    for i in xrange(0, len(line)):
        s = line[i]
        # print s
        if s != ' ' and s != '\t':
            # Get number of spaces until content for each line
            print i
            nested_level = i
            break
    # for in xrange(nested_level+1, len(line)):
        
