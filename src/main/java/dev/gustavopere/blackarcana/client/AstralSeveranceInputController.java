package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.AstralMoveIntentPayload;
import dev.gustavopere.blackarcana.network.neoforge.AstralSeveranceNetworkBridge;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.Input;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.client.event.MovementInputUpdateEvent;

import java.util.Objects;

/**
 * Physical-client movement redirect for an explicitly server-armed Astral Severance session.
 *
 * <p>Camera BEGIN alone never activates this controller. Only the exact-session MOVE_ARM state authored by
 * the server permits local movement input to be converted into bounded C2S intent. The client sends axes and
 * sequence only; it never authors caster identity or a world position. Look redirection is intentionally not
 * implemented here because Stage 07.07 still lacks a verified client hook for raw look deltas.</p>
 */
public final class AstralSeveranceInputController {
    private static final AstralMovementIntentSequencer SEQUENCER = new AstralMovementIntentSequencer();

    private AstralSeveranceInputController() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus").addListener(AstralSeveranceInputController::onMovementInput);
    }

    private static void onMovementInput(MovementInputUpdateEvent event) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || event.getEntity() != minecraft.player) {
            return;
        }

        AstralViewClientState.Desired control = AstralSeveranceClientController.movementControl().orElse(null);
        if (control == null) {
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
