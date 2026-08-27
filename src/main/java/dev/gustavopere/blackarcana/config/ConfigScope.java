package dev.gustavopere.blackarcana.config;

public enum ConfigScope {
    SERVER(true, false),
    COMMON(false, false),
    CLIENT(false, true);

    private final boolean gameplayAuthority;
    private final boolean clientOnly;

    ConfigScope(boolean gameplayAuthority, boolean clientOnly) {
        this.gameplayAuthority = gameplayAuthority;
        this.clientOnly = clientOnly;
    }

    public boolean isGameplayAuthority() {
        return gameplayAuthority;
    }

    public boolean isClientOnly() {
        return clientOnly;
    }
}
