export POX_FOLDER_PATH="/home/$USER/pox"
yes | cp -rf firewall.py settings.py block_rule.py $POX_FOLDER_PATH/pox/misc////
cd $POX_FOLDER_PATH && ./pox.py misc.firewall forwarding.l2_learning