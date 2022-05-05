import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer

# for all qtile related stuffs
# I have mostly used this qtile variable in functions to start different programs...
from libqtile import qtile

# import arcobattery

# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser("~")


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


keys = [
    # CUSTOM KEY
    # FOR INCREASING AND DECREASING LAYOUT SIZE...
    Key(
        ["control", "shift"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        ["control", "shift"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        ["control", "shift"],
        "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        ["control", "shift"],
        "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    # FUNCTION KEYS
    Key([], "F12", lazy.spawn("xfce4-terminal --drop-down")),
    # SUPER + FUNCTION KEYS
    Key([mod], "e", lazy.spawn("pcmanfm")),
    Key([mod, "shift"], "c", lazy.spawn("code")),
    Key([mod], "c", lazy.spawn("conky-toggle")),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "m", lazy.spawn("google-chrome-stable")),
    Key([mod, "control"], "m", lazy.spawn("min")),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "r", lazy.spawn("rofi-theme-selector")),
    Key([mod], "t", lazy.spawn("urxvt")),
    Key([mod], "v", lazy.spawn("pavucontrol")),
    Key([mod], "w", lazy.spawn("vivaldi-stable")),
    Key([mod], "x", lazy.spawn("arcolinux-logout")),
    Key([mod], "Escape", lazy.spawn("xkill")),
    Key([mod, "shift"], "Return", lazy.spawn("alacritty -e zsh -c 'tmux -u'")),
    Key([mod], "Return", lazy.spawn("alacritty -e zsh")),
    Key([mod], "KP_Enter", lazy.spawn("termite")),
    Key([mod], "F1", lazy.spawn("discord")),
    Key([mod], "F2", lazy.spawn("atom")),
    Key([mod], "F3", lazy.spawn("inkscape")),
    Key([mod], "F4", lazy.spawn("gimp")),
    Key([mod], "F5", lazy.spawn("meld")),
    Key([mod], "F6", lazy.spawn("vlc --video-on-top")),
    Key([mod], "F7", lazy.spawn("virtualbox")),
    Key([mod], "F8", lazy.spawn("pcmanfm")),
    Key([mod], "F9", lazy.spawn("evolution")),
    Key([mod], "F10", lazy.spawn("spotify")),
    Key([mod], "F11", lazy.spawn("rofi -show run -fullscreen")),
    Key([mod], "F12", lazy.spawn("rofi -show run")),
    # SUPER + SHIFT KEYS
    Key([mod, mod2], "Return", lazy.spawn("thunar")),
    Key(
        [mod],
        "d",
        lazy.spawn("rofi -show run"),
    ),
    # Key(
    #    ["mod1"],
    #    "d",
    #    lazy.spawn(
    #        "dmenu_run -l 25 -i -nb '#191919' -nf '#0f60b6' -sb '#0f60b6' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=14'"
    #    ),
    # ),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "control"], "r", lazy.restart()),
    # Key([mod, "shift"], "x", lazy.shutdown()),
    # CONTROL + ALT KEYS
    Key(["mod1", "control"], "Next", lazy.spawn("conky-rotate -n")),
    Key(["mod1", "control"], "Prior", lazy.spawn("conky-rotate -p")),
    Key(["mod1", "control"], "a", lazy.spawn("xfce4-appfinder")),
    Key(["mod1", "control"], "b", lazy.spawn("thunar")),
    Key(["mod1", "control"], "c", lazy.spawn("catfish")),
    Key(["mod1", "control"], "e", lazy.spawn("arcolinux-tweak-tool")),
    Key(["mod1", "control"], "f", lazy.spawn("firefox")),
    Key(["mod1", "control"], "g", lazy.spawn("chromium -no-default-browser-check")),
    Key(["mod1", "control"], "i", lazy.spawn("nitrogen")),
    Key(["mod1", "control"], "k", lazy.spawn("arcolinux-logout")),
    Key(["mod1", "control"], "l", lazy.spawn("arcolinux-logout")),
    Key(
        ["mod1", "control"],
        "o",
        lazy.spawn(home + "/.config/qtile/scripts/picom-toggle.sh"),
    ),
    Key(["mod1", "control"], "p", lazy.spawn("pamac-manager")),
    Key(["mod1", "control"], "r", lazy.spawn("rofi-theme-selector")),
    Key(["mod1", "control"], "s", lazy.spawn("spotify")),
    Key(["mod1", "control"], "t", lazy.spawn("termite")),
    Key(["mod1", "control"], "u", lazy.spawn("pavucontrol")),
    Key(["mod1", "control"], "v", lazy.spawn("vivaldi-stable")),
    Key(["mod1", "control"], "w", lazy.spawn("arcolinux-welcome-app")),
    Key(["mod1", "control"], "Return", lazy.spawn("termite")),
    # ALT + ... KEYS
    # Key(["mod1"], "f", lazy.spawn("variety -f")),
    # Key(["mod1"], "h", lazy.spawn("urxvt -e htop")),
    # Key(["mod1"], "n", lazy.spawn("variety -n")),
    # Key(["mod1"], "p", lazy.spawn("variety -p")),
    # Key(["mod1"], "t", lazy.spawn("variety -t")),
    #    Key(["mod1"], "Up", lazy.spawn('variety --pause')),
    #    Key(["mod1"], "Down", lazy.spawn('variety --resume')),
    #    Key(["mod1"], "Left", lazy.spawn('variety -p')),
    #    Key(["mod1"], "Right", lazy.spawn('variety -n')),
    Key(["mod1"], "F2", lazy.spawn("gmrun")),
    Key(["mod1"], "F3", lazy.spawn("xfce4-appfinder")),
    # VARIETY KEYS WITH PYWAL
    Key(
        ["mod1", "shift"],
        "f",
        lazy.spawn(home + "/.config/qtile/scripts/set-pywal.sh -f"),
    ),
    Key(
        ["mod1", "shift"],
        "p",
        lazy.spawn(home + "/.config/qtile/scripts/set-pywal.sh -p"),
    ),
    Key(
        ["mod1", "shift"],
        "n",
        lazy.spawn(home + "/.config/qtile/scripts/set-pywal.sh -n"),
    ),
    Key(
        ["mod1", "shift"],
        "u",
        lazy.spawn(home + "/.config/qtile/scripts/set-pywal.sh -u"),
    ),
    # CONTROL + SHIFT KEYS
    Key([mod2, "shift"], "Escape", lazy.spawn("xfce4-taskmanager")),
    # SCREENSHOTS
    Key(
        [],
        "Print",
        lazy.spawn(
            "scrot 'ArcoLinux-%Y-%m-%d-%s_screenshot_$wx$h.jpg' -e 'mv $f $$(xdg-user-dir PICTURES)'"
        ),
    ),
    Key([mod2], "Print", lazy.spawn("xfce4-screenshooter")),
    Key([mod2, "shift"], "Print", lazy.spawn("gnome-screenshot -i")),
    # MULTIMEDIA KEYS
    # INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),
    # INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    #    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    #    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
    #    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
    #    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),
    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),
    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),
    # FLIP LAYOUT FOR BSP
    # Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    # Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    # Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    # Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    # MY CUSTOM KEY BINDINGS TO CONTROL THINGS UP
    # BRIGHTNESS CONTROL
    Key(
        [], "XF86MonBrightnessUp", lazy.spawn(f"light -A 5")
    ),  # decrease brightness by 5 levels
    Key(
        [], "XF86MonBrightnessDown", lazy.spawn(f"light -U 5")
    ),  # increase brightness by 5 levels
    # Key(["mod1"], "Right", lazy.spawn(f"light -A 5")),
]

