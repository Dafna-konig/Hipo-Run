import io
import math
import struct
import wave
import pygame


class AudioManager:
    """Procedural 8-bit sound generator and manager without external audio files."""

    def __init__(self):
        self.sounds = {}
        self.muted = False
        self.available = False

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self.available = True
            self._generate_all_sounds()
        except Exception as e:
            print(f"[Audio] Audio not available: {e}")
            self.available = False

    def _create_wav_sound(self, samples, sample_rate=44100):
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            for s in samples:
                val = max(-32767, min(32767, int(s * 32767)))
                wav.writeframes(struct.pack("<h", val))
        buf.seek(0)
        return pygame.mixer.Sound(buf)

    def _generate_all_sounds(self):
        rate = 44100

        # 1. JUMP: Retro rising sweep
        jump_samples = []
        n_jump = int(rate * 0.16)
        for i in range(n_jump):
            t = i / rate
            progress = i / n_jump
            freq = 260 + 420 * (progress ** 0.85)
            phase = 2 * math.pi * freq * t
            env = (1.0 - progress) ** 1.2
            # Add subtle square-wave harmonic
            val = (0.7 * math.sin(phase) + 0.3 * (1.0 if math.sin(phase) > 0 else -1.0)) * 0.38 * env
            jump_samples.append(val)
        self.sounds["jump"] = self._create_wav_sound(jump_samples, rate)

        # 2. DUCK: Quick low swoosh
        duck_samples = []
        n_duck = int(rate * 0.09)
        for i in range(n_duck):
            t = i / rate
            progress = i / n_duck
            freq = 280 - 140 * progress
            phase = 2 * math.pi * freq * t
            env = 1.0 - progress
            val = math.sin(phase) * 0.28 * env
            duck_samples.append(val)
        self.sounds["duck"] = self._create_wav_sound(duck_samples, rate)

        # 3. EGG: Sparkling two-tone arpeggio
        egg_samples = []
        n1 = int(rate * 0.07)
        for i in range(n1):
            t = i / rate
            env = 1.0 - 0.3 * (i / n1)
            val = math.sin(2 * math.pi * 587.33 * t) * 0.42 * env
            egg_samples.append(val)
        n2 = int(rate * 0.14)
        for i in range(n2):
            t = i / rate
            env = (1.0 - (i / n2)) ** 1.3
            val = (math.sin(2 * math.pi * 880.0 * t) + 0.25 * math.sin(2 * math.pi * 1760.0 * t)) * 0.42 * env
            egg_samples.append(val)
        self.sounds["egg"] = self._create_wav_sound(egg_samples, rate)

        # 4. GAME OVER: Descending 3-note melody
        go_samples = []
        notes = [(440.0, 0.12), (370.0, 0.12), (261.63, 0.24)]
        for freq, dur in notes:
            n_dur = int(rate * dur)
            for i in range(n_dur):
                t = i / rate
                env = (1.0 - (i / n_dur)) ** 1.1
                phase = 2 * math.pi * freq * t
                val = (0.75 * math.sin(phase) + 0.25 * math.sin(2 * phase)) * 0.45 * env
                go_samples.append(val)
        self.sounds["game_over"] = self._create_wav_sound(go_samples, rate)

        # 5. NEW RECORD: Happy victory fanfare (C-E-G-C)
        rec_samples = []
        rec_notes = [(523.25, 0.08), (659.25, 0.08), (783.99, 0.08), (1046.50, 0.25)]
        for freq, dur in rec_notes:
            n_dur = int(rate * dur)
            for i in range(n_dur):
                t = i / rate
                env = 1.0 - (i / n_dur) * 0.7
                phase = 2 * math.pi * freq * t
                val = (math.sin(phase) + 0.2 * math.sin(3 * phase)) * 0.38 * env
                rec_samples.append(val)
        self.sounds["record"] = self._create_wav_sound(rec_samples, rate)

        # 6. CLICK: Crisp short blip
        click_samples = []
        n_click = int(rate * 0.035)
        for i in range(n_click):
            t = i / rate
            env = 1.0 - (i / n_click)
            val = math.sin(2 * math.pi * 950 * t) * 0.35 * env
            click_samples.append(val)
        self.sounds["click"] = self._create_wav_sound(click_samples, rate)

    def play(self, sound_name):
        if not self.available or self.muted:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            try:
                snd.play()
            except Exception:
                pass

    def toggle_mute(self):
        self.muted = not self.muted
        return self.muted

    @property
    def status_text(self):
        return "SONIDO: OFF (M)" if self.muted else "SONIDO: ON (M)"
