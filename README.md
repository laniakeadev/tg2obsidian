# tg2obsidian

This script parses output from Telegram channel and converts each post to 
Obsidian post in markdown.

Telegram Desktop creates JSON file, as well as different directories containing
multimedia, photos, etc. This script creates new directory and populates it with
formatted posts ready to publish.

## basic usage

Firstly you need to export your channel history from Telegram Desktop app.
This could be done from three dots menu. Then popup menu appears, where
you can choose what data you want to export. The script currently supports
only photos, voice messages and audio files.

![tg-export](docs/tg-export.png)

In format menu you should specify 'Machine-readable JSON' file and then
locate to directory of your desire.

To convert your posts to markdown files you need to run `tg2md.py` program
which takes path to folder that contain `result.json` file as first argument.

```console
$ python tg2md.py path/to/
```

By default it will create `formatted_posts` directory in your current directory
and populate it with markdown files. If you want to specify other location,
use `--out-dir` flag

```console
$ python tg2md.py path/to/ --out-dir path/to/post/output
```

## Original author

Forked from [tg2md](https://github.com/la-ninpre/tg2md) in 2021, original author - [la-ninpre](https://github.com/la-ninpre)
