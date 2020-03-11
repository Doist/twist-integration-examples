# Go Attachment Sample

This sample makes use of environment variables, please make sure you have variables configured for `TWIST_TOKEN` for this to work.

You will also need to know the IDs of either/both a thread or a conversation.

Once you've downloaded the sample folder simply run it:

```
go run . --conversation=1234 --message="hello there" --filepath="/relative/path/to/file"
```

or 

```
go run . --thread=4321 --message="hello there" --filepath="/relative/path/to/file"
```