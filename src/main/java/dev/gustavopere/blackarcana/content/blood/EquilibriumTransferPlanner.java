package dev.gustavopere.blackarcana.content.blood;

/** Pure bounded health-transfer planner. It never creates health and never resurrects a dead endpoint. */
public final class EquilibriumTransferPlanner {
    private EquilibriumTransferPlanner() { }

    public static TransferPlan plan(
        double sourceHealth,
        double sourceMaxHealth,
        double targetHealth,
        double targetMaxHealth,
        double requestedTransfer,
        double sourceHealthFloor
    ) {
        validateHealth(sourceHealth, sourceMaxHealth, "source");
        validateHealth(targetHealth, targetMaxHealth, "target");
        if (!Double.isFinite(requestedTransfer) || requestedTransfer < 0.0D
            || requestedTransfer > BloodSafetyCeilings.MAX_EQUILIBRIUM_TRANSFER) {
            throw new IllegalArgumentException("requestedTransfer outside hard bounds");
        }
        if (!Double.isFinite(sourceHealthFloor) || sourceHealthFloor < 0.0D || sourceHealthFloor > sourceMaxHealth) {
            throw new IllegalArgumentException("sourceHealthFloor invalid");
        }
        if (sourceHealth <= 0.0D || targetHealth <= 0.0D) {
            return new TransferPlan(0.0D, sourceHealth, targetHealth, false);
        }

        double availableFromSource = Math.max(0.0D, sourceHealth - sourceHealthFloor);
        double capacityAtTarget = Math.max(0.0D, targetMaxHealth - targetHealth);
        double transfer = Math.min(requestedTransfer, Math.min(availableFromSource, capacityAtTarget));
        return new TransferPlan(transfer, sourceHealth - transfer, targetHealth + transfer, transfer > 0.0D);
    }

    private static void validateHealth(double health, double maxHealth, String field) {
        if (!Double.isFinite(health) || !Double.isFinite(maxHealth) || maxHealth <= 0.0D || health < 0.0D || health > maxHealth) {
            throw new IllegalArgumentException(field + " health values invalid");
        }
    }

    public record TransferPlan(double transferred, double sourceAfter, double targetAfter, boolean applicable) {
        public TransferPlan {
            if (!Double.isFinite(transferred) || transferred < 0.0D) throw new IllegalArgumentException("transferred invalid");
            if (!Double.isFinite(sourceAfter) || sourceAfter < 0.0D) throw new IllegalArgumentException("sourceAfter invalid");
            if (!Double.isFinite(targetAfter) || targetAfter < 0.0D) throw new IllegalArgumentException("targetAfter invalid");
        }
    }
}
