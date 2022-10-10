#! /usr/bin/env python 
import os
import yaml
import pprint
import re
#os.system("git clone git@forge.in.asso-cocktail.org:dsiadm/caas/caas-argocd-apps.git ")
os.chdir("caas-argocd-apps/caas-apps/templates/caas-applications")

# Récupération 1 couple (type/name) et image 
trouple_name_type_image = []
with open ('caas-apps-adherent1.yaml', "r") as f:
    try:
        file_one = yaml.safe_load(f)
        for k in file_one['spec']['generators']:
            for iElem in k['list']['elements']:
                name = iElem['name']
                type_elm = iElem['type']
                trouple_name_type_image.append({'name': name, 'type': type_elm, 'new_image': ''})

    except yaml.YAMLError as exc:
        print ("not ok")


# Récupératon 2 image pour type spécifique récupéré dans recupération 1 
with open('template_image.yaml', "r") as t:
    try:
        template = yaml.safe_load(t)
        for elm in trouple_name_type_image:

            elm['new_image'] = template['adherent1'][elm['type']][elm['name']]['image']

    except yaml.YAMLError as exc:
        print ("not ok")
        
os.system("pwd")
# Replace image récupération 1 par récupération 2 
with open ('caas-apps-adherent1.yaml', "r") as f:
    try:
        file_one = yaml.safe_load(f)
        for i, k in enumerate(file_one['spec']['generators']):
            for j, iElem in enumerate(k['list']['elements']):
                for elm in trouple_name_type_image:
                    if iElem['name'] == elm['name'] and iElem['type'] == elm['type']:
                        cValue = iElem['customValues']
                        regex = re.compile(r"repository: .*")
                        regex_2 = regex.sub(f"\nrepository: {elm['new_image']}\n", cValue)
                        file_one['spec']['generators'][i]['list']['elements'][j]['customValues'] = regex_2
                        break
                    
    except yaml.YAMLError as exc:
        print (exc)

# Write
with open ('caas-apps-adherent11.yaml', "w") as f:
    f.writelines(yaml.dump(file_one))


#ton code pourri >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# #os.system("ls")



#########################################################################################################################################################
# Replace : 
#                         Fait de replacer quelque chose, de la remettre à sa place d'origine.
# Exemple : Ils ont beau avoir mis beaucoup d'énergie dans le replacement de mes livres, je vois que certains d'entre eux ne sont pas à la bonne place.
########################################################################################################################################################

                        # y = str(x)
                        # print(type(y))
                        #os.system("yq -i  'cData[image][repository] = "'"'"dev-0.115"'"'" ' caas-apps-adherent1.yaml ")
                        # with open ('template_image.yaml', "r") as t:
                        #     try:
                                
                        #         template_applications=yaml.safe_load(t)
                        #         x = template_applications['adherent1']['web-object']['mangue']
                        #         #print (template_applications)
                        #         #os.system("yq -i -y '. = "dev-0.115"' caas-apps-adherent1.yaml")
                        #     except yaml.YAMLError as exc:
                        #         print ("not ok")
                        #os.system("yq -i -y '.app1.tag = "dev-0.115"' caas-apps-adherent1.yaml")         

    # except yaml.YAMLError as exc:
    #     print ("not ok")
