rainonme
========

I've got to be at work by 9am.
It takes 50minutes on the bus but only 30 by bike and it looks like it might rain.
Should I:

1. Leave at 8.30 as usual?
2. Leave early to beat the rain?
3. Leave now with an umbrella and take the bus?

Our app does just one thing brilliantly --
it automatically locates you and gets an accurate short-range,
minute-by-minute precipitation forecast for the next 60 minutes.
It displays this as a coloured background on a clock.
Orange means no rain and blues means rain (light blue = light rain -- navy blue = heavy rain).

We're demoing this as an iPhone/Android webapp
but this would look really cool on a Moto360/GalaxyGear/iWatch.

![Moto 360 smartwatch](http://origin.media.t3.com/img/resized/mo/xl_moto%20360%20new.jpg)

In [the background](/Derek-Jones/rain-on-me/), the short-range forecast
is determined by converting Lat/Lon to a location using ESRI's ArcGIS Geocoding API
then pulling the last hour's wind and rain data from
[weather stations 40km around your location](http://www.wunderground.com/weather/api/d/docs?d=data/geolookup) using Mashable's
[Weather Underground Almanac API](http://www.wunderground.com/weather/api/d/docs?d=data/almanac).
We then extrapolate how that rain will be blown over your location in the next hour.