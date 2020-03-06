# Python Attachment Sample

This sample makes use of environment variables, please make sure you have variables configured for `twist_token` for this to work.

You will also need to know the IDs of either/both a thread or a conversation.

Once you've downloaded `attachment.py` simply import it and call one of the methods:

```
python 
>>> import attachments as at
>>> at.upload_attachment_to_thread("hello from python")
>>> at.upload_attachment_to_conversation("hello from python")
```