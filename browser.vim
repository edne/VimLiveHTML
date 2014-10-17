fu! StartBrowserFunc()
    exec "!python $HOME/.vim/plugin/browser.py start % &"
    redraw!
    augroup browsergroup
        autocmd BufWritePost * :exec "!python $HOME/.vim/plugin/browser.py refresh &" | :redraw!
    augroup END
endfu

fu! StopBrowserFunc()
    exec "!python $HOME/.vim/plugin/browser.py close &"
    redraw!
    augroup browsergroup
        autocmd!
    augroup END
endfu

command! BrowserStart :call StartBrowserFunc()
command! BrowserStop :call StopBrowserFunc()
