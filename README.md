# Task Manager

The tools are tied together by one super-command (task) and a set of sub-commands.
This is similar to `git.

## Task Command Set

* `add`: Add new task
* `del`: Delete existing task

## Command-line completion (bash/zsh)
All you need to do to enable full command line completion
is:

```bash
pip install argcomplete
eval "$(register-python-argcomplete task)"
```

The "pip install" only needs to be done once.  If you get an error while trying
to install argcomplete, you might need to use `sudo pip install argcomplete`.
The `eval` statement can be put into your .bashrc for persistence.


## Examples


### "task add" examples

| Command | Purpose |
| ------- | --------|
| `add` | add new task (recent interrupt) |
| `add -t build` | add new 'Build' task |

### "task del" examples

| Command | Purpose |
| ------- | --------|
| `task del` | del existing task |

