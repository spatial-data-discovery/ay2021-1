# README
LAST UPDATED: 2020-11-13  
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
## Migration Data
![MigrationData](https://www.movebank.org/cms/webapp?gwt_fragment=page=studies,path=study204253)
Firstly, my migratory data came from MoveBank.org, an opensource platform that allows researchers to archive and analyze animal 
movement data. From MoveBank, I was able to successfully identify the Swainson's Hawk dataset. Originally, the dataset was composed
for a study of "migration routes, length of migration, and duration of migration" for Swainson's Hawks in 1998. Each bird was radio 
tracked using the ARGOS satellite system, a satellite telemtery service for "scientificand environmental applications." The 
dataset identifies each individual bird with a unique individual indentifier (i.e SW1, SW2, etc.), and provides
time-stamped coordinates tracking the hawk's movement. 

With this datasource, intial exploration of the data allowed me to see the movement of a bird overtime by seeing each given 
bird's location over time. So, my goal was to aggregate my data by individual identifier (SW1, SW2, ...) and map their 
migratory path over time. I needed to create shapes beyond the POINT shapes I currently had. So, I found LineStrings. In a GeoJSON
object, LineStrings are shape objects constructed by a series of coordinate pairs. The LineString will then create line shapes 
between the points. Initially, I had made LineStrings mapping out the paths of each individual bird. However, I realized that for 
animation's sake, it would be more helpful for the user to be able to see the path of the bird develop overtime. So, I rewrote my 
script to create LineStrings that are timestamped. 

To visualize this data, I took advantage of a tool called Kepler-gl, a tool for geospatial data analysis that I think particularly excels at visualizing time series data. I was able to simply import my dataset in GeoJSON format to the WebGL component of Kepler-gl. There, I was able to use a timestamp filter to create the animation of the bird migration over time. 

## Wind Vector Data
![WindVectorData](https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.surface.html)
For my wind vector data, the biggest challenge was finding surface wind data that covered the time period of my migration dataset; 
1995 - 1998. I found the wind vector data, titled NCEP Reanalysis provided by NOAA/OAR/ESRL PSL, which had surface wind vector data 
from 1948 to the present. As such, I downloaded two datasets filtered from 1995-1998. The first is called Zonal Velocity (u) which 
is horizontal wind velocity at coordinate points. The second dataset is called Meridional Velocity (v), which is vertical wind. 
With this, I was able to create vectors in Panoply by loading both datasets, then creating a merged plot which created a wind 
vector (as an arrow) with the formula:

![equation](http://www.sciweavers.org/upload/Tex2Img_1605305106/render.png)

# Attributions
Fuller, M.R., Seegar, W.S., Schueck, L.S., 1998. Routes and Travel Rates of Migrating Peregrine Falcons Falco peregrinus and 
Swainson's Hawks Buteo swainsoni in the Western Hemisphere. Journal of Avian Biology 29:433-440.

Kalnay et al.,The NCEP/NCAR 40-year reanalysis project, Bull. Amer. Meteor. Soc., 77, 437-470, 1996.

![WindVectorMathematics](http://tornado.sfsu.edu/geosciences/classes/m430/Wind/WindDirection.html)

