# Demo for my Healthbot

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

* Gnu-linux

```bash
source ./venv/bin/activate

```
* Windows

```powershell
.\venv\Scripts\Activate.ps1

```

```python
python main.py

```
