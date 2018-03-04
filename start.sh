_IP=$(hostname -I)
/home/pi/dispy/py3/dispy/dispynode.py -i "$_IP" --clean --daemon&
