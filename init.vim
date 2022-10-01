:set number
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

Plug 'https://github.com/vim-airline/vim-airline' " Status bar
Plug 'https://github.com/preservim/nerdtree' " Tree-like file explorer
Plug 'https://github.com/tpope/vim-surround' " Surrounding ysw)
Plug 'https://github.com/tpope/vim-commentary' " For commenting gcc & gc
Plug 'https://github.com/ap/vim-css-color' " CSS color preview
Plug 'https://github.com/rafi/awesome-vim-colorschemes' " Retro scheme(s)
Plug 'https://github.com/ryanoasis/vim-devicons' " Developer icons
Plug 'https://github.com/terryma/vim-multiple-cursors' " CTRL + N for multiple cursors

Plug 'https://github.com/jiangmiao/auto-pairs' " Auto closes brackets, quotes etc
call plug#end()

nnoremap <C-f> :NERDTreeFocus<CR>
nnoremap <C-n> :NERDTreeFocus<CR>
nnoremap <C-t> :NERDTreeToggle<CR>
