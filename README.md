# Lichess Sample Population Generator
This project generates a sample population from the lichess userbase using the Lichess API. It does this by recursively taking the followers of known players until it hits a size limit.
# How to use
User info is stored in a json file named "data.json", so make sure it doesn't already exist when using this program for the first time.
This program uses a console system which prompts for commands

# Commands:
* "q" to quit
* "list" to print current population
* "add" to add a player to the population
* "followers" to add everyone following a player to the population
* "recursive_followers" to recursively add followers, starting with a single person, until number of added exceeds a certain limit. This should be used to generate the sample population.
 * This command utilizes a limit to avoid adding the followers of people with too many followers. To change this limit, change the "MAX_FOLLOWERS" const.
* "s" to save data to "data.json"

# Personal Thoughts
I created this program in a span of 24 hours as I frantically tried to finish my IA by the deadline (I didn't). However, this project marks the first time I use an API, which was surprisingly easier than I thought it would be. I also used python libraries such as json and worked with external files.