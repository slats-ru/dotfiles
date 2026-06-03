import re
import socket
import subprocess

from libqtile import bar, hook, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from modules import openmeteo
from modules.colors import colors
from modules.kbswitch import MyKeyboardLayout
from qtile_extras import widget
from qtile_extras.widget import modify
from qtile_extras.widget.decorations import RectDecoration

##########################
####### Variables ########
##########################

mod = "mod4"
terminal = "kitty"
host = socket.gethostname()
wmname = "QTile"
thunar_path = (
    "/home/slats/Downloads" if host == "thinkpad-x1-carbon" else "/mnt/data/Downloads/"
)


##########################
###### Keybindings #######
##########################


def rofi_power_menu(qtile):
    qtile.spawn("""
                    rofi -show menu 
                    -modi menu:'rofi-power-menu 
                    --choices=shutdown/reboot/suspend/logout 
                    --symbols-font "Symbols Nerd Font Mono"' 
                    -font "JetBrains Mono NF 12" 
                    -theme-str 'window {width: 12em;} listview {lines: 4;}'
                    """)


MyKeyboardLayout = modify(MyKeyboardLayout, initialise=False)


keys = [
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
    Key([mod, "control"], "d", lazy.layout.shrink(), desc="Shrink window (monadtall)"),
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
    Key([mod], "p", lazy.function(rofi_power_menu), desc="Poweroff"),
    # Applications launcher
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch Rofi launcher"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "t", lazy.spawn(f"thunar {thunar_path}"), desc="Thunar"),
    Key([mod], "o", lazy.spawn("obsidian"), desc="Obsidian"),
    # Key([mod], "v", lazy.spawn("code"), desc="VS Code"),
    Key(
        [mod],
        "b",
        lazy.spawn("brave --proxy-server='socks5://localhost:12334'"),
        desc="Brave",
    ),
    Key([mod], "m", lazy.spawn("virt-manager"), desc="VirtManager"),
    # Brightness
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.widget["brightnesscontrol"].brightness_up(),
        desc="Increses brightness",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.widget["brightnesscontrol"].brightness_down(),
        desc="Decreases brightness",
    ),
    # Volume
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


########################
######## Groups ########
########################

