"""
a little setup and update programs.

#-----------------------------------------------------------------------------------------------#
wrote by gnabro Israel.
date : 22 / 08 / 2026
version: 1.0.0

#-----------------------------------------------------------------------------------------------#

"""

# -------------------------------------------------------------------------------------------------------------------#
# global variables
# -------------------------------------------------------------------------------------------------------------------#

"maximun bytes send to the progressbar. This is the maximun value of the progressbar."
bytes_send: int = 0

"value display eache time by the progressbar, it's update by the Update instance."
bytes_received: int = 0


import json
import shelve
import requests
import os
import sys
import subprocess
from plyer import notification as notifyer

# ------------------------------------------------------------------------------------------------------------------#
# setup class : this wil be improuve later
# version: 1.0.0
# ------------------------------------------------------------------------------------------------------------------#


class Update:
    """
    run the installation set up.
    try to find a new release of the app.

    """

    def __init__(self, app=None) -> None:
        "flag to run install_setup"
        self.can_run_install_setup = False

        # the current app instance
        self.app = app

        # firstly read the setup.bin file to get the version of the software. --- task 1
        current_version: str | None = self.get_current_version()

        # secondly connect to github to download the content and setup.bin this should
        # store a dict object. --- task 2
        new_version: str | None = self.get_new_version()

        # search for version in the dict object previously download and compare it to the current
        # version of the app found in setup.bin --- task 3
        # if these are differents, download the app.exe file located at github. --- task 4
        self.download(current_version, new_version)

        # if the download of app.exe is performed, display a popup to install the new release --- task 5
        self.install()

    def get_current_version(self, *args):
        """_perform task 1_"""
        with shelve.open("setup.bin") as metadata:

            # return the version
            if not (metadata.get("version", 0) == 0):
                return metadata["version"]

            # the file 'setup.bin' is corrupted or not build
            metadata["version"] = "1.0.0"
            metadata["author"] = "Gnabro Israel"
            metadata["email"] = "ambroiseisrael5@gmail.com"
            metadata["about"] = (
                "extracteur de texte (contenu les fichiers .pdf et .docx) et de vidéo youtube."
            )

            # close the file
            metadata.close()

            return "1.0.0"

    def get_new_version(self, *args):
        """_perform task 2_"""
        # the url of the metada of new_release, is store in new.json file
        url = "https://raw.githubusercontent.com/Ambroise07/extractor/main/config/new.json"

        try:
            # get the response object
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                print(response.text)

                version = json.loads(response.text)["version"]
                return version

        except:
            return None

    def install(self, *args):
        """_install the new release_"""
        # see the bin folder
        exe_url = (
            "https://raw.githubusercontent.com/Ambroise07/extractor/main/bin/app.exe"
        )

        try:
            # response object
            response = requests.get(exe_url, timeout=5)

            if response.status_code == 200:
                bytes_send = len(response.content)
                contents: bytes = response.content

                with open("../bin/app.exe", "wb") as exe_app:

                    for content in contents:

                        exe_app.write(content)
                        bytes_received += len(content)

                        yield bytes_received

                self.can_run_install_setup = True

        except Exception:
            return None

    def download(self, current_version: str, new_version: str | None):
        """_perform task 3_"""
        global bytes_send, bytes_received

        if new_version == None:
            self.can_run_install_setup = False
            return

        if current_version != new_version:
            notifyer.notify(
                title="nouvelle version disponible",
                message="Une nouvelle version de cet logiciel sera installée dans quelque instant.",
                app_name="extracteur",
            )

    def launch(self, *args):
        """_perform task 5_"""
        # if the can_run_install_setup is True
        # start installation
        if self.can_run_install_setup:

            # update the install flag
            self.can_run_install_setup = False

            # Chemin vers l'exécutable qui vient d'être téléchargé
            chemin_exe = os.path.abspath("../bin/app.exe")

            try:
                # Démarre le nouvel exécutable de manière indépendante
                subprocess.Popen([chemin_exe], shell=True)

                # Ferme proprement l'ancienne version actuelle du logiciel
                sys.exit()

            except Exception as e:
                print("erreur du lancement ...", e)

    def perform_task(self, *args):
        """
        call by the progressbar.
        """
        try:
            return next(self.install())

        except StopIteration:
            return None

    def finish_task(self, *args):
        """
        call by the progressbar.

        """
        self.app.quit()
        self.launch()


"""
display the installation progress.
notice, now this is only show when software is installing
a new release.

#------------------------------------------------------------------------------------------------------#
#author : Gnabro Israel
#date: August 22, 2026
#------------------------------------------------------------------------------------------------------# 
"""


import tkinter
from tkinter.ttk import Progressbar
from tkinter.messagebox import Message


class UpdateProgressUI(tkinter.Tk):

    def __init__(self, setup=None, **args) -> None:
        """_display the progression of setup._

        Args:
            setup (_type_): _performed the installation
                             of the updating of the software. should has methods bellows:_

                - perform_task: this will be call until the progressbar stopped the progression
                                  the progressbar mode is indeterminate,

                                  it's return a number that it's show in the  description label, dest_label.
                                  when this return None, the value of the progressbar is maximun.

                - finish_task: this will call when performed_task return None as value, this allowed the setup
                               to display a dialogue message, to notify user that the current instance of the
                               app will be destroyed to launch the new one.

                - release_metadata: the informations about the new release :
                                    *version
                                    *author
                                    *email
                                    *update


        """

        super().__init__(*args)

        "the setup instance"
        self.setup = Update(self) if setup is None else setup

        "the size of screen"
        self.geometry("600x300")

        "remove title bar"
        # self.overrideredirect(True)

        "main title"
        title_frame = tkinter.Frame(master=self)
        title_frame.pack(expand=True, fill="x", padx=("2c", 0), ipady=0)

        title = tkinter.Label(
            master=title_frame, text="Installation en cours...", font="Arial 12 bold"
        )
        title.pack(side="left")

        "step perfomed"
        step_frame = tkinter.Frame(master=self)
        step_frame.pack(expand=True, fill="x", padx=("2c", 0))

        step_var = tkinter.StringVar()
        step_var.set("0 effectué")

        title = tkinter.Label(
            master=step_frame, textvariable=step_var, font="Arial 12 bold"
        )
        title.pack(side="left")

        "the progressbar"
        progress_frame = tkinter.Frame(master=self)
        progress_frame.pack(expand=True, fill="both", padx=("2c", "2c"))

        progress_value = tkinter.IntVar()
        progress_value.set(0)

        progressbar = Progressbar(
            master=progress_frame, variable=progress_value, mode="determinate"
        )
        progressbar.pack(fill="x")

        self.after(3000, self.update_progressbar)

        "mainloop"
        self.mainloop()

    def update_progressbar(self, *args):
        new_value: int | None = self.setup.perform_task()

        if new_value is not None:
            self.progressbar["value"] = new_value
            self.step_var.set(f"{new_value} effectuées")
            return

        # launch the new release.
        Message(
            title="Mise - jour éffectuée",
            message="l'installateur rédemarre l'application.",
        ).show()
        self.setup.finish_task()


if __name__ == "__main__":
    UpdateProgressUI()
