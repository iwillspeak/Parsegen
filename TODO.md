# Parsegen TODO Items

This is a list of items that require attention in the project. They are roughly ordered in priorities however there is likely some overlap in the groups.

If you're a super-dooper cool coder feel free to have a go at any of these items. Once you pick one raise it as an issue so there is somewhere to track what's going on. When you're done start a pull request and I'll try and merge your contributions.

Feel free to post suggestions for other items that are not on this list as issues too.

## HIGH

* Add command line parameters. Because what use is a command line program with no user interface.

Don't plan on having too many parameters really, the application is kind of a one-trick horse.

Something like:
`parsegen [-o <out>] [-l <lang>] <in> [option=value]*`

## MEDIUM

* Add `name` to Symbol object. This will allow iterations over the  symbols within a grammar without having to use `.items()` all the time. It should cut down on the number of parameters needed in some functions too.
* Add some form method to the Symbol object that would allow it to return the number of terminals and nonterminals in it. This may have to wait for the creation of the Token wrapper class.
* Create an Expansion object to be responsible for computing the predictions for an expansion and providing some form of signature that can be used to uniquely identify expansions within a symbol.
* Create a Token wrapper class that will expose a unified interface for terminal and nonterminals.
* Allow adding semantic actions to each expansion within the grammar, bison style.

## LOW

	* Add doc-comments to all files
* Ensure that lines don't get too long