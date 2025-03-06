from ursina import Vec3, color

WEAPON_TYPES = {
    'pistol': {
        'name': 'M9 Pistol',
        'damage': 25,
        'fire_rate': 0.25,
        'range': 50,
        'magazine_size': 15,
        'reload_time': 1.5,
        'type': 'semi',
        'accuracy': 0.95,
        'mobility': 1.0,
        'ads_fov': 65,
        'ads_position': Vec3(0, -0.2, 0.5),
        'sway_amount': Vec3(0.1, 0.1, 0.1),
        'model_path': 'assets/models/weapons/pistol.obj',
        'animations': {
            'idle': 'assets/animations/weapons/pistol/idle.anim',
            'fire': 'assets/animations/weapons/pistol/fire.anim',
            'reload': 'assets/animations/weapons/pistol/reload.anim',
            'draw': 'assets/animations/weapons/pistol/draw.anim'
        }
    },
    'rifle': {
        'name': 'M4 Rifle',
        'damage': 30,
        'fire_rate': 0.1,
        'range': 100,
        'magazine_size': 30,
        'reload_time': 2.0,
        'type': 'auto',
        'accuracy': 0.9,
        'mobility': 0.8,
        'ads_fov': 55,
        'ads_position': Vec3(0, -0.15, 0.3),
        'sway_amount': Vec3(0.15, 0.15, 0.15),
        'model_path': 'assets/models/weapons/rifle.obj',
        'animations': {
            'idle': 'assets/animations/weapons/rifle/idle.anim',
            'fire': 'assets/animations/weapons/rifle/fire.anim',
            'reload': 'assets/animations/weapons/rifle/reload.anim',
            'draw': 'assets/animations/weapons/rifle/draw.anim'
        }
    },
    'shotgun': {
        'name': 'Combat Shotgun',
        'damage': 20,  # Per pellet
        'pellets': 8,
        'fire_rate': 0.8,
        'range': 30,
        'magazine_size': 6,
        'reload_time': 0.5,  # Per shell
        'type': 'pump',
        'accuracy': 0.8,
        'mobility': 0.7,
        'ads_fov': 60,
        'ads_position': Vec3(0, -0.1, 0.4),
        'sway_amount': Vec3(0.2, 0.2, 0.2),
        'model_path': 'assets/models/weapons/shotgun.obj',
        'animations': {
            'idle': 'assets/animations/weapons/shotgun/idle.anim',
            'fire': 'assets/animations/weapons/shotgun/fire.anim',
            'pump': 'assets/animations/weapons/shotgun/pump.anim',
            'reload_start': 'assets/animations/weapons/shotgun/reload_start.anim',
            'reload_insert': 'assets/animations/weapons/shotgun/reload_insert.anim',
            'reload_end': 'assets/animations/weapons/shotgun/reload_end.anim',
            'draw': 'assets/animations/weapons/shotgun/draw.anim'
        }
    }
}

MODIFICATION_TYPES = {
    'scope': {
        'red_dot': {
            'name': 'Red Dot Sight',
            'ads_fov': -5,  # Reduces FOV by 5
            'ads_speed': 1.2,
            'model_path': 'assets/models/attachments/red_dot.obj'
        },
        'acog': {
            'name': 'ACOG Scope',
            'ads_fov': -10,
            'ads_speed': 0.8,
            'model_path': 'assets/models/attachments/acog.obj'
        }
    },
    'barrel': {
        'suppressor': {
            'name': 'Suppressor',
            'noise_reduction': 0.7,
            'damage_range': 0.9,
            'model_path': 'assets/models/attachments/suppressor.obj'
        },
        'compensator': {
            'name': 'Compensator',
            'recoil_reduction': 0.8,
            'model_path': 'assets/models/attachments/compensator.obj'
        }
    },
    'magazine': {
        'extended': {
            'name': 'Extended Magazine',
            'capacity_multiplier': 1.5,
            'reload_time_multiplier': 1.2,
            'model_path': 'assets/models/attachments/ext_mag.obj'
        },
        'quick': {
            'name': 'Quick-Draw Magazine',
            'reload_time_multiplier': 0.8,
            'model_path': 'assets/models/attachments/quick_mag.obj'
        }
    }
}