groups = []

# WINDOW CHANGING SHORCUT KEYS BY USING "MOD + group_names[i]"
# group_names = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "8",
    "9",
    "0",
]  # reduced the size of numbers of groups
# group_labels = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
group_labels = [
    " ⦿ ",
    " ⦿ ",
    " ⦿ ",
    " ⦿ ",
    " ⦿ ",
    " ⦿ ",
    " ⦿ ",
    " ⦿ ",
    " ⦿ ",
]  # reduced the number of groups
# group_labels = ["WEB", "NVIM", "TERM", "DROID", "TEST", "MUSIZ", "FILE", "GAME", "FUN", "ETC"]
group_layouts = [
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
]
for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )


def toscreen(qtile, group_name):
    if group_name == qtile.current_screen.group.name:
        return qtile.current_screen.set_group(qtile.current_screen.previous_group)
    for i, group in enumerate(qtile.groups):
        if group_name == group.name:
            return qtile.current_screen.set_group(qtile.groups[i])


for i in groups:
    keys.extend(
        [
            # CHANGE WORKSPACES
            Key([mod], i.name, lazy.group[i.name].toscreen()),
            Key([mod], "Tab", lazy.screen.next_group()),
            Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
            # Key(["mod1"], "Tab", lazy.screen.next_group()),
            # alt + tab will shift focus of layouts... like in windows
            # and S + tab will change screens...
            Key(["mod1"], "Tab", lazy.layout.up()),
            Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                lazy.group[i.name].toscreen(),
            ),
        ]
    )

