package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class AstralSeveranceChannelRegistrationTest {
    @Test
    void installPublishesExplicitChannelSpecIntoServerAuthority() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        ArcanaChannelSpec channelSpec = new ArcanaChannelSpec(3L, 17L);
        AstralSeveranceCastBinding.Profile profile = new AstralSeveranceCastBinding.Profile(
            new ArcanaSpellDefinition(
                AstralSeveranceCastBinding.SPELL_ID,
                "spell.black_arcana.astral_severance",
                "black_arcana:textures/gui/spell_icons/astral_severance.png",
                new ArcanaCost("black_arcana:test_resource", 1.0D),
                false),
            new ArcanaCooldownSpec("black_arcana:test_astral", 1L, false),
            channelSpec,
            10,
            8.0D);

        AstralSeveranceCastBinding.install(
            runtime,
            profile,
            new AstralSeveranceCastBinding.Authorities(
                new TestResourceAuthority(),
                request -> ArcanaDecision.allow(),
                request -> ArcanaDecision.allow(),
                ArcanaServices.CastSuccessObserver.noop()),
            (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.allow());

        assertEquals(
            channelSpec,
            runtime.channelSpecs().resolve(AstralSeveranceCastBinding.SPELL_ID).orElseThrow());
    }

    private static final class TestResourceAuthority implements AstralSeveranceCastBinding.ResourceAuthority {
        @Override
        public String resourceId() {
            return "black_arcana:test_resource";
        }

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
    }
}
