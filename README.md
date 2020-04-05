# termite-themes
An easy tool to download and change termite themes on the fly.

This automatically downloads [base16-termite](https://github.com/khamer/base16-termite) and you can choose any theme from there.


## Installation
1. Clone the repo and in the project directory run `./setup.sh`. This should set you up with configuration and themes path.


## Usage
### List available themes
`python termite-themes.py --list`

### Randomly select a theme
`python termite-themes.py --random`

### Switch to specific theme
`python termite-themes.py --switch-to <theme name from available lists>`
**NEW** You can use tab for autocompletion.

### Help
`python termite-themes.py --help`


