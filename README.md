# tg2obsidian

## Preamble

Concerned with Telegram (three-letters project) privacy issues but binded with it your life or have favourite bloggers that don't use secure services? With this script you can **make a migration of a channel or saved messages** to your local knowledge system with a single command.

This script parses output from Telegram channel and converts each post to post in markdown, files used in Obsidian and [other note-taking apps](https://www.markdownguide.org/tools/) that use Markdown (Joplin, Simplenote)

Telegram Desktop creates JSON file, as well as different directories containing
multimedia, photos, etc. This script creates new directory and populates it with
formatted posts ready to publish.

## 🛑 Ethical Use Disclaimer  

This tool is **not** intended for:  
- Tracking, monitoring, or collecting personal information about individuals.  
- Doxxing, bullying, or any form of cyberstalking.
- Unauthorized data collection or surveillance.
- Any activity that invades privacy or causes harm.  

Please use this tool responsibly and ethically.  If you disagree with these terms, do not use this tool.

## Basic usage

Firstly you need to export your channel history from Telegram Desktop app.
This could be done from three dots menu. Then popup menu appears, where
you can choose what data you want to export. The script currently supports
only photos, voice messages and audio files.

![tg-export](docs/tg-export.png)

In format menu you should specify 'Machine-readable JSON' file and then
locate to directory of your desire.

Clone the repository or download main.py, /src/ and /configs/ (keeping the structure)

To convert your posts to markdown files you need to run `main.py` script from cmd or PowerShell
which takes path to folder that contain folder with `result.json` file as first argument.

```console
$ python main.py path/to/
```

`-h` to list help

By default it will create `formatted_posts` directory in your current directory
and populate it with markdown files. If you want to specify other location,
use `--out-dir` flag

```console
$ python main.py path/to/ --out-dir path/to/post/output
```

## Known issues
- Limited flexibility
- Nested formatting is not supported
- Limited logging

## To do
- Parse nested formatting
- Divide my primary post type
- Calculate hashes
- Expand config options
- Ability to run immediatly with preset config

## Original author

Forked from [tg2md](https://github.com/la-ninpre/tg2md) in 2021, original author - [la-ninpre](https://github.com/la-ninpre)
