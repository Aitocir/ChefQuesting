# ChefQuesting

ChefQuesting is a text-based, client-server game played in the terminal that supports multiplayer over a LAN or the Internet. It has no persistent account information, as player information is tied to the connection address, and is all forgotten the moment the player disconnects from the game server. The idea is it's like a board game: once it's over, it's over and you can play another game with no ties to previous games. The inventory and stat meters (currently only suports hunger, though it isn't used by the game yet, it just silently goes up) are common to the entire party. Right now, games can be left and joined at any point, but soon they will be locked to the party it started with to prevent odd game behavior.

It's written entirely in Python, as the long-term goal is cross-platform support. The server has been tested in Debian Linux and OS X, and the client has only been tested on OS X. Support for Windows 10 shouldn't be a problem with the new support for console codes Win10 has introduced the client currently uses. 

## Commands

Right now, the commands are all case sensitive, and will only work in the lower case.

The following commands work in the game lobby (where players land when they first join the server):
* __create__: this command creates a new game, and requires an 'as' clause to choose the creating player's class, for example: "create as knight"
* __join__: this command joins an existing game, and requires a game name and an 'as' clause for class choice, for example: "join ColdBrownShoe as bandit"

These commands work in a game:
* __leave__: this command leaves the current game and returns the player to the Lobby
* __look__: this command causes the player to analyze in the provided direction; options include north, south, east, west, and here for the current map tile, for example "look north" will describe the map tile one to the north of the player's current position
* __go__: this command moves the game party in the provided direction if it's valid, such as "go north". Valid directions are north, south, east, and west
* __check__: this command currently takes no arguments and lists the ingredient list showing what the party has left to find, ending the game if there are no ingredients left to find. In the future, it will takes arguments to do that, or check the party's hunger, the current game time, and so on
* __search__: this command causes the players to search the current location for ingredients on their list
* __attack__: this command causes the party to engage in battle with a monster if there is one at the current location
* __eat__: NOT MADE YET (this will lower the hunger meter, which is implemented but not used yet)

These commands are global, and work in or out of game:
* __logout__: this command disconnects from the server. Accepted aliases include "logoff" and "disconnect"
* __quit__: this commands quit outs of the client program altogether
* __say__: this command creates a chat shared with other players in the same game, or in the lobby with you, for example "say hello friends" will send "hello friends" to the room you're in
* __rename__: this command changes the player's name, which is auto-assigned to a random name at first, for example "rename Bob" will change the player's name to Bob
