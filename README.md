# CIIE
Repositorio para la creacion de un juego en 2D con Pygame y un juego en 3D usando Unity

## Skelly and Soulie (2D)

## Descripción
Skelly and Soulie es un juego de plataformas en 2D que cuenta con tres niveles y una batalla final. Ofrece dos resoluciones de pantalla (1280x720 y 720x405), tres niveles de dificultad y diálogos disponibles en inglés, castellano y gallego.

## Requisitos
Para ejecutar el juego desde el código fuente, necesitas tener instalado:
- Python 3.x
- Pygame

El juego también utiliza los módulos estándar de Python:
- `sys`
- `random`

## Instalación
### Windows
1. Asegúrate de tener instalado Python 3.
2. Instala las dependencias ejecutando:
   ```sh
   pip install pygame
   ```

### Linux
1. Asegúrate de tener instalado Python 3.
2. Instala las dependencias ejecutando:
   ```sh
   pip install pygame
   ```

## Ejecución
Para jugar desde el código fuente, navega a la carpeta `src` y ejecuta:
```sh
python main.py
```

Si prefieres jugar con el ejecutable, simplemente abre `Skelly and Soulie.exe` en Windows.

## Ejecutable
Se incluye un ejecutable precompilado para Windows: `Skelly and Soulie.exe`.
Si deseas generar un nuevo ejecutable, usa el siguiente comando:
```sh
pyinstaller --onefile --windowed --name "Skelly and Soulie" \
--add-data "Art;Art" --add-data "ButtonText;ButtonText" \
--add-data "config;config" --add-data "Credits;Credits" \
--add-data "Dialog;Dialog" --add-data "Font;Font" \
--add-data "Sound;Sound" --add-data "save;save" main.py
```

## Estructura del Proyecto
```
Skelly_and_Soulie/
│── src/
│   ├── classes/
│   ├── enemies/
│   ├── game/
│   │   ├── objects/
│   │   │   ├── decor/
│   ├── save/
│   ├── utils/
│   ├── views/
│   ├── main.py
│── assets/
│   ├── Art/
│   │   ├── 1280x720/
│   │   ├── 720x405/
│   │   ├── common/
│   ├── ButtonText/
│   ├── config/
│   ├── Credits/
│   ├── Dialog/
│   ├── Font/
│   ├── Sound/
│   │   ├── BSO/
│   │   ├── FX/
```




