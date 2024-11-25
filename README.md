# Uncontrolled reentries will disrupt airspace again

This repository contains the data and code used in the paper 'Airspace closures due to reentering space debris' (2024) by Ewan Wright, Aaron Boley and Michael Byers.

It is provided for independent assessment. If you use information provided here, please cite the 2024 paper linked here: [TBC]

The aircraft transponder data is too large to upload here but is available from https://samples.adsbexchange.com/readsb-hist/. We downloaded it in 5 second intervals. The 'Output data' folder is also too large to upload but will be generated by the below scripts.

The file 'create_weighting_function'.py uses the past 10 years of reentry data from GCAT to build a weighting function as described in the paper methodology.

The file 'find_aircraft_expectation.py' uses data from 1 September 2023 to find the casualty expectation for that day. 

The file 'find_airspace_expectation.py' uses data from 1 September 2023 to find the airspace infringement expectation for that day. 

The four plotting scripts create each plot used in the paper. 

Licence (CC BY-SA 4.0): https://creativecommons.org/licenses/by-sa/4.0/