groups = [
    Group("1", label="", layout="columns"),
    Group(
        "2",
        label="",
        layout="monadtall",
        matches=[Match(wm_class=re.compile(r"^(brave\-browser|Brave\-browser)$"))],
    ),
    Group(
        "3",
        label="",
        layout="columns",
        matches=[Match(wm_class=re.compile(r"^(code|Code|virt\-manager)$"))],
    ),
    Group(
        "4",
        label="",
        layout="columns",
        matches=[Match(wm_class=re.compile(r"^(thunar)$"))],
    ),
    Group(
        "5",
        label="󰈚",
        layout="columns",
        matches=[
            Match(
                wm_class=re.compile(r"^(xreader|com\.github\.johnfactotum\.Foliate)$")
            )
        ],
    ),
    Group(
        "6",
        label="󰜫",
        layout="monadtall",
        matches=[Match(wm_class=re.compile(r"^(obsidian)$"))],
    ),
    Group(
        "7",
        label="󰒓",
        layout="columns",
        matches=[Match(wm_class=re.compile(r"^(transmission\-gtk)$"))],
    ),
    Group("8", label="", layout="columns"),
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


#########################
######## Layouts ########
#########################

layout_theme = {
    "border_width": 2,
    "margin": 5,
    "border_focus": colors[17],
    "border_normal": colors[21],
}

layouts = [
    # layout.Max(),
    layout.Columns(
        border_width=2,
        margin=[4, 3, 2, 3],
        margin_on_single=5,
        border_focus=colors[13],
        border_normal=colors[21],
        border_focus_stack=colors[3],
        border_normal_stack=colors[14],
        border_on_single=True,
    ),
    layout.Floating(**layout_theme),
    layout.MonadTall(ratio=0.7, **layout_theme),
]


#############################
#### Widgets decorations ####
#############################

rect = {
    "decorations": [
        RectDecoration(use_widget_background=True, padding=4, filled=True),
    ]
}

rect_spacer = {
    "decorations": [
        RectDecoration(use_widget_background=True, padding=6, filled=True),
    ]
}

rect_groupbox = {
    "decorations": [
        RectDecoration(
            use_widget_background=True,
            padding_x=0,
            padding_y=4,
            filled=True,
            extrawidth=2,
        ),
    ]
}

rect_group = {
    "decorations": [
        RectDecoration(
            use_widget_background=True,
            padding=4,
            filled=True,
            group=True,
        ),
    ]
}

rect_extra = {
    "decorations": [
        RectDecoration(
            use_widget_background=True, padding=4, filled=True, extrawidth=4
        ),
    ]
}

rect_alsa = {
    "decorations": [
        RectDecoration(
            use_widget_background=True,
            padding=4,
            filled=True,
            clip=True,
            extrawidth=3,
        ),
    ]
}


#################################
######## Widget defaults ########
#################################

widget_defaults = dict(
    font="JetBrainsMono NF SemiBold",
    background=colors[22],
    fontsize=14,
    padding=4,
)
extension_defaults = widget_defaults.copy()


#########################
######## Widgets ########
#########################

current_layout = widget.CurrentLayoutIcon(
    use_mask=True,
    foreground=colors[14],
    scale=0.5,
)
groupbox = widget.GroupBox(
    background=colors[19],
    foreground=colors[22],
    this_current_screen_border=colors[3],
    active=colors[15],
    inactive=colors[22],
    borderwidth=2,
    highlight_method="text",
    highlight_color=colors[1],
    font="JetBrainsMono NFM",
    fontsize=25,
    padding_x=2,
    padding_y=1,
    rounded=False,
    center_aligned=True,
    disable_drag=True,
    urgent_alert_method="block",
    urgent_border=colors[4],
    **rect_groupbox,
)
textbox = widget.TextBox(
    text="  ",
    foreground=colors[22],
    background=colors[16],
    font="IBM Plex Sans SmBld",
    fontsize=16,
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
    **rect_extra,
)
mpris = widget.Mpris2(
    font="JetBrainsMono NF",
    fontsize=14,
    foreground=colors[14],
    format="{xesam:title} - {xesam:artist}",
    paused_text="{track}",
    playing_text="  {track}",
    max_chars=45,
)
clock_date = widget.Clock(
    format="%a %d %b",
    fmt="   {} ",
    font="IBM Plex Sans SmBld",
    fontsize=16,
    mouse_callbacks={"Button1": lambda: qtile.spawn("gsimplecal")},
    foreground=colors[14],
)
clock_time = widget.Clock(
    format="%H:%M",
    fmt=" 󰀠   {} ",
    foreground=colors[14],
    font="IBM Plex Sans SmBld",
    fontsize=16,
)
weather = openmeteo.OpenMeteo(
    fontsize=16,
    foreground=colors[14],
    font="IBM Plex Sans SmBld",
    tooltip_fontsize=14,
    tooltip_color=colors[14],
    tooltip_background=colors[20],
    update_interval=600,
    language="ru",
    popup_show_args={"relative_to": 2, "relative_to_bar": True},
)
widgetbox = widget.WidgetBox(
    text_open="  ",
    text_closed="   ",
    foreground=colors[22],
    background=colors[3],
    fontsize=15,
    font="Hack Nerd Font Bold",
    widgets=[
        widget.Memory(
            format="{MemUsed: .1f}{mm}",
            foreground=colors[22],
            background=colors[3],
            fontsize=15,
            mouse_callbacks={"Button1": lambda: qtile.spawn(terminal + " -e htop")},
            measure_mem="G",
            **rect_group,
        ),
        widget.CPU(
            format="  {load_percent}%",
            foreground=colors[22],
            background=colors[3],
            fontsize=15,
            mouse_callbacks={"Button1": lambda: qtile.spawn(terminal + " -e htop")},
            **rect_group,
        ),
        widget.ThermalSensor(
            format="  {temp:.1f}{unit} ",
            foreground=colors[22],
            background=colors[3],
            fontsize=15,
            threshold=60,
            **rect_group,
        ),
    ],
    **rect_group,
)
check_updates = widget.CheckUpdates(
    update_interval=600,
    distro="Arch_checkupdates",
    display_format=" 󰮯 {updates} ",
    no_update_string=" 󰮯 0 ",
    background=colors[12],
    colour_have_updates=colors[22],
    colour_no_updates=colors[22],
    execute=terminal + " -e paru -Syu",
    font="Hack Nerd Font Bold",
    fontsize=15,
    **rect,
)
battery_icon = widget.UPowerWidget(
    fill_critical=colors[4],
    fill_low=colors[6],
    fill_normal=colors[8],
    fill_charge=colors[12],
    border_critical_colour=colors[4],
    border_colour=colors[22],
    border_charge_colour=colors[22],
    background=colors[13],
    foreground=colors[22],
    margin=1,
    percentage_low=0.3,
    battery_name="BAT0",
    **rect_group,
)
battery_text = widget.Battery(
    format="{percent:2.0%} ",
    notify_below=15,
    update_interval=60,
    font="Hack Nerd Font Bold",
    fontsize=15,
    notification_timeout=0,
    background=colors[13],
    foreground=colors[22],
    low_percentage=0.11,
    low_foreground=colors[4],
    **rect_group,
)
brightness_ctl = widget.BrightnessControl(
    bar_colour=colors[11],
    bar_background=colors[19],
    bar_height=24,
    bar_width=60,
    bar_text_font="IBM Plex Sans SmBld",
    bar_text_fontsize=14,
    bar_text_foreground=colors[22],
)
volume_ctl = widget.ALSAWidget(
    mode="both",
    theme_path="/home/slats/.config/qtile/resources/icons/svg/light/",
    icon_size=30,
    bar_width=60,
    bar_height=24,
    bar_text_font="IBM Plex Sans SmBld",
    bar_text_fontsize=14,
    bar_text_foreground=colors[22],
    bar_colour_high=colors[7],
    bar_colour_loud=colors[4],
    bar_colour_normal=colors[8],
    bar_colour_mute=colors[13],
    bar_background=colors[19],
    limit_normal=50,
    limit_high=90,
    text_format="{volume}%",
)
wifi_icon = widget.WiFiIcon(
    active_colour=colors[14],
    inactive_colour=colors[20],
    disconnected_colour=colors[23],
    expanded_timeout=3,
    foreground=colors[14],
    padding_y=9,
    padding_x=3,
    mouse_callbacks={"Button3": lazy.spawn("networkmanager_dmenu")},
)
keyboard_layout = MyKeyboardLayout(
    text="UNK",
    update_interval=0.1,
    foreground=colors[14],
    font="Hack Nerd Font Bold",
    fontsize=15,
)
systray_1 = widget.Systray()
systray_2 = widget.StatusNotifier()
cat = widget.Image(
    background=colors[13],
    margin_x=4,
    filename="/home/slats/.config/qtile/resources/icons/svg/dark/cat.svg",
    **rect,
)

#########################
######## Spacers ########
#########################

spacer_3 = widget.Spacer(length=3)
spacer_5 = widget.Spacer(length=5)
spacer_stretch = widget.Spacer(length=bar.STRETCH)
spacer_line = widget.Spacer(
    background=colors[14],
    length=2,
    **rect_spacer,
)
spacer_battery = widget.Spacer(
    length=11,
    background=colors[13],
    **rect_group,
)

########################
##### Widgets list #####
########################

normal_widgets_1 = [
    spacer_3,
    current_layout,
    spacer_5,
    groupbox,
    spacer_5,
    textbox,
    spacer_3,
    mpris,
    spacer_stretch,
    clock_date,
    spacer_line,
    clock_time,
    spacer_line,
    weather,
    spacer_stretch,
    widgetbox,
    spacer_3,
    check_updates,
    spacer_3,
]
battery_widgets = [
    spacer_battery,
    battery_icon,
    battery_text,
]
normal_widgets_2 = [
    brightness_ctl,
    volume_ctl,
    wifi_icon,
    keyboard_layout,
    systray_1,
    systray_2,
    spacer_5,
]

widgets_list = (
    normal_widgets_1
    + (battery_widgets if host == "thinkpad-x1-carbon" else [cat])
    + normal_widgets_2
)


#########################
######## Screens ########
#########################

screens = [
    Screen(
        top=bar.Bar(
            widgets=widgets_list,
            size=33,
            background=colors[22],
            opacity=1,
            margin=[5, 5, 1, 5],
        ),
    ),
]


##########################
######## Floating ########
##########################

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
    border_normal=colors[21],
    border_width=2,
)


#########################
######### Rules #########
#########################

auto_fullscreen = True
auto_minimize = True
bring_front_click = True
cursor_warp = False
floats_kept_above = True
focus_on_window_activation = "smart"
follow_mouse_focus = False

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


#########################
######### Hooks #########
#########################


@hook.subscribe.startup_once
def start_once():
    subprocess.call(["/home/slats/.config/qtile/scripts/autostart.sh"])


@hook.subscribe.client_new
def new_client(window):
    if window.match(Match(wm_class="mpv")):
        window.togroup("8", switch_group=True)
        window.toggle_fullscreen()
        # window.togroup(qtile.current_group.name)
        # window.cmd_disable_floating()
    if window.match(
        Match(wm_class=re.compile(r"^(xreader|com\.github\.johnfactotum\.Foliate)$"))
    ):
        window.togroup("5", switch_group=True)
