    """_ a little setup and update programs.
       wrote by gnabro Israel.
       date : 22 / 08 / 2026
       version: 1.0.0
    _
    """

import json
import shelve 
import requests 
import os
import sys
import subprocess

import plyer.notification as notifyer 




class Setup:
    """
    run the installation set up.
    try to find a new release of the app.

    """
    def __init__(self) -> None:

        "flag to run install_setup"
        self.can_run_install_setup = False

        # firstly read the setup.bin file to get the version of the software. --- task 1
        current_version: str | None = self.get_current_version()

        # secondly connect to github to download the content and setup.bin this should 
        # store a dict object. --- task 2
        new_version: str| None = self.get_new_version()

        # search for version in the dict object previously download and compare it to the current 
        # version of the app found in setup.bin --- task 3
        # if these are differents, download the app.exe file located at github. --- task 4
        self.download(current_version, new_version)

        # if the download of app.exe is performed, display a popup to install the new release --- task 5
        self.install_setup()


    def get_current_version(self, *args):
        """_perform task 1_
        """
        with shelve.open('setup.bin') as metadata:

          # return the version otherwise 
          if len(metadata):
            return metadata['version']

          # the file 'setup.bin' is corrupted or not build 
          metadata['version'] = '1.0.0'
          metadata['author'] = 'Gnabro Israel'
          metadata['email'] = 'ambroiseisrael5@gmail.com'
          metadata['about'] = 'extracteur de texte (contenu les fichiers .pdf et .docx) et de vidéo youtube.'

          # close the file
          metadata.close()

          return '1.0.0'      


    def get_new_version(self, *args):
        """_perform task 2_
        """
        # later I'll update it :)
        url = "https://raw.githubusercontent.com/Ambroise07/extractor/main/config/new.json"


        try: 
          # get the response object
          response = requests.get(url, timeout=5)

          if response.status_code == 200:
            print(response.text)

            version = json.loads(response.text)['version']
            return version

        except:
           return None
           

    def download(self, current_version:str, new_version:str):
        """_perform task 3_
        """
        if current_version == None or new_version == None:
          self.can_run_install_setup = False
          return 
          
        if (current_version != new_version):
          notifyer.notify(
            title='nouvelle version disponible',
            message='Une nouvelle version de cet logiciel sera installée dans quelque instant.',
            app_name='extracteur'
                      ) 
          exe_url = "https://raw.githubusercontent.com/Ambroise07/extractor/main/bin/app.exe"  

          try: 
            # response object
            response = requests.get(exe_url, timeout=5)

            if response.status_code == 200:
              with open('../bin/app.exe', 'wb') as exe_app:
                exe_app.write(response.content)

              self.can_run_install_setup = True

          except Exception:
            return None
            

          

    def install_setup(self, *args):
        """_perform task 5_
        """
        # if the can_run_install_setup is True
        # start installation 
        if self.can_run_install_setup:

          # Chemin vers l'exécutable qui vient d'être téléchargé
          chemin_exe = os.path.abspath('../bin/app.exe')
                     
          try:
            # Démarre le nouvel exécutable de manière indépendante
            subprocess.Popen([chemin_exe], shell=True)
                         
            # Ferme proprement l'ancienne version actuelle du logiciel
            sys.exit()

          except Exception as e:
            print('erreur du lancement ...', e)

          # do something here 
          self.can_run_install_setup = False
          
