# Action Buttons Sample

This script allows you to add action buttons to either a conversation, or a thread (you can also add them when you create a new thread).

This sample makes use of environment variables, please make sure you have variables configured for `TWIST_TOKEN` for this to work.

You can run the script with parameters:

```
go run . --message="films available" --buttontext="book at the cinema" --action="open_url" --url="https://www.cinemachainsrus.co.uk" --conversation=123456
```

or
```
go run . --message="films available" --buttontext="book at the cinema" --action="open_url" --url="https://www.cinemachainsrus.co.uk" --thread=654321
```

To see all options available, please run `go run . --help`