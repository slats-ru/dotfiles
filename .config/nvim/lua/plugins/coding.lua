return {  
    -- Detect tabstop and shiftwidth automatically based on the current file
    'tpope/vim-sleuth',

    { 
        -- "gc" to comment visual regions/lines
        'numToStr/Comment.nvim',         
        opts = {} 
    },

    {
        -- 
        "windwp/nvim-autopairs",
        -- Optional dependency
        dependencies = { 'hrsh7th/nvim-cmp' },
        config = function()
            require("nvim-autopairs").setup {}
            -- If you want to automatically add `(` after selecting a function or method
            local cmp_autopairs = require('nvim-autopairs.completion.cmp')
            local cmp = require('cmp')
            cmp.event:on(
            'confirm_done',
            cmp_autopairs.on_confirm_done()
            )
        end,
    },

    {
        -- Adds LSP completion capabilities
        "hrsh7th/cmp-nvim-lsp"
    },

    {
        -- Snippet Engine & its associated nvim-cmp source
        "L3MON4D3/LuaSnip",
        dependencies = {
            "saadparwaiz1/cmp_luasnip",
            "rafamadriz/friendly-snippets",  -- Adds a number of user-friendly snippets
        },
    },

    {
        -- Autocompletion
        "hrsh7th/nvim-cmp",
        config = function()

            -- local has_words_before = function()
            --     unpack = unpack or table.unpack
            --     local line, col = unpack(vim.api.nvim_win_get_cursor(0))
            --     return col ~= 0 and vim.api.nvim_buf_get_lines(0, line - 1, line, true)[1]:sub(col, col):match("%s") == nil
            -- end

            local cmp = require("cmp")
            local luasnip = require("luasnip")

            require("luasnip.loaders.from_vscode").lazy_load()

            cmp.setup({
                snippet = {
                expand = function(args)
                    require("luasnip").lsp_expand(args.body)
                end,
                },
                window = {
                    completion = cmp.config.window.bordered(),
                    documentation = cmp.config.window.bordered(),
                },
                mapping = cmp.mapping.preset.insert({
                    ['<C-n>'] = cmp.mapping.select_next_item(),
                    ['<C-p>'] = cmp.mapping.select_prev_item(),
                    ["<C-b>"] = cmp.mapping.scroll_docs(-4),
                    ["<C-f>"] = cmp.mapping.scroll_docs(4),
                    ["<C-Space>"] = cmp.mapping.complete(),
                    ["<C-e>"] = cmp.mapping.abort(),
                    --["<CR>"] = cmp.mapping.confirm({ select = true }),
                    -- ['<CR>'] = cmp.mapping.confirm {
                    --     behavior = cmp.ConfirmBehavior.Replace,
                    --     select = true,
                    --     },            
                    ['<CR>'] = cmp.mapping(function(fallback)
                            if cmp.visible() then
                                if luasnip.expandable() then
                                    luasnip.expand()
                                else
                                    cmp.confirm({
                                        select = true,
                                    })
                                end
                            else
                                fallback()
                            end
                        end),

                        ["<Tab>"] = cmp.mapping(function(fallback)
                        if cmp.visible() then
                            cmp.select_next_item()
                        elseif luasnip.locally_jumpable(1) then
                            luasnip.jump(1)
                        else
                            fallback()
                        end
                        end, { "i", "s" }),

                        ["<S-Tab>"] = cmp.mapping(function(fallback)
                        if cmp.visible() then
                            cmp.select_prev_item()
                        elseif luasnip.locally_jumpable(-1) then
                            luasnip.jump(-1)
                        else
                            fallback()
                        end
                        end, { "i", "s" }),
                                        }),
                                    sources = cmp.config.sources({
                                        { name = "nvim_lsp" },
                                        { name = "luasnip" }, -- For luasnip users.
                                    }, {
                                        { name = "buffer" },
                                    }),
                                })
                            end,
  },
}