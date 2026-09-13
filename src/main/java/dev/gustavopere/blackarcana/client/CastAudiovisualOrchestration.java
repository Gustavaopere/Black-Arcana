package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;
import java.util.Optional;

/**
 * Surface-neutral audiovisual directives for Stage 05.15 Phase C.
 *
 * <p>These directives deliberately contain no target, impact position, world geometry, sound id,
 * particle id or provider animation id. Phase C can therefore communicate only facts already proven
 * by the local intent/server-result correlation contract. Resource/provider selection belongs to
 * later reviewed phases.</p>
 */
public final class CastAudiovisualOrchestration {
    public enum Kind {
        ANTICIPATION,
        RESULT_SUCCESS,
        RESULT_DENIED,
        RESULT_FAILED
    }

    public record Directive(
            ArcanaCastId castId,
            Optional<ArcanaSpellId> spellId,
            CastPresentationLifecycle.Authority authority,
            Kind kind,
            double decorativeParticleDensity,
            boolean optionalMotionAllowed,
            boolean flashHeavyEffectsAllowed
    ) {
        public Directive {
            Objects.requireNonNull(castId, "castId");
            Objects.requireNonNull(spellId, "spellId");
            Objects.requireNonNull(authority, "authority");
            Objects.requireNonNull(kind, "kind");
            if (!Double.isFinite(decorativeParticleDensity)
                    || decorativeParticleDensity < 0.0D
                    || decorativeParticleDensity > 1.0D) {
                throw new IllegalArgumentException("decorativeParticleDensity must be finite and within [0, 1]");
            }
        }

        public boolean authoritative() {
            return authority == CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT
                    || authority == CastPresentationLifecycle.Authority.SERVER_OWNED_RUNTIME_EVENT;
        }
    }

    private CastAudiovisualOrchestration() { }

    public static Directive plan(
            CastPresentationLifecycle.Cue cue,
            CastPresentationLifecycle.SensoryPolicy policy
    ) {
        Objects.requireNonNull(cue, "cue");
        Objects.requireNonNull(policy, "policy");
        Kind kind = switch (cue.state()) {
            case ANTICIPATING -> Kind.ANTICIPATION;
            case SUCCEEDED -> Kind.RESULT_SUCCESS;
            case DENIED -> Kind.RESULT_DENIED;
            case FAILED -> Kind.RESULT_FAILED;
        };
        return new Directive(
                cue.castId(),
                cue.spellId(),
                cue.authority(),
                kind,
                policy.particleDensity(),
                policy.nonessentialMotionAllowed(),
                policy.flashHeavyEffectsAllowed());
    }
}