main_theme_color = "#A74D24"
main_bg_color = "#001C2D"
# here the main background color is based on the wallpaper theme or primary color
def init_color_final():
    return [
        [main_bg_color, main_bg_color],  # 0 - main background color
        ["#FFFFFF", "#FFFFFF"],  # 1 - active icon color
        [main_bg_color, main_bg_color],  # 2 - active icon background color
        ["#7F7F7F", "#7F7F7F"],  # 3 - inactive icon color
        [main_bg_color, main_bg_color],  # 4 - inactive icon background color
        ["#EFEFEF", "#EFEFEF"],  # 5 - normal text color
        ["#16222C", "#16222C"],  # 6 - 1st type background color
        [main_theme_color, main_theme_color],  # 7 - 1st type text color
        [main_bg_color, main_bg_color],  # 8 - 2nd type background color
        ["#EFEFEF", "#EFEFEF"],  # 9 - 2nd type text color
        ["#151515", "#151515"],  # 10 - opposite background
        "#892F82",  # 11 - single color
        "#0F1419",  # 12 - single color
    ]


colors = init_color_final()
# USER_NAME = "| 𝓼𝓸𝓫𝓱𝓪𝓷𝓫𝓮𝓻𝓪 | "
USER_NAME = " sobhanbera |"
currcolor = True
marginHorizontal = 20
marginHorizontalBottom = 600  # this value should not be more higher... BTW this value is according to my screen size
margin = 0

bar_size = 26
bar_opacity = 0.65
font_size = 14
default_font = "SauceCodePro Nerd Font"


def init_layout_theme(name):
    return {
        "margin": margin,
        "border_width": 0,
        "border_focus": colors[11],
        "border_normal": colors[12],
        "name": f"{name}",
        "num_stacks": 1,
    }


