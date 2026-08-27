package dev.gustavopere.blackarcana.api;

public interface ArcanaIntegration {
    String integrationId();
    boolean available();
    String implementationVersion();
}
