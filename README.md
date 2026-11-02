This is my solution to Space Cadets Challenge 5, where we must make a spirograph-drawing program
> The challenge this week is to create a virtual version of a "Spirograph" (a childrens toy back in the dark ages). A Spirograph consisted of a set of small toothed wheels that rolled around the inside of larger wheels. You put a pen inside a hole in the smaller wheels and drew out a pattern as it looped around the bigger wheel.
>

Spirographs can either be rendered and then displayed, via Spirograph.render, or drawn in realtime via Spirograph.draw

Spirographs are made of a list of Pens, each of which is attached to a Point, which is itself on a Wheel. Wheels are anchored to Points, with the exception of the Root Wheel, which is anchored at the origin
