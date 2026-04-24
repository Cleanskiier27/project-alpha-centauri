# Git Analysis Patterns

## File Blame (Line-by-Line Authorship)
To see who changed which lines in a file:
`git blame -L <start>,<end> <file_path>`

## File History (Commit Log for File)
To see all commits that touched a file:
`git log --follow --patch <file_path>`

## Find Content in History
To search for a string across all past commits:
`git log -S "<string>"`

## Visualizing Branch Merges
`git log --graph --oneline --all`

## Repository Statistics
`git shortlog -sn --all`
