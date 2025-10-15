import os
import subprocess

import owm
from libqtile import bar, hook, layout, qtile
from libqtile import widget as old_widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

#  from libqtile.utils import send_notification
from qtile_extras import widget
from qtile_extras.widget import modify
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration

mod = "mod4"
terminal = "kitty"


def rofi_power_menu(qtile):
    qtile.cmd_spawn("""
                    rofi -show menu 
                    -modi menu:'rofi-power-menu 
                    --choices=shutdown/reboot/suspend/logout 
                    --symbols-font "Symbols Nerd Font Mono"' 
                    -font "JetBrains Mono NF 12" 
                    -theme-str 'window {width: 12em;} listview {lines: 4;}'
                    """)


class MyKeyboardLayout(old_widget.base.ThreadPoolText):
    def __init__(self, **config):
        super().__init__(**config)
        self.add_callbacks({"Button1": self.next_keyboard})

    def poll(self):
        return subprocess.check_output("xkb-switch").decode().strip()[:2].upper()

    def next_keyboard(self):
        subprocess.run(["xkb-switch", "-n"])
        self.tick()


MyKeyboardLayout = modify(MyKeyboardLayout, initialise=False)


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "i", lazy.layout.grow(), desc="Expand window (monadtall)"),
    Key([mod, "control"], "d", lazy.layout.shrink(), desc="Shrink window (monadtal)"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key(
        [mod, "control"],
        "w",
        lazy.layout.reset(),
        desc="Reset all window sizes (monadtall)",
    ),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key(
        [mod, "shift", "control"],
        "h",
        lazy.layout.swap_column_left(),
        desc="Swap column left",
    ),
    Key(
        [mod, "shift", "control"],
        "l",
        lazy.layout.swap_column_right(),
        desc="Swap column right",
    ),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    # Essentials
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "p", lazy.function(rofi_power_menu), desc="Poweroff"),
    # Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),
    # Applications launcher
    # Key([mod], "s", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch Rofi launcher"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key(
        [mod],
        "b",
        lazy.spawn("brave --proxy-server='socks5://localhost:12334'"),
        desc="Brave",
    ),
    Key(
        [mod],
        "g",
        lazy.spawn("google-chrome-stable --proxy-server='socks5://localhost:12334'"),
        desc="Google Chrome",
    ),
    Key([mod], "t", lazy.spawn("thunar /home/slats/Downloads"), desc="Thunar"),
    Key([mod], "o", lazy.spawn("obsidian"), desc="Obsidian"),
    # Key([mod], "v", lazy.spawn("code"), desc="VS Code"),
    # Key([mod], "y", lazy.spawn(terminal + " -e yazi"), desc="Yazi"),
    Key([mod], "c", lazy.spawn(terminal + " -e cmus"), desc="Cmus"),
    # Brightness
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl set +5%"),
        desc="Increses brightness",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl set 5%-"),
        desc="Decreases brightness",
    ),
    # Volume
    # Key([], "XF86AudioRaiseVolume", lazy.widget["volume"].increase_vol(), desc="Increases volume"),
    # Key([], "XF86AudioLowerVolume", lazy.widget["volume"].decrease_vol(), desc="Decreases volume"),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"),
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"),
    ),
    Key([], "XF86AudioMute", lazy.spawn("amixer -c 0 -q set Master toggle")),
    Key(
        [mod],
        "s",
        lazy.spawn("/home/slats/.config/qtile/scripts/maim-desktop.sh", shell=True),
    ),
]

