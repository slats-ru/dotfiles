return {
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
}