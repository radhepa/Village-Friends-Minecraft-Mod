package dev.villagefriends.animation;

/**
 * Keyframes for one channel, sampled with monotone cubic curves: smooth through every key,
 * flat at holds and at both ends, and never overshooting a key. Sampling allocates nothing.
 */
public final class AnimationTrack {
    private final float[] times;
    private final float[] values;
    private final float[] slopes;

    /** {@code values} holds three components per key; unused components stay zero. */
    public AnimationTrack(float[] times, float[] values) {
        if (times.length == 0 || values.length != times.length * 3) throw new IllegalArgumentException("Track needs three values per key");
        for (int i = 1; i < times.length; i++)
            if (!(times[i] > times[i - 1])) throw new IllegalArgumentException("Keyframe times must increase");
        this.times = times.clone(); this.values = values.clone(); this.slopes = new float[values.length];
        int n = times.length;
        for (int c = 0; c < 3; c++) {
            for (int k = 1; k < n - 1; k++) {
                float before = secant(k - 1, c), after = secant(k, c);
                slopes[k * 3 + c] = before * after <= 0 ? 0 : (before + after) / 2;
            }
            // Fritsch-Carlson limiting keeps every segment monotone between its keys.
            for (int k = 0; k < n - 1; k++) {
                float d = secant(k, c);
                if (d == 0) { slopes[k * 3 + c] = 0; slopes[(k + 1) * 3 + c] = 0; continue; }
                float a = slopes[k * 3 + c] / d, b = slopes[(k + 1) * 3 + c] / d, sum = a * a + b * b;
                if (sum > 9) {
                    float scale = 3 / (float) Math.sqrt(sum);
                    slopes[k * 3 + c] = scale * a * d; slopes[(k + 1) * 3 + c] = scale * b * d;
                }
            }
        }
    }
    private float secant(int k, int c) { return (values[(k + 1) * 3 + c] - values[k * 3 + c]) / (times[k + 1] - times[k]); }

    public int keys() { return times.length; }
    public float time(int key) { return times[key]; }
    public float value(int key, int component) { return values[key * 3 + component]; }
    public float end() { return times[times.length - 1]; }

    /** Writes the pose at {@code t} seconds into {@code out[offset..offset+2]}. */
    public void sample(float t, float[] out, int offset) {
        int n = times.length;
        if (n == 1 || t <= times[0]) { copy(0, out, offset); return; }
        if (t >= times[n - 1]) { copy(n - 1, out, offset); return; }
        int k = 0;
        while (k < n - 2 && t >= times[k + 1]) k++;
        float h = times[k + 1] - times[k], s = (t - times[k]) / h, s2 = s * s, s3 = s2 * s;
        float h00 = 2 * s3 - 3 * s2 + 1, h10 = s3 - 2 * s2 + s, h01 = -2 * s3 + 3 * s2, h11 = s3 - s2;
        for (int c = 0; c < 3; c++) {
            int a = k * 3 + c, b = a + 3;
            out[offset + c] = h00 * values[a] + h10 * h * slopes[a] + h01 * values[b] + h11 * h * slopes[b];
        }
    }
    private void copy(int key, float[] out, int offset) { System.arraycopy(values, key * 3, out, offset, 3); }
}
