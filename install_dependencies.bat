@echo off

echo Update pip...
call python.exe -m pip install --upgrade pip

echo Update virtual environment...
pip install --upgrade pip

echo Installing virtualenv...
pip install virtualenv

echo Creating virtual environment...
python -m venv env

echo Activating virtual environment...
call .\env\Scripts\activate

echo Running with GPU...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121/

echo Installing API requirements...
pip install -r requirements.txt

echo Make Migrations...
py manage.py makemigrations
py manage.py migrate

echo Installation completed.
pause
