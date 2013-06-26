# Parsegen TODO Items

This is a list of items that require attention in the project. They are roughly ordered in priorities however there is likely some overlap in the groups.

If you're a super-dooper cool coder feel free to have a go at any of these items. Once you pick one raise it as an issue so there is somewhere to track what's going on. When you're done start a pull request and I'll try and merge your contributions.

Feel free to post suggestions for other items that are not on this list as issues too.

## HIGH

## MEDIUM

* Create an Expansion object to be responsible for computing the predictions for an expansion and providing some form of signature that can be used to uniquely identify expansions within a symbol.
* Create a Token wrapper class that will expose a unified interface for terminal and nonterminals.
* Allow adding semantic actions to each expansion within the grammar, bison style.

## LOW

## HOUSEKEEPING

* Add doc-comments to all files. Doc comments should be of the form:

    """Function Name

    Paragraph or short description of the function.
    """

* Ensure that lines don't get too long. All lines should be hard-wrapped at 80 characters.