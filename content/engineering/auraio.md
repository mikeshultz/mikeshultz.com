Title: Auraio and Conveying Information With Atmospheric Lighting
Date: 2017-03-08 00:19
Category: Engineering
Tags: led, RPi, raspberry pi, python
Slug: auraio-and-conveying-information-with-atmostpheric-lighting
Authors: Mike Shultz
Summary: After the LED strip project I was itching to make it more useful.  I wanted to do something with the RGB LED strip lighting that would convey real world information to me.

After the LED strip project I was itching to make it more useful.  I wanted to do something with the RGB LED strip lighting that would convey real world information to me.  For this, I built [auraio](https://github.com/mikeshultz/auraio).  It's built with python, and is completely modular.  My first plugin was for [Sensu monitoring](https://sensuapp.org/).  

By plugging auraio into sensu, I was able to have the atmospheric lighting tell me when something has gone wrong(or that everything is okay).  I decided to go with red when there's a critical issue, yellow if a warning, green for "everything is cool", and blue when there's and unknown state and a human needs to get involved to interpret.

![blue looked pretty good](http://i.imgur.com/cwKtt2p.jpg)

## LED Control

Auraio was pretty straight forward to build.  It needed to [be able to control the LEDs on a Raspberry Pi](https://github.com/mikeshultz/auraio/blob/master/auraio/core/ledcontrol.py).  For this I used the [pigpio daemon and Python library](http://abyz.co.uk/rpi/pigpio/python.html). 

pigpio made setting the LED states really straight forward and it just took a little follig around to get it to blink, sent brightness, set color taking a hex value, and fade from state to state in a fairly pleasant manner.  I shot a video of the state change at some point but I can't find it right now.  If I do, I'll post it.

## Plug-Ins

I built this so it could take whatever plugins it needs.  I only needed Sensu at first, but you could build a plug-in to consume data from whatever and send a state/alert back to the controller to tell it what to do.  Right now, that's just "good", "warn", "bad", and "unknown."  Those are the easiest states to convey through light, anyway.

## Sensu

I based the Sensu plugin off of it's check states.  Basically, they map to 0(good), 1(warning), 2(bad), and any higher number is from a Sensu check plugin throwing an unusual state.  That's almost always bad, but sometimes it's just garbage, which is why I couldn't default to bad > 1.

## Future

I hope to hook this up to a Grafana display in the future to get the full monitoring picture with glanceable information provided by auraio.  Perhaps a Raspberry Pi could handle everything.