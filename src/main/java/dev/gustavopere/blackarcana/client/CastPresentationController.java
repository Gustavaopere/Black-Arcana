package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.CastResultPayload;

import java.util.Objects;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.Supplier;

/**
 * Provider-free Phase C controller that turns presentation lifecycle transitions into bounded
 * surface-neutral audiovisual directives.
 */
public final class CastPresentationController {
    private final CastPresentationLifecycle lifecycle;
    private final Supplier<CastPresentationLifecycle.SensoryPolicy> policySupplier;
    private final Consumer<CastAudiovisualOrchestration.Directive> sink;

    public CastPresentationController(
            int maxEntries,
            long staleAgeTicks,
            Supplier<CastPresentationLifecycle.SensoryPolicy> policySupplier,
            Consumer<CastAudiovisualOrchestration.Directive> sink
    ) {
        this.lifecycle = new CastPresentationLifecycle(maxEntries, staleAgeTicks);
        this.policySupplier = Objects.requireNonNull(policySupplier, "policySupplier");
        this.sink = Objects.requireNonNull(sink, "sink");
    }

    public Optional<CastAudiovisualOrchestration.Directive> recordLocalIntent(
            ArcanaCastId castId,
            ArcanaSpellId spellId,
            long tick
    ) {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spellId, "spellId");
        if (lifecycle.find(castId).isPresent()) return Optional.empty();
        return Optional.of(emit(lifecycle.recordLocalIntent(castId, spellId, tick)));
    }

    public Optional<CastAudiovisualOrchestration.Directive> acceptAuthoritativeResult(
            CastResultPayload payload,
            long tick
    ) {
        Objects.requireNonNull(payload, "payload");
        ArcanaCastId castId = ArcanaCastId.parse(payload.castId());
        Optional<CastPresentationLifecycle.Cue> existing = lifecycle.find(castId);
        if (existing.isPresent() && existing.orElseThrow().settled()) return Optional.empty();
        return Optional.of(emit(lifecycle.acceptAuthoritativeResult(payload, tick)));
    }

    public void evictStale(long currentTick) {
        lifecycle.evictStale(currentTick);
    }

    public int size() {
        return lifecycle.size();
    }

    public void clear() {
        lifecycle.clear();
    }

    private CastAudiovisualOrchestration.Directive emit(CastPresentationLifecycle.Cue cue) {
        CastPresentationLifecycle.SensoryPolicy policy = Objects.requireNonNull(
                policySupplier.get(), "sensory policy");
        CastAudiovisualOrchestration.Directive directive = CastAudiovisualOrchestration.plan(cue, policy);
        sink.accept(directive);
        return directive;
    }
}
