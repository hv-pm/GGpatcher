# General Game Patcher (GG!patcher)

<p align="center"><img width="460" height="190" src="https://github.com/hv-pm/GGpatcher/blob/main/assets/logo/GG!patcher_logo.svg"></img></p>

&nbsp;&nbsp;&nbsp;&nbsp;Games, especially MMORPGs, usually have an initial UI screen to update and repair the game files, show the patch notes for updates, and to allow the user to change the game's settings before launching it. This UI is usually called `Patcher`.
The GG!patcher is a fruition of a study on how to implement a general-purpose patcher with Python, PyQT5 and QT Designer that could be applied to any game that is capable of receiving online updates. The visual identity adopted for the GG!patcher's inbuilt example is a homage to Trickster Online (2006-2013), but the instructions bellow will guide you to change the GG!patcher at your will.

## The Visuals
&nbsp;&nbsp;&nbsp;&nbsp;You can customize the UI by simply overwriting the images in the `img` folder, as long as your img files keep the same name as the ones they are overwriting it will work just fine. Some adjustments will be necessary in the `setGeometry` property for your images dimensions and position though, keep that in mind.

&nbsp;&nbsp;&nbsp;&nbsp;The other and most recommended way to customize the UI is through QT Designer. If you choose this path then there are rules you must follow to name your UI elements in QT Designer before saving your template:

### patcher.ui
 * `Background Image` &rarr; `bgImg`;
 * `Game Logo Image` &rarr; `logoImg`;
 * `Close Patcher Button` &rarr; `closeBt`;
 * `Language Button` &rarr; `languageBt`;
 * `Repair Files Button` &rarr; `updateBt`;
 * `Settings Button` &rarr; `optionsBt`;
 * `Launch Game Button` &rarr; `gameStartBt`;
 * `Patch Notes Text Browser` &rarr; `patchNotes`;
 * `Patch Notes Label` &rarr; `patchNotesLabel`;
 * `Progress Bar Background Image` &rarr; `progressBarImg`;
 * `Progress Bar` &rarr; `progressBar`;
 * `Progress Bar Auxiliary Indicator` &rarr; `auxProgressImg`; 

&nbsp;&nbsp;&nbsp;&nbsp;You can also add new elements as buttons, widgets and labels to your liking and implement their functionality in the GG!patcher's main program file `run.py`. After you've customized your UI in QT Designer, save your template as a `.ui` file and convert it to a `.py` file using the command `pyuic5 patcher.ui -o patcher.py` on your preferred IDE, this will translate your QT Designer template into a Python app by using PyQT5 libraries. If you had the GG!patcher project open in the IDE, your `patcher.py` file will be generated in the same folder as your `run.py`.

## language.ui
&nbsp;&nbsp;&nbsp;&nbsp;Rules you must follow to name your UI elements in QT Designer before saving your template:
 * `en-us Language Radio Button` &rarr; `en_usBt`;
 * `US Flag Image` &rarr; `usImg`;
 * `en-us Label` &rarr; `en_usLabel`;
 * `pt-br Language Radio Button` &rarr; `pt_brBt`;
 * `BR Flag Image` &rarr; `brImg`;
 * `pt-br Label` &rarr; `pt_brLabel`;
 * `th Language Radio Button` &rarr; `thBt`;
 * `TH Flag Image` &rarr; `thImg`;
 * `th Label` &rarr; `thLabel`;
 * `zh-cn Language Radio Button` &rarr; `zh_cnBt`;
 * `CN Flag Image` &rarr; `cnImg`;
 * `zh-cn Label` &rarr; `zh_cnLabel`;
 * `Language Window Background Image`: `bgImg`;
 * `Confirm Button` &rarr; `confirmBt`;

&nbsp;&nbsp;&nbsp;&nbsp;Differently from `patcher.ui`, in case you want to add a language window you'll have to go through some aditional steps, as we are rendering this window only when `languageBt` is pressed.
Edit it normally with QT Designer and save the template as a `.ui` file and convert it to a `.py` file, just as aforementioned. Then, open your `language.py` file in your preferred IDE and do the following:
 * Change `Ui_Form(object):` to `Ui_LanguageWindow(QWidget):`;
 * Add `confirmLanguage = pyqtSignal()` right below it;
 * Change `setupUi(self, Form):` to `__init__(self):`;
 * Add `super().__init__()` right below it;
 * Substitute every `Form` instance to `self`;
 * Copy and paste to your `language.py` the lines from 121 to 175 of GG!patcher's `language.py`. 

