return {
  { --file manager
    "nvim-neo-tree/neo-tree.nvim",
    branch = "v3.x",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "nvim-tree/nvim-web-devicons", -- not strictly required, but recommended
      "MunifTanjim/nui.nvim",
    },
    keys = {
      {
        "<leader>fe",
        function()
          require("neo-tree.command").execute({ toggle = true, dir = "C:/Users/gorsheninaas/Documents/Python-Projects" })
        end,
        desc = "[F]ile [E]xplorer NeoTree (Python-Projects)",
      },
      {
        "<leader>ge",
        function()
          require("neo-tree.command").execute({ source = "git_status", toggle = true, position = "float" })
        end,
        desc = "[G]it [E]xplorer",
      },
      {
        "<leader>be",
        function()
          require("neo-tree.command").execute({ source = "buffers", toggle = true, position = "float" })
        end,
        desc = "[B]uffer [E]xplorer",
      },
      {
        "<leader>fc",
        function()
          require("neo-tree.command").execute({ toggle = true, dir = vim.uv.cwd() })
        end,
        desc = "Explorer NeoTree ([c]wd)",
      },
    },
    config = function()
      require('neo-tree').setup({
        window = {
          width = 25,
        },
        filesystem = {
          filtered_items = {
            hide_dotfiles = false,
            hide_gitignored = false,
            hide_hidden = false, -- only works on Windows for hidden files/directories
          },
          follow_current_file = {
            leave_dirs_open = true, -- `false` closes auto expanded dirs, such as with `:Neotree reveal`
          },
        },
      })
      vim.cmd([[nnoremap \ :Neotree reveal<cr>]])
    end,
  },

  {
    -- edit your filesystem like a normal Neovim buffer
    'stevearc/oil.nvim',
    opts = {},
    -- Optional dependencies
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("oil").setup({
        columns = {
          "icon",
          "type",
          "size",
        },
        delete_to_trash = true,
        skip_confirm_for_simple_edits = true,
        use_default_keymaps = true,
        view_options = {
          show_hidden = false,
          is_hidden_file = function(name, bufnr)
            return vim.startswith(name, ".")
          end,
          sort = {
            { "type", "asc" },
            { "name", "asc" },
          },
        },
      })
      vim.keymap.set("n", "-", "<CMD>Oil<CR>", { desc = "Open parent directory" })
    end,
  },

  {
    -- displays a popup with possible key bindings of the command you started typing
    "folke/which-key.nvim",
    event = "VeryLazy",
    opts = {
      plugins = { spelling = true },
      defaults = {
        mode = { "n", "v" },
        ["g"] = { name = "+goto" },
        ["gs"] = { name = "+surround" },
        ["z"] = { name = "+fold" },
        ["]"] = { name = "+next" },
        ["["] = { name = "+prev" },
        ["<leader><tab>"] = { name = "+tabs" },
        ["<leader>b"] = { name = "+buffer" },
        ["<leader>c"] = { name = "+code" },
        ["<leader>d"] = { name = "+debug" },
        ["<leader>f"] = { name = "+file/find" },
        ["<leader>g"] = { name = "+git" },
        ["<leader>h"] = { name = "+hunks" },
        ["<leader>q"] = { name = "+quit/session" },
        ["<leader>s"] = { name = "+search" },
        ["<leader>t"] = { name = "+tests" },
        ["<leader>u"] = { name = "+ui" },
        ["<leader>w"] = { name = "+workspaces" },
        ["<leader>x"] = { name = "+diagnostics/quickfix" },
      },
    },
    config = function(_, opts)
      local wk = require("which-key")
      wk.setup(opts)
      wk.register(opts.defaults)
    end,
  },

  {
    -- Fuzzy Finder (files, lsp, etc)
    'nvim-telescope/telescope.nvim',
    branch = '0.1.x',
    dependencies = { 'nvim-lua/plenary.nvim' },
    config = function()
      require('telescope').setup {
        defaults = {
          mappings = {
            i = {
              ['<C-u>'] = false,
              ['<C-d>'] = false,
            },
          },
        },
        extensions = {
          fzf = {
            fuzzy = true,                   -- false will only do exact matching
            override_generic_sorter = true, -- override the generic sorter
            override_file_sorter = true,    -- override the file sorter
            case_mode = "smart_case",       -- or "ignore_case" or "respect_case", the default case_mode is "smart_case"
          },
          ["ui-select"] = {
            require("telescope.themes").get_dropdown {}
          }
        }
      }

      -- To get fzf loaded and working with telescope, you need to call
      -- load_extension, somewhere after setup function:
      --require('telescope').load_extension('fzf')

      -- Enable telescope fzf native, if installed
      pcall(require('telescope').load_extension, 'fzf')

      -- To get ui-select loaded and working with telescope, you need to call
      -- load_extension, somewhere after setup function:
      require("telescope").load_extension("ui-select")

      vim.keymap.set('n', '<leader>gf', require('telescope.builtin').git_files, { desc = 'Search [G]it [F]iles' })
      vim.keymap.set('n', '<leader>sf', require('telescope.builtin').find_files, { desc = '[S]earch [F]iles' })
      vim.keymap.set('n', '<leader>sh', require('telescope.builtin').help_tags, { desc = '[S]earch [H]elp' })
      vim.keymap.set('n', '<leader>sw', require('telescope.builtin').grep_string, { desc = '[S]earch current [W]ord' })
      vim.keymap.set('n', '<leader>sg', require('telescope.builtin').live_grep, { desc = '[S]earch by [G]rep' })
      vim.keymap.set('n', '<leader>sd', require('telescope.builtin').diagnostics, { desc = '[S]earch [D]iagnostics' })
      vim.keymap.set('n', '<leader>?', require('telescope.builtin').oldfiles, { desc = '[?] Find recently opened files' })
      vim.keymap.set('n', '<leader><space>', require('telescope.builtin').buffers, { desc = '[ ] Find existing buffers' })
      vim.keymap.set('n', '<leader>/', function()
        -- You can pass additional configuration to telescope to change theme, layout, etc.
        require('telescope.builtin').current_buffer_fuzzy_find(require('telescope.themes').get_dropdown {
          winblend = 10,
          previewer = false,
        })
      end, { desc = '[/] Fuzzily search in current buffer' })

      -- LSP Keymaps
      --vim.keymap.set('n', 'gd', require('telescope.builtin').lsp_definitions, { desc = '[G]oto [D]efinition' })
      --vim.keymap.set('n', 'gr', require('telescope.builtin').lsp_references, { desc = '[G]oto [R]eferences' })
      --vim.keymap.set('n', 'gI', require('telescope.builtin').lsp_implementations, { desc = '[G]oto [I]mplementation' })
      --vim.keymap.set('n', '<leader>D', require('telescope.builtin').lsp_type_definitions, { desc = 'Type [D]efinition' })
      vim.keymap.set('n', '<leader>cs', require('telescope.builtin').lsp_document_symbols,
        { desc = 'LSP: ([C]ode) Document [S]ymbols' })
      vim.keymap.set('n', '<leader>ws', require('telescope.builtin').lsp_dynamic_workspace_symbols,
        { desc = '[W]orkspace [S]ymbols' })
    end
  },

  {
    -- Fuzzy Finder Algorithm
    'nvim-telescope/telescope-fzf-native.nvim',
    build = 'make',
    cond = function()
      return vim.fn.executable 'make' == 1
    end
  },

  {
    -- sets vim.ui.select to telescope
    'nvim-telescope/telescope-ui-select.nvim',
  },

  {
    -- Adds git releated signs to the gutter, as well as utilities for managing changes
    'lewis6991/gitsigns.nvim',
    opts = {
      signs = {
        add = { text = '+' },
        change = { text = '~' },
        delete = { text = '_' },
        topdelete = { text = '‾' },
        changedelete = { text = '~' },
      },
      on_attach = function(buffer)
        local gitsigns = require('gitsigns')

        local function map(mode, l, r, opts)
          opts = opts or {}
          opts.buffer = bufnr
          vim.keymap.set(mode, l, r, opts)
        end

        -- Navigation
        map('n', ']c', function()
            if vim.wo.diff then
              vim.cmd.normal({ ']c', bang = true })
            else
              gitsigns.nav_hunk('next')
            end
          end,
          { desc = 'Next Hunk' })

        map('n', '[c', function()
            if vim.wo.diff then
              vim.cmd.normal({ '[c', bang = true })
            else
              gitsigns.nav_hunk('prev')
            end
          end,
          { desc = 'Prev Hunk' })

        -- Actions
        map('n', '<leader>hs', gitsigns.stage_hunk, { desc = '[S]tage [H]unk' })
        map('n', '<leader>hr', gitsigns.reset_hunk, { desc = '[R]eset [H]unk' })
        map('v', '<leader>hs', function() gitsigns.stage_hunk { vim.fn.line('.'), vim.fn.line('v') } end)
        map('v', '<leader>hr', function() gitsigns.reset_hunk { vim.fn.line('.'), vim.fn.line('v') } end)
        map('n', '<leader>hS', gitsigns.stage_buffer, { desc = '[S]tage Buffer' })
        map('n', '<leader>hu', gitsigns.undo_stage_hunk, { desc = '[U]ndo stage [H]unk' })
        map('n', '<leader>hR', gitsigns.reset_buffer, { desc = '[R]eset Buffer' })
        map('n', '<leader>hp', gitsigns.preview_hunk, { desc = '[P]review [H]unk' })
      end,
    },
  },

  {
    "hedyhli/outline.nvim",
    lazy = true,
    cmd = { "Outline", "OutlineOpen" },
    keys = { -- Example mapping to toggle outline
      { "<leader>o", "<cmd>Outline<CR>", desc = "Toggle outline" },
    },
    opts = {
      outline_window = {
        position = 'left',
        relative_width = false,
      }, 
    },
  },

  {
    -- persist and toggle multiple terminals
    {
      'akinsho/toggleterm.nvim', 
      version = "*", 
      opts = {
        open_mapping = [[<leader>T]]
      }
    }
  },
}
