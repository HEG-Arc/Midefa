trello-github-integration
=========================

A cool app to link Trello with GitHub in order to sync cards with issues

This app uses two python libraries to interface Trello and GitHub's API:
* https://github.com/jacquev6/PyGithub
* https://github.com/plish/Trolly

This script get the cards moved to Planned, create an issue #user-story with the card and create n issues #requirements based on the check-list items.

When an issue is closed, the card is updated (check-list item checked or card moved to done).

You should call it with a cron in order to automate the sync.
