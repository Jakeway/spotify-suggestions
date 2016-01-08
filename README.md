[![Build Status](https://travis-ci.org/Jakeway/spotify-suggestions.svg?branch=master)](https://travis-ci.org/Jakeway/spotify-suggestions)

# spotify-suggestions
an app to get suggestions based on your spotify music

## how it works
spotify-suggestions looks at your saved tracks (looking at your playlists is also in the TODO) and then tries to match
you with users who have similar tastes. once matched up, spotify-suggestions will recommend other tracks saved by your matches.

## TODO
* add tests
* make the spotify api calls more robust (currently it always assumes a 200 response)
* come up with a better name...
* add user's playlist music to the database to get a larger sample
* work on the website design (yeah, I know it's bad)
* work on enhancing the suggestion algorithm
  * currently, suggesting music based on Spotify's 'popularity' field
  * try getting the most common genre of the matching songs, and suggest a song belonging to that genre (echo nest api)
