import json
import os
from libqtile import layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

# Load pywal colors
colors = []
cache_dir = os.path.expanduser("~/.cache/wal/colors")
if os.path.isfile(cache_dir):
    with open(cache_dir, "r") as file:
        for line in file:
            colors.append(line.strip())
else:
    # Fallback colors if pywal hasn't been run
    colors = [
        "#000000",  # black
        "#ff0000",  # red
        "#00ff00",  # green
        "#ffff00",  # yellow
        "#0000ff",  # blue
        "#ff00ff",  # magenta
        "#00ffff",  # cyan
        "#ffffff",  # white
    ]

# Load pywal JSON data for additional colors
wal_cache = os.path.expanduser("~/.cache/wal/colors.json")
if os.path.isfile(wal_cache):
    with open(wal_cache, "r") as file:
        wal_colors = json.load(file)
        background = wal_colors["special"]["background"]
        foreground = wal_colors["special"]["foreground"]
else:
    background = colors[0]
    foreground = colors[7]

mod = "mod4"
terminal = "kitty"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Grow windows
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Toggle between split and unsplit sides of stack
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    
    # Launch terminal
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    
    # Toggle between layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    
    # Window controls
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    
    # Qtile controls
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Add key bindings for VT switching in Wayland
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc=f"Switch to group {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc=f"Switch to & move focused window to group {i.name}"),
    ])

layouts = [
    layout.Columns(
        border_focus=colors[4],
        border_normal=background,
        border_width=2,
        margin=4,
    ),
    layout.Max(),
    layout.MonadTall(
        border_focus=colors[4],
        border_normal=background,
        border_width=2,
        margin=4,
    ),
]

# Screen setup without a bar (since we're using Polybar)
screens = [Screen()]

# Drag floating layouts
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
    border_focus=colors[4],
    border_normal=background,
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"
