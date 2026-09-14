package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.AstralMoveIntentPayload;
import dev.gustavopere.blackarcana.network.neoforge.AstralSeveranceNetworkBridge;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.Input;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.client.event.CalculatePlayerTurnEvent;
import net.neoforged.neoforge.client.event.MovementInputUpdateEvent;

import java.util.Objects;

/**
 * Physical-client movement/look redirect for an explicitly server-armed Astral Severance session.
 *
 * <p>Camera BEGIN alone never activates this controller. Only the exact-session MOVE_ARM state authored by
 * the server permits local movement and look input to be converted into bounded C2S intent. The client sends
 * axes, relative look deltas and sequence only; it never authors caster identity or a world position.</p>
 */
public final class AstralSeveranceInputController {
    private static final AstralControlIntentSequencer SEQUENCER = new AstralControlIntentSequencer();

    private AstralSeveranceInputController() { }

    public static void register(IEventBus gameBus) {
        IEventBus bus = Objects.requireNonNull(gameBus, "gameBus");
        bus.addListener(AstralSeveranceInputController::onMovementInput);
        bus.addListener(AstralSeveranceInputController::onCalculatePlayerTurn);
    }

    private static void onCalculatePlayerTurn(CalculatePlayerTurnEvent event) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null) {
            SEQUENCER.clear();
            return;
        }

        AstralViewClientState.Desired control = AstralSeveranceClientController.movementControl().orElse(null);
        if (control == null) {
            SEQUENCER.clear();
            return;
        }

        SEQUENCER.captureLook(
                control.projectionId(),
                minecraft.mouseHandler.getXVelocity(),
                minecraft.mouseHandler.getYVelocity(),
                event.getMouseSensitivity(),
                minecraft.options.invertYMouse().get());

        // Prevent the same mouse sample from rotating the authoritative physical body locally. The server
        // remains authoritative over the Astral projection because only bounded relative intent is sent.
        event.setMouseSensitivity(AstralControlIntentSequencer.PHYSICAL_BODY_NEUTRAL_SENSITIVITY);
        event.setCinematicCameraEnabled(false);
    }

    private static void onMovementInput(MovementInputUpdateEvent event) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || event.getEntity() != minecraft.player) {
            return;
        }

        AstralViewClientState.Desired control = AstralSeveranceClientController.movementControl().orElse(null);
        if (control == null) {
            SEQUENCER.clear();
            return;
        }

        Input input = event.getInput();
        double verticalAxis = (input.jumping ? 1.0D : 0.0D) - (input.shiftKeyDown ? 1.0D : 0.0D);
        AstralMoveIntentPayload payload = SEQUENCER.capture(
                control.projectionId(),
                input.leftImpulse,
                verticalAxis,
                input.forwardImpulse).orElse(null);

        suppressPhysicalBodyMovement(input);
        if (payload != null) {
            AstralSeveranceNetworkBridge.sendMove(payload);
        }
    }

    private static void suppressPhysicalBodyMovement(Input input) {
        input.leftImpulse = 0.0F;
        input.forwardImpulse = 0.0F;
        input.up = false;
        input.down = false;
        input.left = false;
        input.right = false;
        input.jumping = false;
        input.shiftKeyDown = false;
    }
}
