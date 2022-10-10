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
    except Exception as E :
        print(E)

def parseString(yaml_content):
    """
    this function is parsing yuml string to python dict
    :param yaml_content: the string content
    :return: python dict of the parsed yuml
    """
    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError as exc :
        print("erreur in yaml loading ")
        print(exc)
    except Exception as E :
        print(E)


for tp in TEMPLATE_FILES :
    template= getParse(tp)
    yaml_file_name= [*template.keys()][0]
    yaml_path = glob.glob(DIR_YAML+"*{}.yaml".format(yaml_file_name))[0]
    yaml_dict= getParse(yaml_path)

    for list in yaml_dict["spec"]["generators"]:
        for elem in list["list"]["elements"]:
            if elem["name"] in template[yaml_file_name][elem["type"]].keys():

                img = template[yaml_file_name][elem["type"]][elem["name"]]["image"]
                tag = template[yaml_file_name][elem["type"]][elem["name"]]["tag"]
                custom = parseString(elem["customValues"])
                custom["image"]["repository"] = img

                # to resolve the configfile writings
                for config in custom["configFilesTree"] :
                    for conf in config["configFiles"].keys():
                        pass
                        #s il y a une solution pour les aut de ligne a appliquer dans la ligne suivante
                        #config["configFiles"][conf]= str(config["configFiles"][conf]).replace(r'\n', '\n')
                elem["customValues"] = custom
    try:
        with open(yaml_path.replace('.yaml', '_out.yaml'), "w") as out :
            yaml.dump(yaml_dict,out,  sort_keys=False)
            #out.write(yaml.dump(yaml_dict, sort_keys=False))
    except Exception as e :
        print(e)

