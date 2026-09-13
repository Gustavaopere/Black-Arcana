package dev.gustavopere.blackarcana.client;

/** Pure contained geometry for the bounded Stage 05.16 discoverability cue. */
record DiscoverabilityHintLayout(int x, int y, int width, int maxHeight) {
    private static final int MARGIN = 8;
    private static final int PREFERRED_WIDTH = 360;
    private static final int PREFERRED_MAX_HEIGHT = 112;

    DiscoverabilityHintLayout {
        if (x < 0 || y < 0 || width <= 0 || maxHeight <= 0) {
            throw new IllegalArgumentException("invalid discoverability hint layout");
        }
    }

    static DiscoverabilityHintLayout forViewport(int viewportWidth, int viewportHeight) {
        if (viewportWidth <= 0 || viewportHeight <= 0) {
            throw new IllegalArgumentException("viewport dimensions must be positive");
        }

        int x = viewportWidth > MARGIN * 2 ? MARGIN : 0;
        int y = viewportHeight > MARGIN * 2 ? MARGIN : 0;
        int width = Math.max(1, Math.min(PREFERRED_WIDTH, viewportWidth - x * 2));
        int maxHeight = Math.max(1, Math.min(PREFERRED_MAX_HEIGHT, viewportHeight - y * 2));
        return new DiscoverabilityHintLayout(x, y, width, maxHeight);
    }
}
