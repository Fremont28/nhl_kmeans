# nhl_kmeans
Clustering NHL defenseman playing styles 

Many NHL defenseman are tasked with defending both their net while providing a steady supply of offensive production. Aside from these two key roles, the playing style of defenseman varies widely across the league. Some defenseman are more aggressive in the offensive zone and others focus on eliminating odd-man rush situations.   

Using primarily offensive metrics (on even strength) from the 2017-18 regular season, we split NHL defenseman into five groups using K-means clustering. Defenseman included in our sample had to play a minimum number of games and minutes per game based on their even strength statistics.  For reference, K-means clustering is an unsupervised algorithm that separates samples on n groups of equal variance minimizing the within–cluster sum of squares. 

Players were clustered based on traditional and advanced hockey metrics including but not limited to points per game, Corsi For% (detailed later), expected goals for (xGF), and percent of offensive zone starts (ZSR).  

Based on the K-means results, we found that Group three (29 players) has the most prolific collection of defenseman. Players in this group averaged 8.16 points shares, which is 4.05 points higher than the next highest Group one’s total. 

Group three is characterized by ice-logging defenseman that tend are also offensively oriented. This group averages 18.1 minutes per game and 57.5 expected goals for (xGF) or 7.5% xGF above the NHL average. Based on these numbers, Group three is obviously littered with talent featuring players like Alex Pietrangelo, Brent Burns, and P.K. Subban. 

Read Here: 
