"Plugins
call plug#begin(stdpath('data') . '/plugged')
    " fzf
    Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
    Plug 'junegunn/fzf.vim'
    " Goyo
    Plug 'junegunn/goyo.vim'
    " treesitter
    Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
    " vim-bufkill
    Plug 'qpkorr/vim-bufkill'
    " vim-snippets
    Plug 'honza/vim-snippets'
    " dracula colorscheme
    Plug 'dracula/vim', { 'as': 'dracula' }
    " vim-codefmt
    Plug 'google/vim-maktaba'
    Plug 'google/vim-codefmt'
    " Coc
    Plug 'neoclide/coc.nvim', {'branch': 'release'}
    " vifm
    Plug 'vifm/vifm.vim'
    " vim-buftabline
    Plug 'ap/vim-buftabline'
call plug#end()

"Plugins options
" fzf
let g:fzf_preview_window=['right:70%'] " preview window, right, 70% of space
let g:fzf_buffers_jump = 1 " jump to existing window if possible
" treesitter
lua <<EOF
require'nvim-treesitter.configs'.setup {
    highlight = {
        enable = true,
    },
    indent = {
        enable = true,
    },
}
EOF
" vim-codefmt
augroup autoformat_settings
  autocmd FileType bzl AutoFormatBuffer buildifier
  autocmd FileType c,cpp,proto,javascript,arduino AutoFormatBuffer clang-format
  autocmd FileType dart AutoFormatBuffer dartfmt
  autocmd FileType go AutoFormatBuffer gofmt
  autocmd FileType gn AutoFormatBuffer gn
  autocmd FileType html,css,sass,scss,less,json AutoFormatBuffer js-beautify
  autocmd FileType java AutoFormatBuffer google-java-format
  autocmd FileType python AutoFormatBuffer yapf
  autocmd FileType rust AutoFormatBuffer rustfmt
  autocmd FileType vue AutoFormatBuffer prettier
augroup END
" coc
function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction
" vifm

"Transparency
let t:is_transparent = 0

function! Toggle_background()
    if t:is_transparent == 1
        hi Normal guibg=#1D1F26 ctermbg=black
        let t:is_transparent = 0
    else
        hi Normal guibg=NONE ctermbg=NONE
        let t:is_transparent = 1
    endif
endfunction

"General settings
set encoding=UTF-8 " encoding file to utf8
filetype plugin indent on " Enable detection, plugin and indent
syntax enable " enable syntax highlighting
set autoread " auto re-read files that have been changed outside nvim
set spell spelllang=en_us " spell check as English
set hidden " hide file buffers when opening new files instead of closing them
set nowrap " no wrap line, just one long big line
" menu for command line completion
set wildmenu
set wildmode=longest:full,full
set backspace=indent,eol,start " backspace behave like a normal backspace
set confirm " prompt question instead of printing errors on commands like :q
" a tab is worth 4 spaces
set shiftwidth=4 
set tabstop=4
set softtabstop=4
set expandtab
set autoindent " enable indentation
set smartindent " indentation made smarter (works better for C like language)
" prevent inserting comments on new lines
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o
set hls " highlight all matches from previous search pattern
set is " highlight all matches for search pattern as you type it
set ic " ignore case for search pattern
set laststatus=2 " always print line status
set cmdheight=1 " number of line for the command line
set splitbelow " when splitting horizontal, put the new window under the current one
set splitright " when splitting vertical, put the new window to the right of the current one
" no backup
set nobackup
set nowritebackup
set number " display the current line number
set relativenumber " display the relative line number
set colorcolumn=81 " display a bar on the right to limit at 80 char
set cursorline " highlight current line
set updatetime=300 " more frequent update time (recommended by coc)
set shortmess+=c " remove some message to avoid spamming by coc
set signcolumn=number " display sign column on the number one

"Colorscheme
set background=dark
set termguicolors
colorscheme dracula
hi Normal guibg=#1D1F26 ctermbg=black

"Status line
set statusline=
set statusline+=%#PmenuSbar# " left side color
set statusline+=\ %M " is file modified
set statusline+=\ %y " file type
set statusline+=\ %r " is file read only
set statusline+=\ %F " full path to file
set statusline+=%= " go to right side
set statusline+=%#PmenuSel# " right side color
set statusline+=\ %c:%l/%L " position in the file
set statusline+=\ %p%% " seen percentage of the file
set statusline+=\ [%n] " buffer number

"Key bindings
let mapleader="," " map leader to comma
" open split
nnoremap <leader>v :vsplit<CR>
nnoremap <leader>h :split<CR>
" resize windows with arrow keys
nnoremap <Up> :resize +2<CR>
nnoremap <Down> :resize -2<CR>
nnoremap <Left> :vertical resize +2<CR>
nnoremap <Right> :vertical resize -2<CR>
" move around split with control + direction
nnoremap <C-h> <C-W>h
nnoremap <C-j> <C-W>j
nnoremap <C-k> <C-W>k
nnoremap <C-l> <C-W>l
" move around buffers
nnoremap <leader>h :bp<CR>
nnoremap <leader>l :bn<CR>
nnoremap <leader>x :BD<CR>
" spell check
nnoremap <leader>sf :set spelllang=fr<CR>
nnoremap <leader>se :set spelllang=en_us<CR>
nnoremap <leader>st :set spell!<CR>
" fzf
nnoremap <leader>ff :Files .<CR> 
nnoremap <leader>fl :Lines<CR>
nnoremap <leader>fbl :BLines<CR>
nnoremap <leader>fs :Snippets<CR>
" Goyo
nnoremap <leader>G :Goyo<CR> " toggle Goyo
" Coc
" Use tab for trigger completion with characters ahead and navigate
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"
" Use <c-space> to trigger completion.
inoremap <silent><expr> <c-space> coc#refresh()
" Make <CR> auto-select the first completion item and notify coc.nvim to
" format on enter
inoremap <silent><expr> <cr> pumvisible() ? coc#_select_confirm()
                              \: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"
" vifm
nnoremap <leader>o :Vifm<CR>
                              \: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"
let g:coc_snippet_next = '<tab>'
