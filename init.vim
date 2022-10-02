:set number
:set relativenumber
:set autoindent
:set tabstop=4
:set shiftwidth=4
:set smarttab
:set softtabstop=4
:set mouse=a
:set encoding=UTF-8
:set wildoptions+=pum
:set wildmode=full

call plug#begin()

Plug 'vim-airline/vim-airline' " Status bar
Plug 'preservim/nerdtree' " Tree-like file explorer
Plug 'tpope/vim-surround' " Surrounding ysw)
Plug 'tpope/vim-commentary' " For commenting gcc & gc
Plug 'ap/vim-css-color' " CSS color preview
Plug 'rafi/awesome-vim-colorschemes' " Retro scheme(s)
Plug 'ryanoasis/vim-devicons' " Developer icons
Plug 'terryma/vim-multiple-cursors' " CTRL + N for multiple cursors
Plug 'jiangmiao/auto-pairs' " Auto closes brackets, quotes etc
Plug 'preservim/tagbar' " Auto closes brackets, quotes etc
Plug 'neoclide/coc.nvim', {'branch': 'release'} " Auto closes brackets, quotes etc

call plug#end()

let g:NERDTreeDirArrowExpandable="+"
let g:NERDTreeDirArrowCollapsible="-"
let g:tagbar_autofocus=1
let g:tagbar_iconchars=['+', '-']

nnoremap <C-f> :NERDTreeFocus<CR>
nnoremap <C-n> :NERDTree<CR>
nnoremap <C-t> :NERDTreeToggle<CR>

:colorscheme onehalfdark

nmap <F8> :TagbarToggle fj<CR>
