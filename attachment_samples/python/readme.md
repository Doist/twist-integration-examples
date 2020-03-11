# Python Attachment Sample

This sample makes use of environment variables, please make sure you have variables configured for `TWIST_TOKEN` for this to work.

You will also need to know the IDs of either/both a thread or a conversation.

Once you've downloaded `attachment.py` and `client.py` you can run it by running either of these commands:

If you don't have [Click](http://click.pocoo.org/5/) installed, you will need to do this for the script to run
```
pip install click
```


```
python attachments.py --thread=1234 --message="attached file" --filepath="./relative/path/to/file"
```

or 

```
python attachments.py --conversation=1234 --message="attached file" --filepath="./relative/path/to/file"
```