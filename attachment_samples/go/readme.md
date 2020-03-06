# Go Attachment Sample

This sample makes use of environment variables, please make sure you have variables configured for `twist_token` for this to work.

You will also need to know the IDs of either/both a thread or a conversation.

Once you've downloaded the sample folder simply run it:

```
go run .
```

To determine which type of message (conversation/thread) should be posted, you should edit the `attachments.go` file and change the method call in `main()`