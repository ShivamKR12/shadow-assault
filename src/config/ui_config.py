from ursina import color, Vec2, Vec4

UI_CONFIG = {
    'colors': {
        'primary': color.azure,
        'secondary': color.light_gray,
        'background': color.rgba(0, 0, 0, 0.8),
        'danger': color.red,
        'success': color.green,
        'warning': color.yellow,
        'text': color.white
    },
    'fonts': {
        'default': 'assets/fonts/arial.ttf',
        'title': 'assets/fonts/roboto_bold.ttf'
    },
    'hud': {
        'health_bar_size': Vec2(0.4, 0.025),
        'health_bar_position': Vec2(-0.7, 0.45),
        'ammo_position': Vec2(0.7, -0.45),
        'score_position': Vec2(-0.7, 0.4),
        'crosshair_size': 0.02
    }
}

SOUND_CONFIG = {
    'master_volume': 1.0,
    'music_volume': 0.7,
    'sfx_volume': 0.8,
    'sounds': {
        'menu_click': 'assets/sounds/ui/click.wav',
        'menu_hover': 'assets/sounds/ui/hover.wav',
        'game_start': 'assets/sounds/ui/game_start.wav',
        'game_over': 'assets/sounds/ui/game_over.wav'
    }
}
