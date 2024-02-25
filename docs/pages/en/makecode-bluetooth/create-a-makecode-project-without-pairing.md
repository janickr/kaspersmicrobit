---
title: Create a Bluetooth-enabled MakeCode project with no pairing required 
description: How to create a micro:bit MakeCode project, enable the Bluetooth extension and disable pairing
---
# Your own MakeCode project (No pairing required)

You can create a Bluetooth-enabled [MakeCode](https://makecode.microbit.org) project yourself. 
Below are the detailed instructions to create a micro:bit MakeCode project, enable the Bluetooth extension 
and disable pairing. A project with [pairing disabled ("No pairing required")](#disable-pairing) is the easiest to work with:

- it works on the [widest range of micro:bit versions and operating systems](../index.md#microbit-versions-operating-systems-bluetooth-pairing)
- it doesn't require the extra steps of pairing the micro:bit with your operating system
- it makes the microbit advertise its name, so you can [find it by name](../reference/kaspersmicrobit.md#kaspersmicrobit.kaspersmicrobit.KaspersMicrobit.find_one_microbit)

The disadvantage is that anyone can connect with the micro:bit over Bluetooth, because it is not needed to be paired to it.

## Create a project
In MakeCode for micro:bit, select "New Project"  

![Start a new project](../assets/images/makecode-bluetooth/makecode-new-project.png)  
  
Enter a name:

![Create project: give your project a name](../assets/images/makecode-bluetooth/makecode-create-project-give-name.png)  


## Add the Bluetooth extension
You'll need to add the Bluetooth extension.   
Select "Advanced"

![MakeCode project blocks: select advanced](../assets/images/makecode-bluetooth/makecode-project-blocks-select-advanced.png)  

Select "Extensions"  

![MakeCode project blocks: select extension](../assets/images/makecode-bluetooth/makecode-project-blocks-select-extensions.png)  

Search for Bluetooth, and select the Bluetooth extension

![Extensions: search and select Bluetooth](../assets/images/makecode-bluetooth/makecode-project-extensions-select-bluetooth.png)  

A popup appears, informing you that the "radio" extension will be removed if you add Bluetooth. 
Select "Remove extension and add Bluetooth", this will only apply to this project. 

![Remove the radio extensions and add Bluetooth](../assets/images/makecode-bluetooth/makecode-remove-radio-and-add-bluetooth.png)  


## Disable pairing

In the top-right corner click on the cog icon and select project settings. Enable the "No pairing required: anyone can 
connect via Bluetooth" option. Save the Settings.

![Select No pairing required in project settings](../assets/images/makecode-bluetooth/makecode-project-settings-microbit-no-pairing.png)


## Add Bluetooth services

Now you can select blocks from the bluetooth tab:  

![Select Bluetooth blocks](../assets/images/makecode-bluetooth/makecode-project-blocks-select-bluetooth.png)  

Drag the services you want to enable in an "On start" block  

![Drag Bluetooth services in On start](../assets/images/makecode-bluetooth/makecode-project-drag-services-in-onstart.png)  

The micro:bit v1 has too little memory to enable all bluetooth services. If you try to enable them all, after 
copying the hex the micro:bit, the LED display wil show a sad face and then scroll 020, this means the micro:bit is out of memory.
See also: [the micro:bit error codes](https://makecode.microbit.org/device/error-codes)

## Download the hex file
Download the hex file and copy it to your micro:bit!  