groups = [
    Group("1", label="", layout="columns"),
    Group(
        "2",
        label="",
        layout="max",
        matches=[
            Match(
                wm_class=[
                    "google-chrome",
                    "Google-chrome",
                    "Brave-browser",
                    "brave-browser",
                ]
            )
        ],
    ),
    Group("3", label="", layout="max", matches=[Match(wm_class=["code", "Code"])]),
    Group("4", label="", layout="columns", matches=[Match(wm_class=["thunar"])]),
    Group(
        "5",
        label="󰈚",
        layout="columns",
        matches=[Match(wm_class=["xreader", "com.github.johnfactotum.Foliate"])],
    ),
    Group("6", label="󰜫", layout="max", matches=[Match(wm_class=["obsidian"])]),
    Group(
        "7",
        label="󰒓",
        layout="columns",
        matches=[Match(wm_class=["transmission-gtk"])],
    ),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

colors_nord = [
    ["#2E3440"],  # 0 polar_night_1
    ["#3B4252"],  # 1 polar_night_2
    ["#434C5E"],  # 2 polar_night_3
    ["#4C566A"],  # 3 polar_night_4
    ["#D8DEE9"],  # 4 snow_storm_1
    ["#E5E9F0"],  # 5 snow_storm_2
    ["#ECEFF4"],  # 6 snow_storm_3
    ["#8FBCBB"],  # 7 frost_1
    ["#88C0D0"],  # 8 frost_2
    ["#81A1C1"],  # 9 frost_3
    ["#5E81AC"],  # 10 frost_4
    ["#BF616A"],  # 11 aurora_red
    ["#D08770"],  # 12 aurora_orange
    ["#EBCB8B"],  # 13 aurora_yellow
    ["#A3BE8C"],  # 14 aurora_green
    ["#B48EAD"],
]  # 15 aurora_magenta

colors = [
    ["#f2d5cf"],  # 0 rosewater
    ["#eebebe"],  # 1 flamingo
    ["#f4b8e4"],  # 2 pink
    ["#ca9ee6"],  # 3 mauve
    ["#e78284"],  # 4 red
    ["#ea999c"],  # 5 maroon
    ["#ef9f76"],  # 6 peach
    ["#e5c890"],  # 7 yellow
    ["#a6d189"],  # 8 green
    ["#81c8be"],  # 9 teal
    ["#99d1db"],  # 10 sky
    ["#85c1dc"],  # 11 sapphire
    ["#8caaee"],  # 12 blue
    ["#babbf1"],  # 13 lavender
    ["#c6d0f5"],  # 14 text
    ["#b5bfe2"],  # 15 subtext1
    ["#a5adce"],  # 16 subtext0
    ["#949cbb"],  # 17 overlay2
    ["#838ba7"],  # 18 overlay1
    ["#737994"],  # 19 overlay0
    ["#626880"],  # 20 surface2
    ["#51576d"],  # 21 surface1
    ["#414559"],  # 22 surface0
    ["#303446"],  # 23 base
    ["#292c3c"],  # 24 mantle
    ["#232634"],
]  # 25 crust

layout_theme = {
    "border_width": 2,
    "margin": 5,
    "border_focus": colors[17],
    "border_normal": colors[21],
}

layouts = [
    layout.Max(),
    # layout.MonadTall(**layout_theme),
    layout.Columns(
        border_width=2,
        margin=[4, 3, 2, 3],
        margin_on_single=5,
        border_focus=colors[17],
        border_normal=colors[21],
        border_focus_stack=colors[3],
        border_normal_stack=colors[14],
        border_on_single=True,
    ),
    layout.Floating(**layout_theme),
    # layout.TreeTab(border_width = 2, bg_color = colors[1], active_bg = colors[9], inactive_bg = colors[3], panel_width = 200),
    # layout.MonadThreeCol(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Stack(num_stacks=2),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    # layout.Slice(),
    # layout.Spiral(),
]

powerline = {
    "decorations": [
        # RectDecoration(use_widget_background=True, padding_y=5, filled=True, radius=0),
        PowerLineDecoration(path="forward_slash")
    ]
}

widget_defaults = dict(
    # font = "Hack Nerd Font Bold",
    font="JetBrainsMono NF Semibold",
    fontsize=14,
    padding=2,
    background=colors[22],
    foreground=colors[14],
)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(
                    scale=0.6,
                    background=colors[25],
                ),
                widget.Spacer(
                    background=colors[25],
                    length=1,
                    **powerline,
                ),
                widget.GroupBox(
                    background=colors[23],
                    this_current_screen_border=colors[12],
                    active=colors[13],
                    inactive=colors[19],
                    borderwidth=2,
                    highlight_method="text",
                    highlight_color=colors[1],
                    font="JetBrainsMono NFM",
                    fontsize=22,
                    padding_x=2,
                    padding_y=1,
                    rounded=False,
                    center_aligned=True,
                    disable_drag=True,
                    urgent_alert_method="block",
                    urgent_border=colors[4],
                    **powerline,
                ),
                widget.TextBox(
                    text="",
                    font="Hack Nerd Font Bold",
                    mouse_callbacks={
                        "Button1": lazy.spawn(
                            "/home/slats/.config/qtile/scripts/maim-desktop.sh",
                            shell=True,
                        ),
                        "Button3": lazy.spawn(
                            "/home/slats/.config/qtile/scripts/maim-select.sh",
                            shell=True,
                        ),
                        "Button2": lazy.spawn(
                            "/home/slats/.config/qtile/scripts/maim-window.sh",
                            shell=True,
                        ),
                    },
                    **powerline,
                ),
                widget.WidgetBox(
                    text_open=" ",
                    text_closed=" ",
                    widgets=[
                        widget.Memory(
                            format="{MemUsed: .1f}{mm}",
                            background=colors[22],
                            foreground=colors[14],
                            mouse_callbacks={
                                "Button1": lambda: qtile.cmd_spawn(
                                    terminal + " -e htop"
                                )
                            },
                            measure_mem="G",
                        ),
                        widget.CPU(
                            format="  {load_percent}%",
                            background=colors[22],
                            foreground=colors[14],
                            mouse_callbacks={
                                "Button1": lambda: qtile.cmd_spawn(
                                    terminal + " -e htop"
                                )
                            },
                        ),
                        widget.ThermalSensor(
                            format="  {temp:.1f}{unit}",
                            background=colors[22],
                            foreground=colors[14],
                            threshold=60,
                        ),
                    ],
                    background=colors[22],
                ),
                widget.Spacer(
                    background=colors[22],
                    length=1,
                    **powerline,
                ),
                widget.Prompt(),
                widget.Spacer(
                    length=bar.STRETCH,
                    **powerline,
                ),
                widget.Clock(
                    format="%a %d %b",
                    fmt=" {}",
                    background=colors[19],
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("gsimplecal")},
                    foreground=colors[25],
                    **powerline,
                ),
                widget.Clock(
                    format="%H:%M",
                    fmt="󰀠 {}",
                    background=colors[16],
                    foreground=colors[25],
                    **powerline,
                ),
                owm.OpenWeatherMap(
                    api_key="f009ccceabb36441891829f2962ba4ba",
                    background=colors[14],
                    foreground=colors[25],
                    latitude=59.9,
                    longitude=30.3,
                    icon_font="Weather Icons",
                    format="{icon} {temp:.1f}{temp_units}",
                    update_interval=1800,
                ),
                widget.Spacer(
                    background=colors[14],
                    length=1,
                    **powerline,
                ),
                widget.Spacer(
                    length=bar.STRETCH,
                    **powerline,
                ),
                widget.CheckUpdates(
                    update_interval=600,
                    distro="Arch_checkupdates",
                    display_format="󰮯 {updates}",
                    no_update_string="󰮯 0",
                    background=colors[12],
                    colour_have_updates=colors[22],
                    colour_no_updates=colors[22],
                    execute=terminal + " -e paru -Syu",
                    font="Hack Nerd Font Bold",
                    **powerline,
                ),
                widget.UPowerWidget(
                    fill_critical=colors[4],
                    fill_low=colors[6],
                    fill_normal=colors[8],
                    fill_charge=colors[12],
                    border_critical_colour=colors[4],
                    border_colour=colors[23],
                    border_charge_colour=colors[23],
                    background=colors[13],
                    foreground=colors[22],
                    margin=2,
                    percentage_low=0.3,
                ),
                widget.Battery(
                    format=" {percent:2.0%}",
                    notify_below=15,
                    update_interval=60,
                    font="Hack Nerd Font Bold",
                    notification_timeout=0,
                    background=colors[13],
                    foreground=colors[22],
                    low_percentage=0.11,
                    low_foreground=colors[4],
                    **powerline,
                ),
                MyKeyboardLayout(
                    text="UNK",
                    update_interval=0.1,
                    background=colors[3],
                    foreground=colors[22],
                    font="Hack Nerd Font Bold",
                    **powerline,
                ),
                widget.Wlan(
                    foreground=colors[22],
                    background=colors[12],
                    format="  {percent:2.0%}",
                    font="Hack Nerd Font Bold",
                    mouse_callbacks={"Button1": lazy.spawn("networkmanager_dmenu")},
                    update_interval=60,
                    **powerline,
                ),
                widget.Backlight(
                    fmt="󰃟 {}",
                    backlight_name="intel_backlight",
                    brightness_file="actual_brightness",
                    change_command="brightnessctl s {0}%",
                    foreground=colors[22],
                    background=colors[13],
                    step=5,
                    font="Hack Nerd Font Bold",
                    **powerline,
                ),
                widget.StatusNotifier(
                    background=colors[3],
                ),
                widget.Systray(background=colors[3]),
                widget.ALSAWidget(
                    mode="both",
                    theme_path="/home/slats/.config/qtile/icons",
                    background=colors[3],
                    foreground=colors[25],
                    bar_width=50,
                    bar_colour_high=colors[7],
                    bar_colour_loud=colors[4],
                    bar_colour_normal=colors[8],
                    bar_colour_mute=colors[13],
                    limit_normal=50,
                    limit_high=90,
                    text_format="{volume}%",
                ),
                widget.Spacer(
                    background=colors[3],
                    length=5,
                ),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="confirm"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="pavucontrol"),
        Match(wm_class="dialog"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="download"),
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    border_focus=colors[17],
    border_width=2,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "QTile"
