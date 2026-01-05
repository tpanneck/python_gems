
# Ubuntu Dev-Environment Setup

Dieses Repository dokumentiert die initiale Einrichtung meines Ubuntu-Systems. Es enthält alle notwendigen Repositories und Tools für Cloud-Development, Docker und Editoren.

## 🚀 Schnellstart (Zusammenfassung)

Um das System auf den Stand dieser History zu bringen, wurden folgende Kategorien installiert:

1. **System & Build Tools**: `git`, `make`, `gcc`, `curl`, `tmux`.
2. **Monitoring**: `btop`, `htop`.
3. **Cloud & IaC**: Terraform (HashiCorp Repo) & Google Cloud SDK.
4. **Container**: Docker CE.
5. **Runtime & Editoren**: Node.js, NPM & Vim (mit vim-plug).
6. **Grafik & Office**: GIMP & MuPDF.

---

## 🛠 Installationsschritte

### 1. System-Update & Basis-Tools
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    make \
    gcc \
    tmux \
    btop \
    clangd \
    htop
```
### 2. Cloud & Infrastructure Tools

#### Terraform (HashiCorp)
```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform
```

#### Google Cloud SDK

```bash
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt update && sudo apt install -y google-cloud-sdk
```

### 3. Docker Engine Setup
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
```

### 4. Development & Editoren
```bash
sudo apt install -y nodejs npm
curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
chmod 600 ~/.vim/autoload/plug.vim
```

### 5. Desktop-Anwendungen
```bash
sudo apt install -y gimp mupdf mupdf-tools
```

### 6. Cleanup
```bash
sudo apt autoremove -y
```

## vimrc 

Don't forget to call ```:PlugInstall```

Language packs CoC  ```:CocInstall coc-pyright coc-clangd coc-json```

```bash
" ============================================================================
" 1. PLUGINS (Vim-Plug)
" ============================================================================
call plug#begin('~/.vim/plugged')
Plug 'tpope/vim-sensible'
Plug 'dense-analysis/ale'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'tpope/vim-fugitive'
" Jedi deaktiviert, da CoC (Pyright) für Python genutzt wird
" Plug 'davidhalter/jedi-vim'
call plug#end()

" ============================================================================
" 2. OPTIK & FARBEN (Aus deiner alten Config)
" ============================================================================
syntax on
colorscheme murphy
" Kommentare in Hellblau (bessere Lesbarkeit auf dunklem Grund)
highlight Comment ctermfg=LightBlue guifg=LightBlue

set number              " Zeilennummern an
set relativenumber      " Relative Zeilennummern für schnelleres Springen
set laststatus=2        " Statuszeile immer anzeigen
set showcmd             " Befehle unten rechts anzeigen
set colorcolumn=120     " Optische Grenze bei 70 Zeichen
set scrolloff=8         " Cursor bleibt beim Scrollen mittig
set sidescrolloff=8

" ============================================================================
" 3. EDITIER-VERHALTEN (Tabs, Suche, Undo)
" ============================================================================
set expandtab           " Leerzeichen statt Tabs
set shiftwidth=4        " Einzug: 4 Leerzeichen
set softtabstop=4
set tabstop=4
set smartindent         " Intelligente Einzüge
set encoding=utf-8
set fileencodings=utf-8,latin1

set incsearch           " Suche während des Tippens
set hlsearch            " Suchergebnisse hervorheben
set showmatch           " Passende Klammern anzeigen
set noerrorbells        " Kein Piep-Ton

set splitbelow          " Neuer Split unten
set splitright          " Neuer Split rechts
set clipboard=unnamedplus " System-Zwischenablage nutzen
set undofile            " Undo-Historie über Sessions hinweg speichern

" Zeige Tabs und Leerzeichen am Ende (wichtig für Python!)
set list
set listchars=tab:>-,trail:.,extends:>,precedes:<

" ============================================================================
" 4. COC & LSP EINSTELLUNGEN (Für C und Python)
" ============================================================================
let mapleader = ","

" Enter bestätigt Auswahl im Autocomplete-Menü
inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<CR>"

" Tab zur Navigation durch Vorschläge
inoremap <expr> <TAB> pumvisible() ? "\<C-n>" : "\<TAB>"
inoremap <expr> <S-TAB> pumvisible() ? "\<C-p>" : "\<S-TAB>"

" Go-To Definitionen
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)
nmap <silent> gp <Plug>(coc-diagnostic-prev)
nmap <silent> gn <Plug>(coc-diagnostic-next)
nmap <silent> gl :<C-u>CocList diagnostics<CR>

nmap <leader> rn <Plug>(coc-rename)
nmap <leader> ac <Plug>(coc-codeaction-cursor)

" ALE + CoC Koexistenz
let g:ale_disable_lsp = 1
```
