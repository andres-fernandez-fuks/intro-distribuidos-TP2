export POX_FOLDER_PATH="/home/andy/pox"
yes | cp -rf firewall.py settings.py block_rule.py $POX_FOLDER_PATH/pox/misc////
gnome-terminal -- /bin/bash -c 'cd $POX_FOLDER_PATH && ./pox.py misc.firewall forwarding.l2_learning; bash'
sleep 2
sudo mn --custom ./topology.py --topo custom,4 --mac --controller remote