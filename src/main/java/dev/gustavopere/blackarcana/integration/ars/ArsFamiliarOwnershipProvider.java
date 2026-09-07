package dev.gustavopere.blackarcana.integration.ars;

import com.hollingsworth.arsnouveau.api.familiar.IFamiliar;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipProvider;

import java.util.Objects;
import java.util.UUID;

/** Ars Nouveau 5.13.1 familiar ownership adapter using only the public IFamiliar API. */
public final class ArsFamiliarOwnershipProvider implements FamiliarOwnershipProvider {
    @Override
    public String providerId() {
        return ArsIntegrationBridge.MOD_ID;
    }

    @Override
    public Result ownership(UUID ownerId, Object candidate) {
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(candidate, "candidate");
        if (!(candidate instanceof IFamiliar familiar)) return Result.NOT_OWNED;
        UUID actualOwner = familiar.getOwnerID();
        return ownerId.equals(actualOwner) ? Result.OWNED : Result.NOT_OWNED;
    }
}
