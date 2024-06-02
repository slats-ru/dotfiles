return {
    {
        --Catppuccin color scheme
        "catppuccin/nvim",
        lazy = false,
        name = "catppuccin",
        priority = 1000,
        config = function()
            require("catppuccin").setup({ transparent_background = false })
            vim.cmd.colorscheme 'catppuccin-frappe'
        end,
    },

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
        dependencies = { 'nvim-tree/nvim-web-devicons' },
        opts = {
        options = {
            theme = 'catppuccin',
            icons_enabled = true,
            component_separators = '|',
            section_separators = '|',
        },
        sections = {
        lualine_c = {'filename', 'encoding'},
        lualine_x = {
            {
            require("lazy.status").updates,
            cond = require("lazy.status").has_updates,
            color = { fg = "#ff9e64" },
            },
        },
        lualine_y = {'progress', 'location'},
        lualine_z = {'tabs', 'windows'}
        },
      }    
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
    scope = { enabled = false } }
    },

    {
    -- Useful plugin to show you pending keybinds.
    'folke/which-key.nvim', 
    opts = {} 
    },
    
    {
    -- A snazzy buffer line with tabpage integration
    'akinsho/bufferline.nvim', 
    version = "*", 
    dependencies = 'nvim-tree/nvim-web-devicons',
    opts = {
        options = {
            always_show_bufferline = true,
            mode = "buffers",
            offsets = {
                {
                    filetype = "neo-tree",
                    text = "Neo-tree",
                    highlight = "Directory",
                    text_align = "left",
                },
            },
            separator_style = "slant",
            diagnostics = "nvim_lsp",
            diagnostics_indicator = function(count, level, diagnostics_dict, context)
                local icon = level:match("error") and " " or " "
                return " " .. icon .. count
            end,
        }
      }
    }
}
