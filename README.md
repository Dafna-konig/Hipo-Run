# Mini Juego Hipo Run

Implementación de un juego tipo *infinite runner* desarrollado en Pygame, en el que debes esquivar obstáculos de tortugas y murciélagos con Hipo.

La dificultad va aumentando progresivamente a medida que avanzas en el juego. 
Atrapa los huevos mágicos para obtener puntos extras y rescatar a los 24 mini hipos coleccionables.

<p align="center">
    <img src="Assets/Juego.png" alt="Inicio del juego" width="400"/>
    <img src="Assets/Juego1.png" alt="Fin del juego" width="400"/>
</p>

## Novedades y Mejoras Recientes

- **Álbum Coleccionable de Mini Hipos:**
  - Los 24 mini hipos ahora son coleccionables permanentes con nombres propios (Sylvia, Mora, Bigotes, Chunky, etc.).
  - Nueva pantalla de **Álbum / Colección** accesible con la tecla <kbd>C</kbd> o mediante los botones de inicio y game over.
  - Los mini hipos no descubiertos aparecen como siluetas misteriosas con `???`.
  - Al atrapar huevos mágicos, el juego prioriza descubrir nuevos mini hipos para tu colección y los destaca con una etiqueta `¡NUEVO!`.
  - Tu progreso se guarda automáticamente en `highscore.json`.
- **Fondo y Pasto con Transparencia Real:**
  - Se eliminó el fondo cian opaco que venía incrustado en la imagen del pasto, recortando con canal alfa suave las briznas y flores.
  - El pasto ahora se integra de forma transparente sobre el cielo, las nubes flotantes y las colinas lejanas sin cortes rectangulares.
  - Lecho de tierra/pradera suave en la base para un suelo sólido y armonioso.
- **Efectos de Sonido Retro (8-bit):** Sonidos procedurales generados por código (salto, agacharse, atrapar huevo, nuevo récord, game over y clics) sin necesidad de archivos de audio externos.
- **Fondo Parallax Multicapa:** Cielo con degradado suave, nubes procedimentales que flotan naturalmente, colinas onduladas distantes y decorados en movimiento con sensación de profundidad.
- **Sistema de Partículas:** Polvo al correr y al aterrizar, destellos de estrellas de colores y texto flotante `+10` al atrapar huevos, y ondas de choque con impacto.
- **Efecto Screen-Shake:** Sacudida de pantalla al chocar para dar mayor impacto y respuesta visual.
- **Récord Guardado (High Score):** Registro persistente de tu mejor puntaje y máxima cantidad de mini hipos rescatados.
- **Controles Mejorados y Game Feel:**
  - Salto variable (mantener para salto alto, soltar para salto corto).
  - *Jump Buffering* (reconoce el salto si presionas antes de tocar el suelo).
  - Caída rápida (*fast fall*) al agacharse en el aire.
  - Menú de pausa.
- **Optimización de Rendimiento:** Precarga y caché de sprites en memoria con aceleración `.convert_alpha()`.
- **Compatibilidad Multiplataforma:** Rutas de archivos estandarizadas para evitar problemas de mayúsculas/minúsculas en Linux, macOS y Windows.

## Instalación 

1. Clona este repositorio:
```bash
git clone https://github.com/Dafna-konig/Hipo-Run.git
```

2. Navega hasta la carpeta del proyecto:
```bash
cd Hipo-Run
```

3. Crea un entorno virtual y actívalo:

    Para Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
    Para Mac / Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4. Instala Pygame:
```bash
pip install pygame
```

5. Corre el juego:
```bash
python hipo.py
```

## Controles

| Acción | Teclas |
| :--- | :--- |
| **Saltar** (altura variable) | <kbd>Espacio</kbd>, <kbd>Flecha Arriba</kbd> ($\uparrow$), o <kbd>W</kbd> |
| **Agacharse / Caída rápida** | <kbd>Flecha Abajo</kbd> ($\downarrow$), o <kbd>S</kbd> |
| **Álbum / Colección de Mini Hipos** | <kbd>C</kbd> o clic en el botón del menú |
| **Pausar / Reanudar** | <kbd>P</kbd> o <kbd>ESC</kbd> |
| **Mutear / Activar sonido** | <kbd>M</kbd> |
| **Reiniciar partida** | <kbd>R</kbd>, <kbd>Espacio</kbd> o clic |
| **Ver hitboxes (Debug)** | <kbd>F3</kbd> o <kbd>H</kbd> |

¡Intenta conseguir la mayor cantidad de puntos y rescatar a los 24 mini hipos para completar tu álbum!
