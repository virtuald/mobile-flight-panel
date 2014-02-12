

DEST=/mnt/local/kivy/Panel

adb start-server

adb push main.py $DEST
adb push panel.kv $DEST
adb push pb_on2.png  $DEST
adb push pb_off2.png  $DEST
adb push rev_off.png  $DEST
adb push rev_active.png  $DEST
adb push background2.png  $DEST
adb push slider_spdbrk2.png  $DEST
adb push slider_flaps2.png  $DEST
adb push throttle_l.png  $DEST
adb push throttle_r.png  $DEST
adb push FlightGear.py  $DEST



