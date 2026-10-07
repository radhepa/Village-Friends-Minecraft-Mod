"""Generate the wordless, human-like voice sounds used by Village Friends.

Everything is synthesised here from scratch (glottal pulse source through vowel
formant filters, plus a nasal hum for the "mm" sounds), so there is no sampled
speech and no third-party licence to carry. Output is Ogg Vorbis via ffmpeg:

  assets/villagefriends/sounds/voice/*.ogg   replace the vanilla villager voice
  assets/villagefriends/sounds/ui/*.ogg      dialogue typewriter blips and pop

Run:  python tools/make_voice_sounds.py
"""
import os
import subprocess
import tempfile
import wave

import numpy as np

SR = 44100
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources",
                    "assets", "villagefriends", "sounds")
rng = np.random.default_rng(1207)

# (F1, F2, F3) in Hz for a soft, mid-pitched voice.
VOWELS = {
    "a": (730, 1090, 2440), "e": (530, 1840, 2480), "i": (300, 2290, 3010),
    "o": (570, 840, 2410), "u": (325, 700, 2530), "m": (250, 1100, 2200),
}


def glottal(f0, n):
    """Band-limited-ish glottal source: a sawtooth with a gentle low-pass, plus breath."""
    phase = np.cumsum(f0) / SR
    saw = 2.0 * (phase % 1.0) - 1.0
    # one-pole low-pass to soften the buzz
    out = np.empty_like(saw)
    acc = 0.0
    for i in range(n):
        acc += 0.35 * (saw[i] - acc)
        out[i] = acc
    return out + 0.015 * rng.standard_normal(n)


def resonator(x, freq, bw):
    r = np.exp(-np.pi * bw / SR)
    theta = 2 * np.pi * freq / SR
    a1, a2 = -2 * r * np.cos(theta), r * r
    y = np.zeros_like(x)
    y1 = y2 = 0.0
    g = 1 - r
    for i in range(len(x)):
        v = g * x[i] - a1 * y1 - a2 * y2
        y[i] = v
        y2, y1 = y1, v
    return y


def voiced(f0_curve, vowel, nasal=0.0, dur=0.2, vib=0.0):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f0 = np.interp(t, np.linspace(0, dur, len(f0_curve)), f0_curve)
    if vib:
        f0 = f0 * (1 + vib * np.sin(2 * np.pi * 5.2 * t))
    src = glottal(f0, n)
    f1, f2, f3 = VOWELS[vowel]
    y = resonator(src, f1, 90) + 0.7 * resonator(src, f2, 110) + 0.35 * resonator(src, f3, 160)
    if nasal:
        y = (1 - nasal) * y + nasal * resonator(src, 250, 70) * 1.4
    return y


def envelope(n, attack, release, shape=1.0):
    env = np.ones(n)
    a, r = int(SR * attack), int(SR * release)
    env[:a] = np.linspace(0, 1, a) ** shape
    env[-r:] = np.linspace(1, 0, r) ** 1.5
    return env


def finish(y, peak=0.55):
    y = np.concatenate([y, np.zeros(int(SR * 0.02))])
    y = y / (np.max(np.abs(y)) + 1e-9) * peak
    return y


def write_ogg(name, y):
    path = os.path.normpath(os.path.join(ROOT, name + ".ogg"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_name = tmp.name
    with wave.open(tmp_name, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_name, "-c:a", "libvorbis", "-q:a", "4", path],
                   check=True)
    os.remove(tmp_name)
    print("wrote", os.path.relpath(path, ROOT), f"{len(y) / SR:.2f}s")


def hum(base, vowels, dur, glide=0.0, nasal=0.7):
    """A soft sustained 'mm' that opens into a vowel and back: wordless, like a hum."""
    n = int(SR * dur)
    parts = []
    seg = dur / len(vowels)
    for k, v in enumerate(vowels):
        f0 = [base * (1 + glide * k / max(1, len(vowels) - 1)),
              base * (1 + glide * (k + 0.6) / max(1, len(vowels) - 1))]
        parts.append(voiced(f0, v, nasal=nasal if v == "m" else nasal * 0.25, dur=seg, vib=0.012))
    y = np.concatenate(parts)
    return finish(y * envelope(len(y), 0.05, 0.12))


# ---- villager voice replacements -------------------------------------------------------------
def make_voice():
    # ambient: gentle idle hums, three takes
    for i, (b, vs) in enumerate([(150, "mum"), (165, "mom"), (140, "mim")], 1):
        write_ogg(f"voice/ambient{i}", hum(b, list(vs), 0.55 + 0.05 * i, glide=0.04) * 0.55)
    # yes: rising "mm-hm" (two short nasal notes, second higher)
    for i, b in enumerate([170, 185, 160], 1):
        a = hum(b, ["m", "u"], 0.16, nasal=0.8)
        c = hum(b * 1.28, ["m", "a"], 0.2, nasal=0.8)
        write_ogg(f"voice/yes{i}", np.concatenate([a, np.zeros(int(SR * 0.04)), c]))
    # no: falling "mm-mm"
    for i, b in enumerate([170, 155, 180], 1):
        a = hum(b * 1.1, ["m", "o"], 0.17, nasal=0.8)
        c = hum(b * 0.82, ["m", "o"], 0.22, nasal=0.8)
        write_ogg(f"voice/no{i}", np.concatenate([a, np.zeros(int(SR * 0.04)), c]))
    # trade: quick considering hums
    for i, b in enumerate([165, 175, 155], 1):
        write_ogg(f"voice/trade{i}", np.concatenate([hum(b, ["m", "e"], 0.13, nasal=0.7),
                                                     hum(b * 1.12, ["m", "i"], 0.13, nasal=0.7)]))
    # hurt: short open vowel, pitched up
    for i, b in enumerate([220, 245, 205, 230], 1):
        y = voiced([b * 1.15, b * 0.9], "a", dur=0.18, vib=0.02)
        write_ogg(f"voice/hurt{i}", finish(y * envelope(len(y), 0.01, 0.1)))
    # death: long falling vowel
    y = voiced([210, 150, 95], "o", dur=0.7, vib=0.015)
    write_ogg("voice/death", finish(y * envelope(len(y), 0.02, 0.35)))


# ---- dialogue blips and pop ------------------------------------------------------------------
def make_ui():
    # Animalese-style blips: very short vowel puffs, one per vowel colour, each played at
    # slightly different pitches by the screen.
    for name, v in [("blip_a", "a"), ("blip_e", "e"), ("blip_i", "i"), ("blip_o", "o"), ("blip_u", "u")]:
        y = voiced([240, 252], v, dur=0.075)
        y = y * envelope(len(y), 0.004, 0.035)
        write_ogg(f"ui/{name}", finish(y, 0.5))
    # pop: a soft bubble pop, a fast pitch drop on a sine plus a touch of noise
    n = int(SR * 0.09)
    t = np.arange(n) / SR
    f = 700 * np.exp(-t * 28) + 180
    pop = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 46)
    pop += 0.08 * rng.standard_normal(n) * np.exp(-t * 90)
    write_ogg("ui/pop", finish(pop, 0.6))


if __name__ == "__main__":
    make_voice()
    make_ui()
