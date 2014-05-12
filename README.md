#Implementation of Stop and Frisk in New York 2012#
###David Koh###
=======

##Introduction##

One of the foundations of policing under former NYPD police commissioner Ray Kelly and former mayor Michael Bloomberg is a technique called “stop and frisk” which gave police officers in New York City the ability to observe individuals, stop them based on a reasonable suspicion, and to frisk them as well if the police officers still believed something was going on. This is a technique that has been gaining popularity over the years and has recently been highlighted for its controversial implementation. 

The purpose of this project is to use data science techniques to analyze how “stop and frisk” was implemented in New York City in 2012. 

##Datasets##

The New York City Police Department (NYPD) requires paperwork to be filed for each stop. In 2012 there were 532,911 stops. I was able to obtain a dataset from the New York Civil Liberties Union (NYCLU) website. For each stop the officer documented details about the suspect’s race, sex, location, time of stop, etc. using Form UF-250. There are 2 ways the NYPD reports this stop-and-frisk data: a paper report released quarterly and an electronic database released annually. 
  1. I explored this data to see what types of people were being stopped, frisked, and if this actually led to arrests. 
  2. I also used the data to try and predict the kinds of people who were most likely to be frisked. 

In addition to the stop and frisk data I also obtained a dataset from the NYPD website containing the number of offenses of the 7 major felony offenses by precinct in 2012: 
  1. Murder and non-negligent manslaughter
  2. Rape
  3. Robbery
  4. Felony assault
  5. Burglary
  6. Grand larceny
  7. Grand larceny of motor vehicle

I also obtained a dataset from the 2010 US Census of the population of each borough of New York City broken down by race: 
  1. White nonhispanic
  2. Black/African American nonhispanic
  3. Asian or Pacific Islander nonhispanic
  4. American Indian and Alaska Native nonhispanic
  5. Some Other Race nonhispanic
  6. Two or More Races nonhispanic
  7. Hispanic Origin

I first performed analysis on the stop and frisk dataset, then used the crime and population data to make determinations if the amount of frisks in a given location was reasonable given the relative crime and demographics. 

##Approach##

For my analysis I primarily used the pandas package in Python to perform statistical analysis. After cleaning the data I was able to perform some basic analysis based by focusing on sex and race. From the analysis it is clear to see that disregarding all other variables, there are a lot of Black men who have been stopped, at nearly 50% of the total population. For comparison there are 1.8M Black men in New York City and in 2012 there were stops of 250,000 Black men. The second most stopped group of people were White Hispanic men. These two groups combine for nearly 70% of the total number of people stopped in 2012. 

Furthermore, the percentages of men and women by race who were subsequently frisked and then arrested were similar to the percentages of the people who were stopped. Choosing to focus on a comparison of Black men versus White men the percentage of stops in Black men led to 5% of those stopped being arrested while the percentage of stops in White men that led to arrests was higher at 6%. 

###Predicting for 'frisked' people###
  1. Wanted to create array that did not contain strings or location-based data.
  2. PCA to reduce dimensions with clustering? 
  3. Used Random Forest to classify as those 'frisked' or not 'frisked'
  4. Performed Cross Validation

##Conclusion##

When it comes to crime and society as a whole, as the technology and methods used to catch criminals becomes better and more widely available we must be ever more vigilant that they are not used to discriminate. Ironically with this push towards colder, more “scientific” ways of policing it may be important now more than ever to allocate resources properly so that we are building stronger communities and working together to prevent crime rather than stepping backwards in time to discriminate against certain peoples based on prejudices and biases that will not go away. 

###References###

  1. http://www.theatlantic.com/features/archive/2014/03/is-stop-and-frisk-worth-it/358644/
  2. http://www.nyclu.org/content/stop-and-frisk-data
  3. http://www.nyc.gov/html/nypd/html/analysis_and_planning/historical_nyc_crime_data.shtml
  4. http://www.nyc.gov/html/dcp/html/census/demo_tables_2010.shtml

