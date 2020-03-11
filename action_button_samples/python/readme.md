# Action Buttons Sample

This script allows you to add action buttons to either a conversation, or a thread (you can also add them when you create a new thread).

To run this script, ensure that you have python3 installed, and make sure you have the Click module installed (`pip install click`).

Then you can run the script with parameters:

```
python3 action_button.py --message="films available" --button_text="book with cineworld" --action="open_url" --url="https://www.cinemachainsrus.co.uk" --conversation=123456
```

or
```
python3 action_button.py --message="films available" --button_text="book with cineworld" --action="open_url" --url="https://www.cinemachainsrus.co.uk" --thread=654321
```

To see all options available, please run `python3 action_button.py --help`