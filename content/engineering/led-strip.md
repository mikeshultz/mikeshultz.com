Title: Building a Raspberry Pi Controllable RGB LED Strip
Date: 2017-02-17 17:20
Modified: 2017-02-19 20:15
Category: Engineering
Tags: engineering, RPi, Raspberry-Pi
Slug: raspberry-pi-controllable-rgb-led-strip
Authors: Mike Shultz
Summary: As part of a larger project, I built an RGB LED strip switch board that can be controlled by a Raspberry Pi

As part of a larger project, I built an RGB LED strip switch board that can be controlled by a Raspberry Pi.  I'm not much of an electrical engineer, so don't judge my awful schematics and soldering.

## Design

I looked through a ton of online articles some were hit or miss.  I based my project off of [David Ordnung's post](https://dordnung.de/raspberrypi-ledstrip/).

![Schematic](https://i.imgur.com/Lu11vIQ.png)

![Physical Schematic](https://i.imgur.com/XL6LD2V.png)

## Assembly

I used a piece of perfboard without any solder spots. I don't recommend using these at all.  They're incredibly difficult to worth with and you end up with a bunch of loose components.  That said, it's what I had and it did the job.

![Top view of the switch board](https://i.imgur.com/vmLmKsN.jpg)

![Another top view](https://i.imgur.com/oeUkoZr.jpg)

Soldering everything together with wires is also really delicate work and requires decent soldering skills.  It can e done haphazardly like I did, but it will end up with melted insulation and possibly more shorts than you wanted.  I'd still recommend getting a perfboard with solder pads.

![Awful wiring](https://i.imgur.com/jIApCf3.jpg)

## Mounting

I initially tried just using the adhesive on the LED strip, but that was woefully inadequite.  I was mounting to the back side of monitors and they fell off almost instantly.  So I went searching my local hardware store and found some drywall corners.  They're intended to make a clean seam in the corner of the room where drywall comes together.  Easy to cut to size and rigid enough for my purposes.

![LED Strip mounting to the drywall corner](https://i.imgur.com/oK7uXBg.jpg)

And I mounted the newly trimmed switch board directly to the drywall corner.

![Switch board mount to the drywall corner](https://i.imgur.com/UrmEu0M.jpg)

I then used double sided tape to adhere it to the back of the monitor.

![Mount to the monitor](https://i.imgur.com/OCJiBAQ.jpg)

## Final Look

Looks pretty good.

![View of the ambient light](https://i.imgur.com/cwKtt2p.jpg)

**NOTE**: I hope to update this more with better instructions in the near future, but wanted to get this up.