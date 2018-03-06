_IP=$(hostname -I)
python3 /home/pi/dispy/py3/dispy/dispynode.py -i "$_IP" --clean --daemon&
