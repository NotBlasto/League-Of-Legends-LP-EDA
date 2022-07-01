# Exploratory Data Analysis - League of Legends
## Introduction
League of Legends is the most popular Mobile Online Battle Arena (MOBA) game in the world, with some professional players within esports organizations reportedly earning in the millions of dollars each each year. At reportedly over 100 million active users per month, gamers around the world are constantly seeking to improve their skills and overall ladder ranking to pursue the dream of becoming a League of Legends professional.

As an avid player and lover of League of Legends since Season 2, throughout my years playing the game I have come across a multitude of rumors related to LP gain shared amongst the playerbase. Rumors centered around rating gains (LP) were extremely common in early League of Legends primarily due to the nontransparent nature of their ranking system in place during this time. The most prevalent of these rumors shared the sentiment that if a given player wins games consecutively, they will gain more LP per game, therefore ranking up faster. To players with little to no way of truly understanding their own rating gains this idea seemed logical to many, myself included. After nearly a decade of believing this rumor, I became curious as to what data is actually tracked on player accounts by Riot Games. After my first API request, I was absolutely stunned to see a boolean value labeled 'hotStreak' on player accounts. Could this rumor really have been true all this time? This is what I set off to find out.

## The Data
Upon setting out to find the answer to my question, I knew the first thing that must be done is determining what influences this hotStreak value to become True. I achieved this by performing an initial API request to retrieve a list of players, separating the players into those with a True and False hotStreak values separately, and manually looking at each player's match history to determine a correlation between the user's who have a True hotStreak value and consecutively winning. It was found that the least amount of consecutive wins necessary to make the hotStreak value True is 2 consecutive wins. 

With the constraints behind the HotStreak value revealed, I began webscraping the entire match history of players(summoners) with a True hotStreak value through the combined usage of Selenium and popular player statistics tracking website U.gg. The unorganized data is manipulated and cleaned with Pandas where each player's entire match history is sorted into consecutive and nonconsecutive wins to determine the impact consecutively winning truly has on player rating gains.

## The Truth
After collecting enough data on player matches, it has been determined that the amount of player rating gained is on average 1.4 - 1.5, or ~11.1% more per win while consecutively winning in League of Legends. With this amount of fluctuation in rating increases, it is not entirely unreasonable to assume this variable may have an impact on the amount of rating a player gains. However, the data does beg the question of whether or not the 11% rating gain comes directly from the hotStreak variable, or if other systems, such as the MMR, or Matchmaking Rating level of the matches could explain the higher rating gained during these games. What do you think?

![26ceddcac6d9fd4a410462fa2ea13c63](https://user-images.githubusercontent.com/95455528/176819692-3fd0b2ca-019f-465b-b135-1389c79b5560.png)

## What's Next?
Truthfully, this project provides an excellent base to collect a multitude of insights throughout League of Legends, and I plan to use it for many projects to come. I plan to expand this project and provide more rating insights to players such as overall average amounts of LP gained and lost within each league bracket (Diamond, Gold, Silver, etc.), as well as possibly deploy a web application tool that leverages machine learning to predict the outcome of matches off of only the information available in champion select, so look out for that!


