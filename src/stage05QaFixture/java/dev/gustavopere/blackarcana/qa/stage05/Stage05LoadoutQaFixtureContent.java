package dev.gustavopere.blackarcana.qa.stage05;

import com.mojang.logging.LogUtils;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.slf4j.Logger;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.IntStream;

/**
 * Removable Stage 05 QA content. These identities exist only to exercise the
 * canonical 16-slot server-owned loadout bound in a physical client.
 *
 * The spells intentionally deny execution before targeting/cost/effect work;
 * they are selection fixtures, not free gameplay spells.
 */
public final class Stage05LoadoutQaFixtureContent {
    private static final Logger LOGGER = LogUtils.getLogger();
    public static final String NAMESPACE = "black_arcana_stage05_qa";
    public static final List<ArcanaSpellId> SPELL_IDS = IntStream.rangeClosed(1, 16)
            .mapToObj(slot -> ArcanaSpellId.parse(NAMESPACE + ":slot_%02d".formatted(slot)))
            .toList();

    private Stage05LoadoutQaFixtureContent() { }

    public static void install(ArcanaServerRuntime runtime) {
        Objects.requireNonNull(runtime, "runtime");

        List<ArcanaSpellDefinition> definitions = new ArrayList<>(runtime.spells().snapshot().values());
        definitions.removeIf(definition -> SPELL_IDS.contains(definition.id()));
        for (ArcanaSpellId spellId : SPELL_IDS) {
            definitions.add(new ArcanaSpellDefinition(
                    spellId,
                    "spell." + NAMESPACE + "." + spellId.path(),
                    spellId.canonical(),
                    ArcanaCost.none(),
                    false));
        }
        runtime.spells().replaceAll(definitions);

        for (ArcanaSpellId spellId : SPELL_IDS) {
            runtime.installEngine(spellId, selectionOnlyEngine(runtime));
        }
        LOGGER.info("Black Arcana Stage 05 QA fixture installed {} server-authoritative selection-only spells", SPELL_IDS.size());
    }

    private static ArcanaCastEngine selectionOnlyEngine(ArcanaServerRuntime runtime) {
        return new ArcanaCastEngine(
                runtime.spells(),
                request -> ArcanaDecision.allow(),
                request -> ArcanaDecision.deny(
                        "stage05_qa_selection_only",
                        "Stage 05 QA loadout fixture spells are selection-only"),
                new ArcanaServices.CooldownService() {
                    @Override
                    public ArcanaDecision check(ArcanaCastRequest request) {
                        return ArcanaDecision.allow();
                    }

                    @Override
                    public void start(ArcanaCastRequest request) { }
                },
                request -> ArcanaServices.TargetResolution.denied("selection-only QA fixture"),
                new ArcanaServices.CostProvider() {
                    @Override
                    public ArcanaDecision check(ArcanaCastRequest request) {
                        return ArcanaDecision.allow();
                    }

                    @Override
                    public ArcanaServices.CostReservation reserve(ArcanaCastRequest request) {
                        return new ArcanaServices.CostReservation() {
                            @Override
                            public ArcanaDecision decision() {
                                return ArcanaDecision.allow();
                            }

                            @Override
                            public void commit() { }

                            @Override
                            public void refund() { }
                        };
                    }
                },
                (request, target) -> ArcanaDecision.deny(
                        "stage05_qa_selection_only",
                        "Stage 05 QA loadout fixture spells cannot mutate the world"),
                (request, target) -> ArcanaServices.EffectResult.failed(
                        "Stage 05 QA loadout fixture spells cannot execute"));
    }
}
