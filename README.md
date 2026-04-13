# Demo for my Healthbot

### such a bad naming for my project, didn't get a good name though,
### just a damn college project

>[!NOTE]
> works only with qnscale "ble scale"
> and I only prefer python 3.13
>
>dependencies like ollama with llava "Ai model" haven't show in the setup


## Setup 

### cloning the repo

```
git clone https://github.com/Gilbin-Mathew/healthbot-demo.git ./healthbot-demo

```

### setting up the virtual environment

* Gnu-linux setup fedora or rhel users

```bash
cd ./healthbot-demo \
sudo dnf install python3.13 \
python3 -m venv venv \
source ./venv/bin/activate

```
* Windows users

> install the stable python3.13
> then, run poweshell

```poweshell
cd .\healthbot-demo `
; python -m venv venv `
; .\venv\Scripts\Activate.ps1

```
### Requirements 

* Scriptlet for requirements

> [!NOTE]
> run the command on the virtual eviornment

```
pip3 install -r requirements.txt

```

### to run the python programm

>[!NOTE]
> run these scriplets on the programs directory
> I mean on the directory where the code is cloned

* Gnu-linux

```bash
source ./venv/bin/activate

```
* Windows

```powershell
.\venv\Scripts\Activate.ps1

```

```python
python Health-Bot.py

```
