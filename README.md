# acme-voting

# cloud formation notes

1) create s3 bucket + subfolders; "input", "transcoded", "scripts"
2) create sns topic "transcode"
3) create dynamodb tables; "VOD_Info", "votes"
4) create ETS Pipeline
5) copy / clone s3 files from github
6) create the lambda functions (pulling down .zip's from github)
7) create presetId(s) ()
8) Create IAM roles; TranscodeVideo.py,

![alt text](/Architecture.png "Frac-Voting Architecture Diagram")
