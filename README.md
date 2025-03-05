# Shadow Assault

**Shadow Assault** is an immersive first-person shooter game built using the Ursina engine. Dive into intense combat, strategize your moves, and eliminate your enemies in this action-packed game.

## Features
- **Advanced Enemy AI**: Enemies with unique behaviors and complex AI patterns.
- **Weapon System**: Multiple weapon types with modifications and ADS functionality.
- **Particle Effects**: Realistic explosion and trail effects.
- **User Interface**: Animated menus, loading screens, and HUD.
- **Persistence**: Settings persistence and leaderboard system.
- **Achievements**: Unlock achievements and receive notifications.

## Project Structure
```plaintext
shadow-assault/
├── assets/
│   ├── models/
│   ├── textures/
│   ├── sounds/
│   ├── animations/
├── src/
│   ├── config/
│   │   ├── enemy_config.py
│   │   ├── ui_config.py
│   │   └── weapon_config.py
│   ├── effects/
│   │   ├── advanced_particles.py
│   │   └── particle_system.py
│   ├── enemies/
│   │   └── enemy_ai.py
│   ├── player/
│   │   └── player.py
│   ├── ui/
│   │   ├── animated_menu.py
│   │   ├── game_over_screen.py
│   │   ├── hud.py
│   │   ├── loading_screen.py
│   │   ├── main_menu.py
│   │   ├── pause_menu.py
│   │   └── tutorial_system.py
│   ├── utils/
│   │   ├── achievement_system.py
│   │   ├── leaderboard.py
│   │   └── settings_manager.py
│   ├── weapons/
│   │   ├── advanced_weapon.py
│   │   ├── weapon_animator.py
│   │   └── weapon_pickup.py
│   └── main.py
└── README.md
```

## Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/ShivamKR12/shadow-assault.git
   cd shadow-assault
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the game:
   ```sh
   python src/main.py
   ```

## Contributing
Feel free to contribute to the project by submitting issues or pull requests. Make sure to follow the code of conduct.

## License
This project is licensed under the MIT License.
