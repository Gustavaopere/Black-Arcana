package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.content.noetic.BlackArcanaNoeticEntities;
import net.minecraft.client.renderer.entity.NoopRenderer;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Physical-client-only renderer registration for the invisible Astral viewpoint entity. */
public final class AstralProjectionClientRegistration {
    private AstralProjectionClientRegistration() {
    }

    public static void register(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(BlackArcanaNoeticEntities.ASTRAL_PROJECTION.get(), NoopRenderer::new);
    }
}
