local bookmarks = {}

-- Проверяем, запущена ли Yazi внутри tmux (это критично для проброса fzf)
local is_tmux = os.getenv("TMUX") ~= nil

if is_tmux then
	bookmarks.cli = "fzf"
	bookmarks.fzf_args = "--tmux 100%,100% --reverse --height=40%"
else
	-- Используем новый встроенный асинхронный TUI-бэкенд для fzf в чистом терминале
	bookmarks.cli = "fzf"
	bookmarks.fzf_args = "--reverse --height=40%"
end

return bookmarks
