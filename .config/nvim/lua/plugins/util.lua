return {
  "ahmedkhalf/project.nvim",
  opts = {
    manual_mode = false,
  },
  event = "VeryLazy",
  config = function(_, opts)
    require("project_nvim").setup(opts)
    require('telescope').load_extension('projects')
    --require'telescope'.extensions.projects.projects{}
  end,
}