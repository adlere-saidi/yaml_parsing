#! /usr/bin/env python
# ce fichier est pour traiter lorsque chaque fichier a son template
import yaml, glob

#public variables
DIR_YAML = "caas-apps\\templates\\caas-applications\\"
# glob is module to search file's path using a patern, it returns a list
TEMPLATE_FILES = glob.glob(DIR_YAML+"template_*.yaml", recursive=False)

def getParse(path:str):
    """
    this function is just to open yuml file and parse it
    :param path: is the path of the yaml file
    :return: the dct object parsed of the file
    """
    try:
        with open(path, "r") as tf:
            return yaml.safe_load(tf)
    except yaml.YAMLError as exc :
        print("erreur in yaml loading ")
        print(exc)
    except Exception as e :
        print(e)


# we loop on the templates
for tp in TEMPLATE_FILES :
    # file du template parsed as dict
    template= getParse(tp)
    # we get the firs keys of the dict wich is the name of the correspondant file
    yaml_file_name= [*template.keys()][0]
    # we get the path of the file using glob ( even if the name is not standrised it needs only to have the {keyname}.yaml
    yaml_path = glob.glob(DIR_YAML+"*{}.yaml".format(yaml_file_name))[0]
    try:
        with open(yaml_path, 'r') as ymf:
            yaml_content = ymf.readlines()
            for i in range(len(yaml_content)):

                # on cherche la ligne ou il y'a image:
                if "image:" in yaml_content[i]:
                    # on extrait les infos type et nom des ligne i-2 et i-3
                    type , nom = str(yaml_content[i-2].split("type: ")[1]).replace("\n",""), yaml_content[i-3].split("- name: ")[1].replace("\n","")
                    repo = template[yaml_file_name][type][nom]["image"]
                    yaml_content[i+1]= yaml_content[i+1].split(":")[0]+": "+repo+"\n"

    except Exception as e :
        print(e)


    try:
        # to replace the same file use instead
        #with open(yaml_path, "w") as out:
        with open(yaml_path.replace('.yaml', '_out2.yaml'), "w") as out :
            out.writelines(yaml_content)
            #yaml.dump(yaml_content,out, sort_keys=False)
    except Exception as e:
        print(e)