&nbsp;&nbsp;&nbsp;&nbsp;This is necessary to render the language UI when we click `languageBt`, but mainly because `run.py` cannot access `confirmBt`'s `clicked.connect` event as this button is not rendered until we press `languageBt`, so the app will NOT compile. To bypass that we tell `confirmBt` to close the window when it is pressed, and we edit the `closeEvent` inbuilt function to emit a signal to our `run.py` to activate the update process when the language window is closed by pressing `confirmBt`. Finally, this update process will look for the new language selected and update the game with the translated patches/files.

## Filelist Generator
&nbsp;&nbsp;&nbsp;&nbsp;An aditional `.exe` is provided to you at GG!patcher's assets/FilelistGen in order to generate your filelist in the right format for GG!patcher to work with. You simply organize your files inside a folder and insert its absolute path to `filelistGen.exe`. A filelist will be generated in the same directory as `filelistGen.exe` containing the name and size of each file inside the inserted folder. Everytime this guide refers to a filelist, it is a `.txt` file generated using this app.

&nbsp;&nbsp;&nbsp;&nbsp;In case you want to edit the source `.py` and generate your own `filelistGen.exe` you can simply execute the following commands:

1 - `pip pyinstall`

2 - `pyinstaller.exe --onefile main.py`

&nbsp;&nbsp;&nbsp;&nbsp;This will generate three folders in your working directory: `__pycache__`, `build`, `dist`. Your standalone ´.exe´ will be inside `dist` named as `main.exe`.

## URL Glossary
&nbsp;&nbsp;&nbsp;&nbsp;You may have noticed at this point that GG!patcher's `run.py` has fields asking for URLs for each file, these URLs are the direct download link to your files, *i.e.*, the ones that when you paste on a browser will start a download. If you want the patcher to authenticate before downloading these files for security reasons, you'll have to add it manually in the `run.py` file. This section will describe what each URL field stands for:

##### patcher.py
 * `patchNotesUrl`: *your patch notes can be generated by double clicking your `patchNotes` in QT Designer. After it is to your liking, copy the source code generated and delete any new lines so the code to becomes a one-line string, then paste it into a .txt file, upload it to your server and provide the download link to it at this variable*.

##### run.py
 * `updateFileListUrl`: *link to the update filelist to be added/updated in the game client*;
 * `updateFilesUrl`: *link to the game files compressed in a `.zip` archive. The files that: (i) are in the filelist but not in the user's local folder or that (ii) are in the user's local folder but not equal in size as in the filelist will be extracted and downloaded from this archive*;
 * `translatePatchInfoUrl`: *link to the translated game file(s) filelist. There are four of this variable because GG!patcher comes with four language options as you can see in the commented lines at `run.py`*;
 * `translatePatchUrl`: *link to the translated game file(s) compressed in a `.zip` archive. It will execute the same procedure aforementioned in `updateFilesUrl`*;
 
&nbsp;&nbsp;&nbsp;&nbsp;Finally, substitute `Game.exe` and `Setup.exe` for your game's `.exe` files, the path is relative to the `.py` files directory. If you've followed the given instructions until here, then your `run.py` will execute with no errors.
 
## Generating your patcher.exe
&nbsp;&nbsp;&nbsp;&nbsp;Execute the following command in your preferred IDE:

1 - `pip pyinstall`

2 - `pyinstaller.exe --onefile --windowed --icon=patcher.ico run.py`

&nbsp;&nbsp;&nbsp;&nbsp;This will generate three folders in your working directory: `__pycache__`, `build`, `dist`. Your standalone `.exe` will be inside `dist`, for it to work correctly you must send to the user the following:

 * Patcher.exe;
 * img folder;
 * config.txt;
 * YourGame.exe;
 * YourGameSetup.exe;
 * patcher.ico;
 * Your game files and folders.
 
&nbsp;&nbsp;&nbsp;&nbsp;Additional files can be found at GG!patcher's assets/support folder, you can base yourself in those to clear any doubts about how to format the files, if you still have doubts I encourage you to use the discussion section!

### Setup 
 * QT Designer
 * PyCharm (Interpreter: Python v3.10);
