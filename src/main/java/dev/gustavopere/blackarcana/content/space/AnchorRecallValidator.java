package dev.gustavopere.blackarcana.content.space;

import java.util.Objects;
import java.util.UUID;

/** Server-owned ownership/age/range validation for Anchor Recall. */
public final class AnchorRecallValidator {
    private final SafeDestinationPolicy destinationPolicy;

    public AnchorRecallValidator(SafeDestinationPolicy destinationPolicy) {
        this.destinationPolicy = Objects.requireNonNull(destinationPolicy, "destinationPolicy");
    }

    public Result validate(UUID casterId, long nowTick, Anchor anchor) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(anchor, "anchor");
        if (!casterId.equals(anchor.ownerId())) return Result.deny("foreign_projectile");
        if (nowTick < anchor.createdAtTick()) return Result.deny("clock_invalid");
        long age = nowTick - anchor.createdAtTick();
        if (age > anchor.maxAgeTicks()) return Result.deny("projectile_expired");
        if (anchor.distance() > anchor.maxRange()) return Result.deny("projectile_out_of_range");
        SafeDestinationPolicy.Decision destination = destinationPolicy.validate(anchor.destinationFacts());
        return destination.allowed() ? Result.allow() : Result.deny(destination.code());
    }

    public record Anchor(
        UUID ownerId,
        long createdAtTick,
        long maxAgeTicks,
        double distance,
        double maxRange,
        SafeDestinationPolicy.Facts destinationFacts
    ) {
        public Anchor {
            Objects.requireNonNull(ownerId, "ownerId");
            Objects.requireNonNull(destinationFacts, "destinationFacts");
            if (createdAtTick < 0L) throw new IllegalArgumentException("createdAtTick invalid");
            if (maxAgeTicks <= 0L || maxAgeTicks > LiminalSafetyCeilings.MAX_RECALL_PROJECTILE_AGE_TICKS) {
                throw new IllegalArgumentException("maxAgeTicks outside hard ceiling");
            }
            if (!Double.isFinite(distance) || distance < 0.0D) throw new IllegalArgumentException("distance invalid");
            if (!Double.isFinite(maxRange) || maxRange <= 0.0D || maxRange > LiminalSafetyCeilings.MAX_RECALL_RANGE) {
                throw new IllegalArgumentException("maxRange outside hard ceiling");
            }
        }
    }

    public record Result(boolean allowed, String code) {
        public Result { Objects.requireNonNull(code, "code"); }
        static Result allow() { return new Result(true, ""); }
        static Result deny(String code) { return new Result(false, code); }
    }
}