layouts = [
    layout.MonadTall(
        margin=margin,
        border_width=0,
        border_focus=colors[11],
        border_normal=colors[12],
        max_ratio=0.95,
        change_size=0.08,
        change_ratio=0.035,
        name="𝓽𝓪𝓵𝓵|",
        fontsize=20,
        ratio=0.5,
    ),
    layout.MonadWide(
        margin=margin,
        border_width=0,
        border_focus=colors[11],
        border_normal=colors[12],
        max_ratio=0.95,
        change_size=0.08,
        change_ratio=0.035,
        name="𝔀𝓲𝓭𝓮|",
        fontsize=20,
        new_at_current=True,
        ratio=0.5,
    ),
    layout.Bsp(**init_layout_theme("𝓫𝓼𝓹𝔀𝓷|")),
    layout.Matrix(**init_layout_theme("𝓶𝓪𝓽𝓻𝔁|")),
    layout.Floating(**init_layout_theme("𝓯𝓵𝓸𝓪𝓽|")),
    # layout.RatioTile(**init_layout_theme("𝓻𝓪𝓽𝓲𝓸|")),
    layout.Max(**init_layout_theme("𝓶𝓪𝔁𝔀𝓶 |")),
    # layout.Zoomy(**init_layout_theme("zoom|")),
    # layout.Stack(**init_layout_theme('Stack|'))
    # layout.Slice(**init_layout_theme("slice|"))
]


def launch_nvim():
    # qtile.cmd_spawn("/home/sobhanbera/Documents/Softwares/scripts/launch_nvim.sh")
    # qtile.cmd_spawn("alacritty -e zsh -c nvim")
    qtile.cmd_spawn(
        "alacritty -e /home/sobhanbera/Documents/Softwares/nvim/nvim/bin/nvim"
    )


# this function will launch htop from the mouse callback function
def launch_htop():
    qtile.cmd_spawn("alacritty -e htop")


# this function will replace the window name in the tasks list widget
def window_name_text_parser(text):
    return ""


def screenTopWidgetList():
    return [
        widget.TextBox(
            text=USER_NAME,
            foreground=colors[9],
            background=colors[8],
            padding=3,
            fontsize=font_size + 2,
            font=default_font,
            mouse_callbacks={"Button1": launch_nvim},
        ),
        widget.CurrentLayout(
            foreground=colors[5],
            background=colors[0],
            fontsize=font_size,
            font=default_font,
        ),
        # widget.TextBox(text="", foreground=colors[9], background=colors[8], padding=3, fontsize=font_size),
        widget.Net(
            foreground=colors[9],
            background=colors[8],
            fontsize=font_size,
            font=default_font,
            update_interval=5,
            format="↓{down} ↑{up}",
        ),
        widget.TaskList(
            background=colors[8],
            foreground=colors[9],
            highlight_method="border",
            icon_size=20,
            border=colors[5],
            borderwidth=1,
            max_title_width=30,
            padding=1,
            rounded=True,
            txt_floating="🗗",
            txt_minimized="🗕",
            parse_text=window_name_text_parser,
            font=default_font,
        ),
        widget.Spacer(background=colors[0]),
        widget.GroupBox(
            fontsize=font_size,
            font=default_font,
            margin_y=0,
            margin_x=0,
            padding_y=0,
            padding_x=3,
            borderwidth=0,
            disable_drag=False,
            active=colors[1],
            inactive=colors[3],
            highlight_color=colors[
                5
            ],  # highlight color is not used instead simple text color so that eyes are not . you got it right
            block_highlight_text_color=colors[2],
            this_current_screen_border=colors[2],
            this_screen_border=colors[4],
            foreground=colors[2],
            background=colors[0],
            rounded=False,
            highlight_method="line",
            invert_mouse_wheel=True,
            center_aligned=False,
            hide_unused=False,
        ),
        widget.Spacer(background=colors[0]),
        # crypto tracker
        widget.CryptoTicker(
            background=colors[8],
            foreground=colors[9],
            crypto="BTC",
            currency="INR",
            format="{symbol} {amount:.2f} ",
            max_char=12,
            fontsize=font_size,
            font=default_font,
            symbol="",
            update_interval=10,
        ),
        widget.TextBox(
            text=" ",
            foreground=colors[7],
            background=colors[6],
            padding=3,
            fontsize=font_size,
        ),
        widget.Memory(
            format="{MemUsed: .2f}",
            update_interval=5,
            fontsize=font_size,
            font=default_font,
            foreground=colors[7],
            background=colors[6],
            mouse_callbacks={"Button1": launch_htop},
        ),
        widget.TextBox(
            text=" ",
            foreground=colors[9],
            background=colors[8],
            padding=3,
            fontsize=font_size,
        ),
        widget.Clock(
            foreground=colors[9],
            background=colors[8],
            fontsize=font_size,
            font=default_font,
            format="%Y-%m-%d %H:%M",
        ),
        widget.TextBox(
            text=" ",
            foreground=colors[7],
            background=colors[6],
            padding=3,
            fontsize=font_size,
        ),
        widget.Battery(
            update_interval=10,
            fontsize=font_size,
            font=default_font,
            foreground=colors[7],
            background=colors[6],
            format="{percent:2.0%} {char}",
        ),
        widget.TextBox(
            text=" ",
            foreground=colors[9],
            background=colors[8],
            padding=3,
            fontsize=font_size,
        ),
        widget.Backlight(
            foreground=colors[9],
            background=colors[8],
            backlight_name="acpi_video0",
            brightness_file="/sys/class/backlight/intel_backlight/brightness",
            change_command="light -S {0}",
            max_brightness_file="/sys/class/backlight/intel_backlight/max_brightness",
            step=10,
            update_interval=0.2,
            max_chars=0,
            format="{percent:2.0%}",
            fontsize=font_size,
            font=default_font,
        ),
        widget.Systray(
            background=colors[8],
            foreground=colors[9],
            icon_size=18,
            padding=8,
            margin=2,
        ),
    ]


