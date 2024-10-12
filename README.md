# python_gems
Some snippets for python programing which may be useful 


## vimrc 

" Enable syntax highlighting
syntax on

" Set colorscheme 
colorscheme murphy

" Customize comment color for better readability on dark backgrounds
highlight Comment ctermfg=LightBlue guifg=LightBlue

" Use line numbers
set number

" Enable relative line numbers
set relativenumber

" Enable mouse support in all modes
" set mouse=a

" Use spaces instead of tabs
set expandtab 
set shiftwidth=4
set softtabstop=4
set tabstop=4

" Set the number of spaces to use for each step of (auto)indent
set shiftwidth=4

" Enable smart indenting
set smartindent

" Show matching brackets
set showmatch

" Enable incremental search
set incsearch

" Highlight search results
set hlsearch

" Disable beep sound
set noerrorbells

" Set file encodings to consider
set encoding=utf-8
set fileencodings=utf-8,latin1

" Always show the status line
set laststatus=2

" Display command in bottom bar
set showcmd

" Show an undo tree visually
set undofile

" More natural split window behavior
set splitbelow
set splitright

" Enable copy and paste using system clipboard
set clipboard=unnamedplus

" Set a comfortable scrolling margin
set scrolloff=8
set sidescrolloff=8

" Some personal preferences (tk5pt)
set colorcolumn=70


function! ProcessAndInsert()
    " Öffne neuen Buffer
    execute ':new'

    " Manuell Text einfügen und zurück in den Normal-Modus wechseln (mit Esc)
    " Warte auf Einfügen des Textes
    echo "Bitte Text einfügen und dann Esc drücken, um fortzufahren."

    " Globale Variable speichern den Cursorposition und Puffer 
    let s:original_pos = getpos(".")
    let s:original_buf = bufnr("%")

    " Setzen eines Autocmd, der wartet bis der Benutzer zurück in den Normal-Modus wechselt
    augroup ProcessBuffer
        autocmd!
        autocmd InsertLeave * call s:transformAndCopy()
        " Entferne das Autocmd nach der ersten Benutzung
        autocmd InsertLeave * autocmd! ProcessBuffer
    augroup END
endfunction

function! s:transformAndCopy()
    " Führe die Transformationsbefehle aus
    execute '%!par 68rj'
    execute '%s/^/# /'
    execute '%s/^# $/# \\newline/'
    execute "0put = '# \\newline'"
    execute '%y'

    " Schließe den neuen Buffer ohne zu speichern
    execute 'bd!'

    " Wechsel zurück zum ursprünglichen Buffer und setze den Cursor an die vorherige Position
    " execute 'buffer ' . s:original_buf
    " call setpos('.', s:original_pos)

    " Gehe nicht in Insert-Modus, sondern füge den Text im Normal-Modus ein
    normal! p

    echo "Text erfolgreich eingefügt und Buffer geschlossen."
endfunction

" Befehl definieren
command! ProcessAndInsert call ProcessAndInsert()

call plug#begin('~/.vim/plugged')

Plug 'davidhalter/jedi-vim'
" Plug 'dense-analysis/ale'
Plug 'psf/black' 
" Plug 'vim-python/python-syntax' " optional
" Plug 'ycm-core/YouCompleteMe'

call plug#end()

inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<CR>"

" show spaces and tabs (important for python)
set list
set listchars=tab:>-

" nmap <leader>rn :call RenameFunction()<CR>

" function! RenameFunction()
"     let new_name = input("New name: ")
"     if new_name != ""
"         execute 'YcmCompleter RefactorRename '.new_name
"     endif
" endfunction


" Jedi-vim configuration
let mapleader = ","
let g:jedi#auto_vim_configuration = 1    " Automatische Konfiguration für Vim
let g:jedi#completions_enabled = 1       " Aktiviert Autocompletion
let g:jedi#show_call_signatures = 1      " Zeigt Funktionssignaturen im Popup
let g:jedi#use_tabs_not_buffers = 1      " Tabs für die Navigation nutzen
let g:jedi#auto_close_doc = 1            " close doc window
let g:jedi#show_call_signatures_delay = 300 "300 ms before opening call signature
