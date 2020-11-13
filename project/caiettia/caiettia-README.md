# README

LAST UPDATED: 2020-10-19  
ORGANIZATION: spatial-data-discovery  
REPOSITORY: ay2021-1  
FOLDER: project/caiettia

# Project Info
For my project, I looked at the Swainson's Hawk. My initial interest in the bird came from seeing the hawks migrating 
in and around my hometown of San Diego, CA. Yet in terms of migratory patterns, Swainson's Hawk has one of the longest
migrations in terms of distance covered, spanning from the North Western United States down to South Eastern Argentina.
Not only is the distance covered by their migration interesting, but also the indicator for when the birds decide to 
migrate. Supposedly, the hawks begin their migration in the Fall, when the surface wind in the Western United States blows 
south. I found the specificity of this interesting and wanted to combine migratory and surface wind vector data
to see this in action. 

# Relevance
Aside from having an interesting migratory pattern, Swainson's Hawk is an endangered species. The nature of their long distance
migration makes their ecosystem much more fragile, as changes in any region along their migratory path carry implications to the
survivability of the hawk. For example, pesticides used by farmers in Argentina to control local pests had resulted 
in a significant number of these hawks being poisoned. It is important to understand the fragility of the ecosystems that live 
around us. The Swainson's Hawk is particularly a good example of how far-reaching ecosystems are, spanning beyond our own locale. 
If anything, it is important to have a heightened awareness of the implications of our actions. Thus, I find it important to observe
migratory patterns such as the Swainson's Hawk.

# Data Sources
Firstly, my migratory data came from MoveBank.org, an opensource platform that allows researchers to archive and analyze animal 
movement data. From MoveBank, I was able to successfully identify the Swainson's Hawk dataset. Originally, the dataset was composed
for a study of "migration routes, length of migration, and duration of migration" for Swainson's Hawks in 1998. Each bird was radio 
tracked using the ARGOS satellite system, a satellite telemtery service for "scientificand environmental applications." The 
dataset identifies each individual bird with a unique individual indentifier (i.e SW1, SW2, etc.), and provides
time-stamped coordinates tracking the hawk's movement. 

With this datasource, intial exploration of the data allowed me to see the movement of a bird overtime by seeing each given 
bird's location over time. So, my goal was to aggregate my data by individual identifier (SW1, SW2, ...) and map their 
migratory path over time. I needed to create shapes beyond the POINT shapes I currently had. So, I found LineStrings. In a GeoJSON
object, LineStrings are shape objects constructed by a series of coordinate pairs. 

WHERE FROM, PROCESSES / CHANGES MADE
HOW CONVERTED IT FOR VIZ

