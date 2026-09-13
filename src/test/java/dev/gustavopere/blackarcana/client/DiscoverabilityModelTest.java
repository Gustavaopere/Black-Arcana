package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class DiscoverabilityModelTest {
    @Test
    void firstUseHintIsBoundedSeenOnceAndDoesNotRetriggerAfterExpiry() {
        var model = new DiscoverabilityModel(1, 160);

        var hint = model.offer(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                10L,
                true,
                bindings()).orElseThrow();

        assertEquals(DiscoverabilityModel.Topic.CORE_CASTING, hint.topic());
        assertEquals(10L, hint.startedTick());
        assertEquals(170L, hint.expiresAtTick());
        assertEquals(1, model.activeCount(10L));
        assertTrue(model.offer(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                20L,
                true,
                bindings()).isEmpty());
        assertTrue(model.active(169L).isPresent());
        assertTrue(model.active(170L).isEmpty());
        assertEquals(0, model.activeCount(170L));
        assertTrue(model.offer(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                171L,
                true,
                bindings()).isEmpty());
    }

    @Test
    void higherPriorityHintReplacesLowerPriorityWithoutGrowingTheActiveSet() {
        var model = new DiscoverabilityModel(1, 160);
        model.offer(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                10L,
                true,
                bindings()).orElseThrow();

        var required = model.offer(
                DiscoverabilityModel.Topic.UNBOUND_EDITOR,
                DiscoverabilityModel.Priority.REQUIRED,
                11L,
                true,
                bindings()).orElseThrow();

        assertEquals(DiscoverabilityModel.Topic.UNBOUND_EDITOR, required.topic());
        assertEquals(1, model.activeCount(11L));
        assertEquals(DiscoverabilityModel.Topic.UNBOUND_EDITOR, model.active(11L).orElseThrow().topic());
    }

    @Test
    void dismissedTopicDoesNotRetriggerButExplicitReentryStillWorks() {
        var model = new DiscoverabilityModel(1, 160);
        model.offer(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                10L,
                true,
                bindings()).orElseThrow();

        model.dismiss(DiscoverabilityModel.Topic.CORE_CASTING);

        assertTrue(model.active(11L).isEmpty());
        assertTrue(model.offer(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                12L,
                true,
                bindings()).isEmpty());

        var reopened = model.reopen(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                13L,
                bindings()).orElseThrow();
        assertEquals(DiscoverabilityModel.Topic.CORE_CASTING, reopened.topic());
        assertEquals(1, model.activeCount(13L));
    }

    @Test
    void sessionResetAllowsFirstUseAgainWithoutPersistingGameplayState() {
        var model = new DiscoverabilityModel(1, 160);
        model.offer(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                10L,
                true,
                bindings()).orElseThrow();
        model.dismiss(DiscoverabilityModel.Topic.CORE_CASTING);

        model.resetSession();

        assertFalse(model.hasSeen(DiscoverabilityModel.Topic.CORE_CASTING));
        assertFalse(model.isDismissed(DiscoverabilityModel.Topic.CORE_CASTING));
        assertTrue(model.offer(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                20L,
                true,
                bindings()).isPresent());
    }

    @Test
    void disabledHintsSuppressOptionalOffersButNeverBlockExplicitHelpReentry() {
        var model = new DiscoverabilityModel(1, 160);

        assertTrue(model.offer(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                10L,
                false,
                bindings()).isEmpty());
        assertFalse(model.hasSeen(DiscoverabilityModel.Topic.CORE_CASTING));

        assertTrue(model.reopen(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                11L,
                bindings()).isPresent());
    }

    private static DiscoverabilityModel.BindingSnapshot bindings() {
        return new DiscoverabilityModel.BindingSnapshot(
                DiscoverabilityModel.BindingPresentation.bound("key.black_arcana.open_radial", "G"),
                DiscoverabilityModel.BindingPresentation.bound("key.black_arcana.cast_selected", "Mouse 5"),
                DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.edit_loadout"),
                List.of(
                        DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_1"),
                        DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_2"),
                        DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_3"),
                        DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_4"),
                        DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_5"),
                        DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_6"),
                        DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_7"),
                        DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_8")));
    }
}
