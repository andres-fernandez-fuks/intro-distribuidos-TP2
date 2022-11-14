export POX_FOLDER_PATH="/home/andy/pox"
yes | cp -rf ./firewall.py $POX_FOLDER_PATH/pox/misc
yes | cp -rf ./settings.py $POX_FOLDER_PATH/pox/misc
gnome-terminal -- /bin/bash -c 'cd $POX_FOLDER_PATH && ./pox.py misc.firewall forwarding.l2_learning'
sleep 2
sudo mn --custom ./topology.py --topo custom,4