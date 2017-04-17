# GitLabCounter

The philosophy we are using is the following:
We are using a soft version of Scrum, we divide the time in sprints, currently one week sprints.
At the begining of each sprint(Mondays) we define the work of the week. We add tasks to perform to the backlog.
If a task has been added and not executed for more than 4 sprints, it is re-valuated and added a higher prioty or discarded. The idea is to have a clean and fresh backlog and not a untidy box of things to do.

When we create a task we estimate the number of points that will take to finish it. One point tends to be 2 hours of work. For us finished means, not only code complete but also with tests that pass the task programmed.
If a task was correctly estimated it will only have one label with the points done, for example "2 pts", if the task was estimated in a different number of points than the done, we will set the donde tag, "3 pts" and then add the estimated label "Est. 2pts", so we have a record of what was estimated in the first place for future reference.

We use Gitlab's due date as the date of the sprint. We name each sprint as the date when we start it, the script uses this field to calculate the points done it a sprint.