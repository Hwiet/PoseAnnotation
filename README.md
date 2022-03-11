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

- *Temporary, will fix*:
  - The app crashes when you try to move a keypoint.
  - Saving is not implemented yet.
- *Windows only*: If you encounter a codec issue, you may need to install a codec pack such as [LAV Filters](https://github.com/Nevcairiel/LAVFilters/releases).