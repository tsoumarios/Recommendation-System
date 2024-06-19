# Content Overview
- Analysis
- Application

# Kmeans-API
This is a recomendation system based on clustering analysis. After clustering a user_profiles.json file wil be generated keeping the users preferences.
This system generates personalized recommendations, based on each user's preferences and other users preferences that belong in the same cluster.

* More info about the application project can be found in the README.md files on Application folder.

# Dataset - The data set is NOT included due to a confidentiality agreement

## Root
- time : A string representing the datetime when the bet was placed. The format
is yyyy-MM-dd HH:mm:ss.fff expressed as the Universal Coordinated Time
(UTC+0).
- bet : An array of bet objects placed by the user. Note: In the current context,
this array is expected to contain a single bet object.
- userid : An integer representing the unique identifier of the user who placed
the bet.

## Bet
- stake : A float representing the amount of money placed on the bet.
- pick : An array of pick objects representing the user's selections for the bet.
Note: In the current context, this array is expected to contain a single pick
object.
## Pick
- eventType : A string representing the type of event the bet is placed on. In
general, a value of "live" indicates a game that has started (i.e. after the
dateofmatch ), "pregame" indicates a game that has not started yet (i.e. before
the dateofmatch ).
- match : An object containing detailed information about the match.
- market : An object containing detailed information about the market. A market
is a specific type of bet. For example, consider a soccer game, the betting
markets for this event may be the final result of the match (win, draw, or lose
-- 1x2 ), the total number of goals scored, or the player who will score the
first goal.
- oddField : An object containing detailed information about the odd field. An
odd is a specific outcome for a related market (e.g. 1 in 1x2 ).
Match
- id : An integer representing the identifier of the match.
dateofmatch : A string representing the date and time of the match in ISO 8601
format.
- home : A string representing the home team's name.
- homeId : An integer representing the identifier of the home team.
- away : A string representing the away team's name.
- awayId : An integer representing the identifier of the away team.
- sport : A string representing the sport of the match.
- category : A string representing the category of the match.
- tournament : A string representing the tournament of the match.
- sportId : An integer representing the identifier of the sport.
- categoryId : An integer representing the identifier of the category.
- tournamentId : An integer representing the identifier of the tournament.
## Market
- freetext : A string representing the free text (name + specialoddsvalue ) of
the market.
- specialoddsvalue : A string representing the special odds value of the market.
This value indicates the specific variation of the market type. For example, in
- Total a special value of {\"total\": \"2.5\"}" refers to whether the total
number of goals scored will be less/more than 2.5. Null if not applicable.
typeid : An integer representing the type identifier of the market.
## OddField
- oddTypeId : An integer representing the odd type identifier.
- type : A string representing the type of the odd field. Following the above
example, a type of over {total} would mean that you bet on more than 2.5 goals
being scored in total.

- value : A float representing the value of the odd field. This value correlates
with the probability of this outcome.
