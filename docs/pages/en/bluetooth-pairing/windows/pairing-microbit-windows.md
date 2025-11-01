---
title: Pair a micro:bit in Windows
description: Detailed instructions on how to pair your micro:bit in Windows
---

After following the general pairing instructions below, head over to the 
[Kasper's microbit overview page](../../index.md) and start creating your first game!

[![Video of games created with kaspersmicrobit](../../assets/images/kaspersmicrobit-youtube-small.gif)](../../index.md)
  

## Step-by-step instructions

Click on the Bluetooth icon in your system tray.  
Click "Show Bluetooth devices"

![click bluetooth icon in system tray](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-icon-system-tray.png)  

The "Bluetooth & other devices" screen opens, click "Add Bluetooth or other device"

![Bluetooth & other devices screen](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-devices-screen.png)  

The "Add a device" screen pops up. Now you'll need to put your micro:bit in "pairing mode":

  - Hold down the A, B and reset buttons simultaneously.
  - Release the reset button but still hold the A and B buttons.
  - The LED screen will fill and you should then see the Bluetooth logo, followed by a pairing pattern.
  - Now you can release the A and B buttons

Your micro:bit is in pairing mode and is discoverable by Windows
Now click on "Bluetooth"

![Add a device](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-add-a-device.png)  

Windows will scan for bluetooth devices, your micro:bit should show up in the list

![Discover devices](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-discover-devices.png)

Click on the micro:bit device in the list, Windows will pair with the micro:bit

![Pair with micro:bit](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-pair-with-with-microbit.png)

You can click "Done" your micro:bit is paired in Windows!

## Finding the Bluetooth address
If you're not using the [easier connection methods](../../how-to-connect.md), but instead you want to 
[connect to a micro:bit by address](../../how-to-connect.md#connect-to-a-microbit-by-address), these are
the instructions to look up the address in Windows.
 
Back on the Bluetooth & other devices screen, select your micro:bit and click
"More Bluetooth options"

![Bluetooth & other devices](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-devices-more-options.png)

The Bluetooth settings window pops up. On the "Hardware" tab, select your micro:bit and click "Properties"  

![Bluetooth settings](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-devices-hardware-tab.png)

The micro:bit properties window pops up. On the "Details" tab, select the "Association Endpoint address" property. 
The value of this property is the bluetooth address of your micro:bit.  ***Write this address down somewhere*** you'll
need it to connect to your micro:bit.

![Micro:bit properties](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-devices-hardware-address.png)

## Create your first game

[Kasper's microbit](../../index.md) is a python package to make a connection to a BBC micro:bit by means of the Bluetooth LE GATT services
exposed by the micro:bit.

[![Video of games created with kaspersmicrobit](../../assets/images/kaspersmicrobit-youtube.gif)](../../index.md)
  