def screenBottomWidgetList():
    return [
        # put extra bullet text to cover the area of the bar
        widget.TextBox(
            text=" • • •  ",
            foreground=colors[6],
            background=colors[0],
            padding=0,
            fontsize=30,
        ),
        widget.GroupBox(
            font="FontAwesome",
            fontsize=font_size,
            margin_y=0,
            margin_x=0,
            padding_y=8,
            padding_x=5,
            borderwidth=0,
            disable_drag=False,
            active=colors[8],
            inactive=colors[7],
            rounded=True,
            highlight_color=colors[8],
            highlight_method="line",
            this_current_screen_border=colors[1],
            this_screen_border=colors[1],
            foreground=colors[1],
            background=colors[0],
            invert_mouse_wheel=True,
            center_aligned=False,
            hide_unused=False,
            block_highlight_text_color=colors[9],
        ),
        # put extra bullet text to cover the area of the bar
        widget.TextBox(
            text="  • • •  ",
            foreground=colors[6],
            background=colors[0],
            padding=0,
            fontsize=30,
        ),
    ]


def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=screenTopWidgetList(),
                size=bar_size,
                margin=[0, margin, 0, margin],
                opacity=bar_opacity,
                background=colors[1],
            ),
            # bottom=bar.Bar(
            #    widgets=screenBottomWidgetList(),
            #    size=25,
            #    margin=[0, marginHorizontalBottom, 0, marginHorizontalBottom],
            #    opacity=1,
            #    background=colors[1],
            # ),
        ),
        Screen(
            top=bar.Bar(
                widgets=screenTopWidgetList(), size=27, opacity=1, background=colors[1]
            )
        ),
    ]


# required variable even if it is not in use
screens = init_screens()

# MOUSE CONFIGURATION
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
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])


@hook.subscribe.client_new
def set_floating(window):
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="Arcolinux-welcome-app.py"),
        Match(wm_class="Arcolinux-tweak-tool.py"),
        Match(wm_class="Arcolinux-calamares-tool.py"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="Arandr"),
        Match(wm_class="feh"),
        Match(wm_class="Galculator"),
        Match(wm_class="arcolinux-logout"),
        Match(wm_class="xfce4-terminal"),
    ],
    fullscreen_border_width=0,
    border_width=0,
)
auto_fullscreen = True
focus_on_window_activation = "focus"  # or smart
wmname = "LG3D"
