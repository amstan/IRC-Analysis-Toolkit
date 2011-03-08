#Highlight Graph
A tool used to graph highlights(saying another's nickname) from irc logs.

My inspiration was [piespy](http://www.jibble.org/piespy/), but I was dissapointed when it didn't have a log analysis functionality; so I made my own.

## Requirements
 * Python 2.6
 * [pygraphviz](http://networkx.lanl.gov/pygraphviz/)
 * Compatible logfiles, ideally something that supybot outputted
     * Feel free to modify the parser

## Usage:
 * `./generateGraph.py $layout file1 ...`
 * $layout can be one of: neato, dot, twopi, circo, fdp

## Examples:
 * Tested with the [#aichallenge channel logs](http://contestbot.hypertriangle.com/)
 * [Output](http://csclub.uwaterloo.ca/~amstan/%23aichallenge%20highlight%20graph/)