return {
    {
        "NvChad/nvim-colorizer.lua",
        config = function()
            require("colorizer").setup {
                user_default_options = {
                    names = false, -- "Name" codes like Blue or blue
                }
            }
            -- execute colorizer as soon as possible
            vim.defer_fn(function()
                require("colorizer").attach_to_buffer(0)
            end, 0)
        end,
    },

    {
    -- Set lualine as statusline
    'nvim-lualine/lualine.nvim',
    -- Здесь ОСТАВЛЯЕМ только иконки, никаких catppuccin внутри dependencies!
    dependencies = { 'nvim-tree/nvim-web-devicons' },
    opts = {
        options = {
            -- Используем 'catppuccin-frappe' (так как в теме у вас указан флейвор frappe)
            theme = 'catppuccin-frappe',
            icons_enabled = true,
            component_separators = '|',
            section_separators = '|',
        },
        sections = {
            lualine_c = { 'filename', 'encoding' },
            lualine_x = {
                {
                    require("lazy.status").updates,
                    cond = require("lazy.status").has_updates,
                    color = { fg = "#ff9e64" },
                },
            },
            lualine_y = { 'progress', 'location' },
            lualine_z = { 'tabs', 'windows' }
        },
    },

    {
        {
            'nvim-lualine/lualine.nvim',
            dependencies = { 'nvim-tree/nvim-web-devicons' },
            opts = {
                options = {
                    -- Возвращаем "auto", чтобы lualine просто взял цвета активной темы catppuccin
                    theme = 'auto',
                    icons_enabled = true,
                    component_separators = '|',
                    section_separators = '|',
                },
                sections = {
                    lualine_c = { 'filename', 'encoding' },
                    lualine_x = {
                        {
                            require("lazy.status").updates,
                            cond = require("lazy.status").has_updates,
                            color = { fg = "#ff9e64" },
                        },
                    },
                    lualine_y = { 'progress', 'location' },
                    lualine_z = { 'tabs', 'windows' }
                },
            }
        },
    },
},

    {
        -- Add indentation guides even on blank lines
        "lukas-reineke/indent-blankline.nvim",
        main = "ibl",
        opts = {
            indent = {
                char = "│",
                tab_char = "│",
            },
            scope = { enabled = false }
        }
    },

    {
        -- Useful plugin to show you pending keybinds.
        'folke/which-key.nvim',
        opts = {}
    },

    {
        "akinsho/bufferline.nvim",
        optional = true,
        opts = function(_, opts)
            if (vim.g.colors_name or ""):find("catppuccin") then
                opts.highlights = require("catppuccin.special.bufferline").get_theme()
            end
        end,
    },

    {
        -- a fast and fully programmable greeter for neovim
        "goolord/alpha-nvim",
        event = "VimEnter",
        enabled = true,
        init = false,
        opts = function()
            local dashboard = require("alpha.themes.dashboard")
            -- Define and set highlight groups for each logo line
            vim.api.nvim_set_hl(0, "NeovimDashboardLogo1", { fg = "#ea999c" })    -- Maroon
            vim.api.nvim_set_hl(0, "NeovimDashboardLogo2", { fg = "#e5c890" })    -- Yellow
            vim.api.nvim_set_hl(0, "NeovimDashboardLogo3", { fg = "#a6d189" })    -- Green
            vim.api.nvim_set_hl(0, "NeovimDashboardLogo4", { fg = "#81c8be" })    -- Teal
            vim.api.nvim_set_hl(0, "NeovimDashboardLogo5", { fg = "#8caaee" })    -- Blue
            vim.api.nvim_set_hl(0, "NeovimDashboardLogo6", { fg = "#babbf1" })    -- Lavender
            vim.api.nvim_set_hl(0, "NeovimDashboardUsername", { fg = "#ca9ee6" }) -- Mauve
            dashboard.section.header.type = "group"
            dashboard.section.header.val = {
                {
                    type = "text",
                    val = "   ███╗   ██╗███████╗ ██████╗ ██╗   ██╗██╗███╗   ███╗ ",
                    opts = { hl = "NeovimDashboardLogo1", shrink_margin = false, position = "center" },
                },
                {
                    type = "text",
                    val = "   ████╗  ██║██╔════╝██╔═══██╗██║   ██║██║████╗ ████║ ",
                    opts = { hl = "NeovimDashboardLogo2", shrink_margin = false, position = "center" },
                },
                {
                    type = "text",
                    val = "   ██╔██╗ ██║█████╗  ██║   ██║██║   ██║██║██╔████╔██║ ",
                    opts = { hl = "NeovimDashboardLogo3", shrink_margin = false, position = "center" },
                },
                {
                    type = "text",
                    val = "   ██║╚██╗██║██╔══╝  ██║   ██║╚██╗ ██╔╝██║██║╚██╔╝██║ ",
                    opts = { hl = "NeovimDashboardLogo4", shrink_margin = false, position = "center" },
                },
                {
                    type = "text",
                    val = "   ██║ ╚████║███████╗╚██████╔╝ ╚████╔╝ ██║██║ ╚═╝ ██║ ",
                    opts = { hl = "NeovimDashboardLogo5", shrink_margin = false, position = "center" },
                },
                {
                    type = "text",
                    val = "   ╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═══╝  ╚═╝╚═╝     ╚═╝ ",
                    opts = { hl = "NeovimDashboardLogo6", shrink_margin = false, position = "center" },
                },
                {
                    type = "padding",
                    val = 1,
                },
                {
                    type = "text",
                    val = "Пока мы улыбаемся - мы живы, а пока мы живы - мы сильнее времени.",
                    opts = { hl = "NeovimDashboardUsername", shrink_margin = false, position = "center" },
                },
            }
            -- stylua: ignore
            dashboard.section.buttons.val = {
                dashboard.button("f", " " .. " Find file", "<cmd> Telescope find_files <cr>"),
                dashboard.button("n", " " .. " New file", "<cmd> ene <BAR> startinsert <cr>"),
                dashboard.button("r", " " .. " Recent files", "<cmd> Telescope oldfiles <cr>"),
                dashboard.button("g", " " .. " Find text", "<cmd> Telescope live_grep <cr>"),
                dashboard.button("l", "󰒲 " .. " Lazy", "<cmd> Lazy <cr>"),
                dashboard.button("u", " " .. " Update plugins", "<cmd>lua require('lazy').sync()<CR>"),
                dashboard.button("m", "󱌣 " .. " Mason", "<cmd> Mason <cr>"),
                dashboard.button("q", " " .. " Quit", "<cmd> qa <cr>"),
            }
            vim.api.nvim_set_hl(0, "AlphaHeader", { fg = "#e5c890" })   -- Dark Indigo
            vim.api.nvim_set_hl(0, "AlphaButtons", { fg = "#babbf1" })  -- Lavender
            vim.api.nvim_set_hl(0, "AlphaShortcut", { fg = "#ea999c" }) -- Maroon
            vim.api.nvim_set_hl(0, "AlphaFooter", { fg = "#babbf1" })   -- Lavender

            for _, button in ipairs(dashboard.section.buttons.val) do
                button.opts.hl = "AlphaButtons"
                button.opts.hl_shortcut = "AlphaShortcut"
            end
            dashboard.section.header.opts.hl = "AlphaHeader"
            dashboard.section.buttons.opts.hl = "AlphaButtons"
            dashboard.section.footer.opts.hl = "AlphaFooter"
            dashboard.opts.layout[1].val = 3
            return dashboard
        end,
        config = function(_, dashboard)
            -- close Lazy and re-open when the dashboard is ready
            if vim.o.filetype == "lazy" then
                vim.cmd.close()
                vim.api.nvim_create_autocmd("User", {
                    once = true,
                    pattern = "AlphaReady",
                    callback = function()
                        require("lazy").show()
                    end,
                })
            end

            require("alpha").setup(dashboard.opts)

            vim.api.nvim_create_autocmd("User", {
                once = true,
                pattern = "LazyVimStarted",
                callback = function()
                    local stats = require("lazy").stats()
                    local ms = (math.floor(stats.startuptime * 100 + 0.5) / 100)
                    dashboard.section.footer.val = "⚡ Neovim loaded "
                        .. stats.loaded
                        .. "/"
                        .. stats.count
                        .. " plugins in "
                        .. ms
                        .. "ms"
                    pcall(vim.cmd.AlphaRedraw)
                end,
            })
        end,
    },
}
