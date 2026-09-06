package dev.gustavopere.blackarcana.client;

/** Pure responsive geometry for the Stage 05 loadout editor. */
public record LoadoutLayout(
        int left,
        int top,
        int panelWidth,
        int rowsPerPage,
        int rowHeight
) {
    private static final int OUTER_HORIZONTAL_MARGIN = 8;
    private static final int TITLE_HEIGHT = 24;
    private static final int FOOTER_HEIGHT = 48;
    private static final int DEFAULT_PANEL_WIDTH = 300;
    private static final int DEFAULT_ROWS_PER_PAGE = 8;
    private static final int DEFAULT_ROW_HEIGHT = 22;
    private static final int MIN_ROW_HEIGHT = 18;

    public LoadoutLayout {
        if (left < 0 || top < 0 || panelWidth <= 0 || rowsPerPage <= 0 || rowHeight <= 0) {
            throw new IllegalArgumentException("invalid loadout layout");
        }
    }

    public static LoadoutLayout forViewport(int viewportWidth, int viewportHeight) {
        if (viewportWidth <= 0 || viewportHeight <= 0) {
            throw new IllegalArgumentException("viewport dimensions must be positive");
        }

        int panelWidth = Math.min(DEFAULT_PANEL_WIDTH,
                Math.max(1, viewportWidth - OUTER_HORIZONTAL_MARGIN * 2));
        int availableRowsHeight = Math.max(1, viewportHeight - TITLE_HEIGHT - FOOTER_HEIGHT);

        int rowHeight = Math.min(DEFAULT_ROW_HEIGHT,
                Math.max(MIN_ROW_HEIGHT, availableRowsHeight / DEFAULT_ROWS_PER_PAGE));
        int rowsPerPage = Math.max(1,
                Math.min(DEFAULT_ROWS_PER_PAGE, availableRowsHeight / rowHeight));

        int outerHeight = TITLE_HEIGHT + rowsPerPage * rowHeight + FOOTER_HEIGHT;
        int left = Math.max(OUTER_HORIZONTAL_MARGIN, (viewportWidth - panelWidth) / 2);
        int top = TITLE_HEIGHT + Math.max(0, (viewportHeight - outerHeight) / 2);
        return new LoadoutLayout(left, top, panelWidth, rowsPerPage, rowHeight);
    }

    public int pageCount(int totalEntries) {
        if (totalEntries < 0) throw new IllegalArgumentException("totalEntries cannot be negative");
        return Math.max(1, (totalEntries + rowsPerPage - 1) / rowsPerPage);
    }

    public int clampPage(int totalEntries, int page) {
        return Math.max(0, Math.min(page, pageCount(totalEntries) - 1));
    }
}
