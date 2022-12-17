TABLE(DATASET) - substation_details
substation_acronym - acronym(short form) used to represent the substation name
substation name - name of the substation
voltage - various voltage levels present at the substation. the more voltage levels, the bigger the substation
voltage levels - count of the voltage levels
installed capacity - installed transformer capacity 
location - region where the substation is located. substations in the central region are generally bigger, more loaded and more important
generators - indicates whether the substation has generators (dams) connected to it. 1-YES, 0-NO
critical level - shows how important substation is to the national grid. 1 - NOT VERY IMPORTANT, 5- VERY IMPORTANT
comments - brief description of why substation is assigned a given critical level

TABLE(DATASET) - final_data
datetime - original datetime object from the SCADA system
event - event as described in the SCADA system
date - date extracted from original datetime object
month - month extracted from original datetime object
weekday - weekday extracted from original datetime object
type - identifies whether an event is critical or normal
substation_acronym - acronym(short form) used to represent the substation name
substation name - name of the substation
fault_voltage - voltage level at which faulty equipment operates
critical level - shows how important substation is to the national grid. 1 - NOT VERY IMPORTANT, 5- VERY IMPORTANT
