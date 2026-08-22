    """_ a little setup and update programs.
       wrote by gnabro Israel.
       date : 22 / 08 / 2026
       version: 1.0.0
    _
    """

import os 
import pathlib 
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
        current_version: str = self.get_version()

        # secondly connect to github to download the content and setup.bin this should 
        # store a dict object. --- task 2
        new_metada: dict = self.get_new_release_data()

        # search for version in the dict object previously download and compare it to the current 
        # version of the app found in setup.bin --- task 3
        can_download = self.can_download(current_version, new_metada)


        # if these are differents, download the app.exe file located at github. --- task 4
        if can_download:
            notifyer.notify(
                title='nouvelle version disponible',
                message='Une nouvelle version de cet logiciel sera installée dans quelque instant.',
                app_name='extracteur',
            ) 
            self.download()


        # if the download of app.exe is performed, display a popup to install the new release --- task 5
        self.install_setup()


    def get_version(self, *args):
        """_perform task 1_
        """
        pass 


    def get_new_release_data(self, *args):
        """_perform task 2_
        """
        pass 


    def can_download(self, current_version:str, new_metada:dict):
        """_perform task 3_
        """
        return current_version != new_metada['version']


    def download(self, *args):
        """_perform task 4_
        """
        # after that this task is performed, update 
        # the can_run_install_setup attribute, this boolean
        # should be passed to True if download succeded otherwise False
        pass 


    def install_setup(self, *args):
        """_perform task 5_
        """
        # if the can_run_install_setup is True
        # start installation 
        pass