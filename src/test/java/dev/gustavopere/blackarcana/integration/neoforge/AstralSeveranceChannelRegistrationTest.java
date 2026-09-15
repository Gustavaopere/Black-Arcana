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
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralSeveranceChannelRegistrationTest {
    @Test
    void installPublishesExplicitChannelSpecIntoServerAuthority() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        ArcanaChannelSpec channelSpec = new ArcanaChannelSpec(3L, 17L);
        AstralSeveranceCastBinding.Profile profile = profile(channelSpec);

        AstralSeveranceCastBinding.install(
            runtime,
            profile,
            authorities(),
            (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.allow());

        assertEquals(
            channelSpec,
            runtime.channelSpecs().resolve(AstralSeveranceCastBinding.SPELL_ID).orElseThrow());
    }

    @Test
    void channelAuthorityConflictFailsBeforePublishingSpellCooldownOrEngine() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        ArcanaChannelSpec existing = new ArcanaChannelSpec(2L, 9L);
        ArcanaChannelSpec requested = new ArcanaChannelSpec(3L, 17L);
        assertTrue(runtime.channelSpecs().register(AstralSeveranceCastBinding.SPELL_ID, existing));

        assertThrows(IllegalStateException.class, () -> AstralSeveranceCastBinding.install(
            runtime,
            profile(requested),
            authorities(),
            (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.allow()));

        assertEquals(existing, runtime.channelSpecs().resolve(AstralSeveranceCastBinding.SPELL_ID).orElseThrow());
        assertTrue(runtime.spells().resolve(AstralSeveranceCastBinding.SPELL_ID).isEmpty());
        assertFalse(runtime.hasInstalledEngine(AstralSeveranceCastBinding.SPELL_ID));
        assertTrue(runtime.cooldownPolicies().cooldownSnapshot().get(AstralSeveranceCastBinding.SPELL_ID) == null);
    }

    private static AstralSeveranceCastBinding.Profile profile(ArcanaChannelSpec channelSpec) {
        return new AstralSeveranceCastBinding.Profile(
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
    }

    private static AstralSeveranceCastBinding.Authorities authorities() {
        return new AstralSeveranceCastBinding.Authorities(
            new TestResourceAuthority(),
            request -> ArcanaDecision.allow(),
            request -> ArcanaDecision.allow(),
            ArcanaServices.CastSuccessObserver.noop());
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
