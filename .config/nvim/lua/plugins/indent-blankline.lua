return {
    -- Add indentation guides even on blank lines
    "lukas-reineke/indent-blankline.nvim", 
    main = "ibl", 
    opts = { 
        indent = {
            char = "│",
            tab_char = "│",
        },
    scope = { enabled = false } }
}