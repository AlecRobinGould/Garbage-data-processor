# Intro

This code is quite self-explainatory.

This code ignores temps with the same timestamp, and fills in "blank" timestamps (Where the temp logger missed an interval) with an interpolated value. 
The reason I wrote this code is because relative timestamps don't work unless the 2 seperate devices both log at regular intervals.
In other words over a 1 hour log period, I expect exactly 3600 logs.

In this case (See Data.csv), the ambient temperature measurement device is garbage and does not log with consistent intervals. The motor temperature
is given by the Single Pixel Feed Controller (SPFC), from the Helium Compressor, and has a constant 1s interval.
