# GitLabCounter

The philosophy we are using is the following:

This is a soft version of Scrum, we divide the development time in sprints, currently one week sprints.
At the begining of each sprint(Mondays) we define the work of the week. We add tasks to perform to the backlog, which are added as issues on GitLab.
If a task has been added and not executed for more than 4 sprints, it is re-valuated and added a higher prioty or discarded. The idea is to have a clean and fresh backlog and not a untidy box of things to do.

When we create a task we estimate the number of points that will take to finish it. One point tends to be 2 hours of work, but this can be reevaluated from one team to another.
For us "finished" means, not only code complete but also with tests that pass the task programmed.
If a task was correctly estimated it will only have one label with the points done, for example "2 pts", if the task was estimated in a different number of points than the ones really used, we will set the done tag, "3 pts" and then add the estimated label "Est. 2pts", so we have a record of what was estimated in the first place for future reference.

Also we are using Gitlab's due date as the date of the sprint, becuause Milestones are a bigger category. We name each sprint as the date when we start it, the script uses this field to calculate the points done it a sprint.

Now that the philosophy is clear, let's explain what the code does.

It goes through the tasks of the closing sprint, counts the points Estimated and done, for the whole team and each one of the members, and then posts it on slack.