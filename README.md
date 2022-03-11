## Set up for first run

Set up using [pipenv](https://pipenv.pypa.io/):

```bash
pipenv install
```

## Run the app

```bash
pipenv run python -m pose_annotation
```

## Basic usage

- Go to File > Import, or `Ctrl+O` to open the import dialog.
- Select a media file and a matching annotation `.txt` file.
- Use the arrow keys to nagivate each frame.

## Known issues

- *Temporary, will fix*: The app crashes when you try to move a keypoint.