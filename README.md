# Edit42
It is a desktop configuration editor for FieldStation42 station files, written in python and PySide6  
This project is tremendously inspired by the FieldStation42 project  

## Current Features:
 - syntax highlighting  
 - quick navigation to config elements from dropdown lists automatically configured based on the content of a given station config  
 - json error checking as you type  
 - json schema checking as you type. The schema used is from the FieldStation42 project  
 - create, copy, save and insert custom slot overrides and day templates  
 - easy access to all your station configs via either direct file access or via API. configured at first run  
 - simple search functionality
 - NEW - Configs are backed up at app start. If you set Edit42 to use file mode, then the edit42-backup folder will be in your confs directory. If you selected API mode then the edit42-backup will be in the app directory
 - cool styling

## Installation:
 - `git clone https://github.com/visualkev/Edit42.git`
 - `pip install pyside6`
 - `pip install jsonschema`
 - `pip install requests`
 - from the edit42 directory, run `python main.py`
<br>Note: this was developed on linux. I have just setup a windows 10 vm and the app is not 100% on that platform. I'll head down that rabbit hole soon enough.
<br>

## Usage Guide:
<br>
<br>
<img width="550"  alt="Selection_455" src="https://github.com/user-attachments/assets/21bdc877-a69b-4eeb-83da-d4590a559c94" />     
<br>
<br>
<br>
<img width="400" alt="Edit 42 | 42: Happy_001" src="https://github.com/user-attachments/assets/46cc58c0-2d0e-4a35-9b5f-1e1cab80d86a" />     
<br>The main page will automatically load the first available config document at startup
<br>
<br>
<br>the channel list box will have your available channels
<img width="200" alt="Selection_439" src="https://github.com/user-attachments/assets/81e15041-d27b-4592-b49b-55eb5c356830" />    
<br>
<br>
<br>The slot overrides listbox
<img width="189" height="218" alt="Selection_440" src="https://github.com/user-attachments/assets/0a4641ae-6acb-44d6-ab09-b08241131fe6" />     
<br>
<br>
<br>The day templates listbox
<img width="154" height="210" alt="Selection_441" src="https://github.com/user-attachments/assets/1380af94-90f6-4122-a872-79c8303e9f57" />     
<br>
<br>
The common block listbox
<img width="250"  alt="Selection_442" src="https://github.com/user-attachments/assets/59ff94cd-4e0e-4a15-8c60-5f7d78c4a040" />     
<br>
<br>
The simple search box
<img width="250"  alt="Selection_443" src="https://github.com/user-attachments/assets/8d44baf1-0df5-4286-8fee-64ac1e25130b" />
<br>
<br>The title bar shows current loaded channel info
<img width="200"  alt="Selection_444" src="https://github.com/user-attachments/assets/a4f4911d-e4a9-4f58-8383-2ecd4883c29d" />
<br>
<br>The insert listbox
<img width="300"  alt="Selection_445" src="https://github.com/user-attachments/assets/511c17d4-090c-4a4e-85c8-92a87b197c54" />
<br>
<br>The save button
<img width="200"  alt="Selection_446" src="https://github.com/user-attachments/assets/50142135-81ba-442f-beb3-b2e60dbe2c55" />
<br>
<br>Json syntax status
<img width="300"  alt="Selection_447" src="https://github.com/user-attachments/assets/f9cfed3b-fcb0-4794-93dd-16da6a762476" />
<br>
<br>Json schema
<img width="300"  alt="Selection_448" src="https://github.com/user-attachments/assets/910a4e49-5462-4e07-b95f-b1cebb73c6e5" />
<br>
<br>
<br>The insert page
<img width="360"  alt="Edit 42 | 42: Happy_003" src="https://github.com/user-attachments/assets/eaa11a4c-81c7-4ab8-b199-bd3feb6425ca" />
<br>
<br>
<br>The name textbox
<img width="300" alt="Selection_449" src="https://github.com/user-attachments/assets/26b4981d-3a5e-4e85-8ead-a33d342a9b16" />
<br>
<br>Check for new
<img width="300"  alt="Selection_450" src="https://github.com/user-attachments/assets/581de2e6-c594-4977-8f0f-9388a0eaaadb" />
<br>
<br>
<br>
<br>Copy from existing
<img width="300"  alt="Selection_451" src="https://github.com/user-attachments/assets/184bd6e1-4064-4347-bc2a-e3fea8eb78bf" />
<br>
<br>
<br>Customize the new config
<img width="400"  alt="Selection_452" src="https://github.com/user-attachments/assets/b905e27b-998a-44de-8bad-358e05df51f4" />
<br>
<br>Save snippet
<img width="400"  alt="Selection_453" src="https://github.com/user-attachments/assets/1e7ce124-575c-4b3a-8b71-e981b6098c3a" />
<br>
<br>
Insert into main document
<img width="300"  alt="Selection_454" src="https://github.com/user-attachments/assets/3d48bc8e-6ace-49db-a069-002ed7d0c6e2" />
<br>
<br>

## More info:  

This is my first major programming project. It's my first python project and it is also my first time with PySide6. My testing is limited to my linux desktop only, so there will likely be much breakage on other platforms.

That all said, I did want to add something cool to the <a href="https://github.com/shane-mason/FieldStation42">FieldStation42</a> community, because its an awesome project headed by Shane. He is a masterful programmer and very creative.









## Possible Future Features:
 - Optional ability to easily manage schedules with no direct json editing
 - Rule based merge/ blend of day templates
 - Bracket and quote matching
 - Your ideas are welcomed
