When working with AI agents, I often work on the same files with `vim`
while agents are editing

Agents are good at understanding that a file is being modified and 
reload before applying changes and work well in updating files
incrementally

The problem was that `vim` would find the file modified and ask to
reload and overwrite your changes (unless you copy, save the latest
change)

A solution I've found is to add this to `.vimrc`

```
function! AutoReload()
  silent! checktime
endfunction

call timer_start(1000, {-> AutoReload()}, {'repeat': -1})
```

So vim is reloading the file automatically, minimizing the chances
of human-AI "collision"

The only thing that I miss is that sometimes I used the state of vim
to overwrite some git operation, e.g., `git reset --hard` while keeping
a file in vim and then overwriting it
