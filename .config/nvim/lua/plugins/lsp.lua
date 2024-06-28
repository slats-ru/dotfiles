return { 
  {
    -- LSP Configuration & Plugins
    'neovim/nvim-lspconfig',
    dependencies = {
      'williamboman/mason.nvim',
      'williamboman/mason-lspconfig.nvim',
      'WhoIsSethDaniel/mason-tool-installer.nvim',
      { 'j-hui/fidget.nvim', opts = {} },
    },
    config = function()
      vim.api.nvim_create_autocmd('LspAttach', {
        group = vim.api.nvim_create_augroup('kickstart-lsp-attach', { clear = true }),
        callback = function(event)
          local map = function(keys, func, desc)
            vim.keymap.set('n', keys, func, { buffer = event.buf, desc = 'LSP: ' .. desc })
          end
          map('<leader>cr', vim.lsp.buf.rename, '([C]ode) [R]ename object')
          map('<leader>ca', vim.lsp.buf.code_action, '[C]ode [A]ction')
          map('K', vim.lsp.buf.hover, 'Hover Documentation')
          map('gD', vim.lsp.buf.declaration, '[G]oto [D]eclaration')
          map('gd', vim.lsp.buf.definition, '[G]oto [D]efinition')
          map('gi', vim.lsp.buf.implementation, '[G]oto [I]mplementation')
          map('<C-k>', vim.lsp.buf.signature_help, 'signature_help')
          map('<space>wa', vim.lsp.buf.add_workspace_folder, '[A]dd [W]orkspace Folder')
          map('<space>wr', vim.lsp.buf.remove_workspace_folder, '[R]emove [W]orkspace Folder')
          map('<space>D', vim.lsp.buf.declaration, 'Type [D]efinition')
          map('gr', vim.lsp.buf.references, '[G]oto [R]eferences')
          vim.keymap.set('n', '<space>wl', function()
            print(vim.inspect(vim.lsp.buf.list_workspace_folders()))
          end, { desc = "[L]ist [W]orkspace Folders" }, bufopts)        
          local client = vim.lsp.get_client_by_id(event.data.client_id)
          if client and client.server_capabilities.documentHighlightProvider then
            vim.api.nvim_create_autocmd({ 'CursorHold', 'CursorHoldI' }, {
              buffer = event.buf,
              callback = vim.lsp.buf.document_highlight,
            })
 
            vim.api.nvim_create_autocmd({ 'CursorMoved', 'CursorMovedI' }, {
              buffer = event.buf,
              callback = vim.lsp.buf.clear_references,
            })
          end
        end,
      })
      local capabilities = vim.lsp.protocol.make_client_capabilities()
      capabilities = vim.tbl_deep_extend('force', capabilities, require('cmp_nvim_lsp').default_capabilities())
      
      local servers = {
        basedpyright = {
         typeCheckingMode = "standard",
         capabilities = capabilities,
        },
        --ruff_lsp = {},
        ruff = {capabilities = capabilities,},
        --pylyzer,
        lua_ls = {
          settings = {
            Lua = {
              completion = {
                callSnippet = 'Replace',
              },
            },
          },
        },
      }
      require('mason').setup()
 
      local ensure_installed = vim.tbl_keys(servers or {})
      vim.list_extend(ensure_installed, {
        'basedpyright',
        'lua_ls',
        --'ruff-lsp',
        --'mypy',
        --'pylyzer',
        'ruff'
      })
      require('mason-tool-installer').setup { ensure_installed = ensure_installed }
 
      require('mason-lspconfig').setup {
        handlers = {
          function(server_name)
            local server = servers[server_name] or {}
            server.capabilities = vim.tbl_deep_extend('force', {}, capabilities, server.capabilities or {})
            require('lspconfig')[server_name].setup(server)
          end,
        },
      }
    end,
  },

  -- {
  --   -- provide a way for non-LSP sources to hook into NeoVim's LSP client
  --   "nvimtools/none-ls.nvim",
  --   dependencies = { "mason.nvim" },
  --   opts = function(_, opts)
  --     local nls = require("null-ls")
  --     opts.root_dir = opts.root_dir
  --       or require("null-ls.utils").root_pattern(".null-ls-root", ".neoconf.json", "Makefile", ".git")
  --     opts.sources = vim.list_extend(opts.sources or {}, {
  --       nls.builtins.diagnostics.mypy,
  --     })
  --   end,
  -- }
}