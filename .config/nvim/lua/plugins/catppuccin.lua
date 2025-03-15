return {
    --Catppuccin color scheme
    "catppuccin/nvim",
    lazy = false,
    name = "catppuccin",
    priority = 1000,
    config = function()
        require("catppuccin").setup({
            flavour = "frappe",
            background = {
                light = "frappe",
                dark = "frappe",
            },
            transparent_background = true,
            integrations = {
                indent_blankline = {
                    enabled = true,
                    scope_color = "lavender",
                    colored_indent_levels = false,
                },
                mason = true,
                neotree = true,
                neotest = true,
                native_lsp = {
                    enabled = true,
                    virtual_text = {
                        errors = { "italic" },
                        hints = { "italic" },
                        warnings = { "italic" },
                        information = { "italic" },
                        ok = { "italic" },
                    },
                    underlines = {
                        errors = { "underline" },
                        hints = { "underline" },
                        warnings = { "underline" },
                        information = { "underline" },
                        ok = { "underline" },
                    },
                    inlay_hints = {
                        background = true,
                    },
                },
                telescope = {
                    enabled = true,
                    -- style = "nvchad"
                },
                which_key = true,
            },
        })
        vim.cmd.colorscheme 'catppuccin'
    end,
}

