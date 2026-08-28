package dev.gustavopere.blackarcana.api;

public enum ArcanaPaymentPolicy {
    ALWAYS_PAY,
    BYPASS_CREATIVE,
    BYPASS_ADMIN,
    BYPASS_CREATIVE_AND_ADMIN;

    public boolean bypasses(ArcanaCasterMode mode) {
        return switch (this) {
            case ALWAYS_PAY -> false;
            case BYPASS_CREATIVE -> mode == ArcanaCasterMode.CREATIVE;
            case BYPASS_ADMIN -> mode == ArcanaCasterMode.ADMIN;
            case BYPASS_CREATIVE_AND_ADMIN -> mode == ArcanaCasterMode.CREATIVE || mode == ArcanaCasterMode.ADMIN;
        };
    }
}
