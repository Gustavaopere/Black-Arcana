package dev.gustavopere.blackarcana.api;

import java.util.Objects;
import java.util.UUID;

/**
 * Pure-Java reference to a server-resolved target. Minecraft adapters encode
 * their live result into this form so spell effects do not rely on ad-hoc
 * string parsing or client-authored coordinates.
 */
public sealed interface ArcanaTargetReference permits ArcanaTargetReference.EntityRef, ArcanaTargetReference.BlockRef {
    String canonical();

    static ArcanaTargetReference parse(String value) {
        Objects.requireNonNull(value, "value");
        String[] parts = value.split("\\|", -1);
        if (parts.length == 2 && "entity".equals(parts[0])) {
            return new EntityRef(UUID.fromString(parts[1]));
        }
        if (parts.length == 5 && "block".equals(parts[0])) {
            try {
                return new BlockRef(
                        parts[1],
                        Integer.parseInt(parts[2]),
                        Integer.parseInt(parts[3]),
                        Integer.parseInt(parts[4]));
            } catch (NumberFormatException ex) {
                throw new IllegalArgumentException("invalid block target coordinates: " + value, ex);
            }
        }
        throw new IllegalArgumentException("unknown target reference: " + value);
    }

    record EntityRef(UUID entityId) implements ArcanaTargetReference {
        public EntityRef {
            Objects.requireNonNull(entityId, "entityId");
        }

        @Override
        public String canonical() {
            return "entity|" + entityId;
        }
    }

    record BlockRef(String dimensionId, int x, int y, int z) implements ArcanaTargetReference {
        public BlockRef {
            Objects.requireNonNull(dimensionId, "dimensionId");
            ArcanaSpellId.parse(dimensionId);
        }

        @Override
        public String canonical() {
            return "block|" + dimensionId + '|' + x + '|' + y + '|' + z;
        }
    }
}
