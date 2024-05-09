return {
  -- Automatically install LSPs to stdpath for neovim
  "williamboman/mason.nvim",
  config = true,
  cmd = "Mason",
  keys = { { "<leader>cm", "<cmd>Mason<cr>", desc = "Mason" } },
  build = ":MasonUpdate",
  opts = {
    ensure_installed = {
      "pyright",
      "ruff-lsp",
      -- "flake8",
    },
  },
}