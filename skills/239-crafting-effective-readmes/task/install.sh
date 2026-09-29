#!/usr/bin/env bash
# 一键安装脚本：把 dotfiles 链接到 home 目录
set -euo pipefail

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "==> 开始安装 dotfiles（来源：$DOTFILES_DIR）"

# 备份已存在的文件
backup_file() {
  local src="$1"
  if [ -e "$HOME/$src" ] && [ ! -L "$HOME/$src" ]; then
    echo "   备份 $HOME/$src -> $HOME/$src.bak"
    mv "$HOME/$src" "$HOME/$src.bak"
  fi
}

link_dotfile() {
  local src="$1"
  backup_file "$src"
  echo "   链接 $src"
  ln -sfn "$DOTFILES_DIR/$src" "$HOME/$src"
}

# 链接各配置文件
for f in .zshrc .gitconfig .gitignore_global starship.toml .tmux.conf; do
  link_dotfile "$f"
done

# lazygit 配置
mkdir -p "$HOME/.config/lazygit"
ln -sfn "$DOTFILES_DIR/lazygit/config.yml" "$HOME/.config/lazygit/config.yml"

# 安装依赖
if command -v brew >/dev/null 2>&1; then
  echo "==> 安装 zsh / starship / tmux / lazygit"
  brew install zsh starship tmux lazygit
elif command -v apt-get >/dev/null 2>&1; then
  echo "==> apt 安装"
  sudo apt-get update && sudo apt-get install -y zsh tmux
fi

echo "==> 安装完成。执行 source ~/.zshrc 生效。"
