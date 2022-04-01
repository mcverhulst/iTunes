#### iTunes search

This script prompts users to enter a search term that will be sent to the iTunes API. The user's search term will then be used to search for songs, movies, and other media. Custom classes for each of the previously mentioned media types are used to organize the responses and give each media-type its own .info() method that returns relevent data such as artist, director, and date of publication.

The user is then presented with an indexed list of the results sorted by media type. The user can then enterthe number of the item they would like to see and that item's iTunes page will be launched in their browser. If the user doesn't find what they are looking for they can enter a new search term at this point. Additionally, if the user inputs a number that is out of range for the results presented it will be treated as a new query.
