package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.LoadoutUpdatePayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.List;
import java.util.Objects;

public record LoadoutUpdatePacket(int protocolVersion, List<String> spellIds) implements CustomPacketPayload {
    public static final Type<LoadoutUpdatePacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "loadout_update"));
    public static final StreamCodec<ByteBuf, LoadoutUpdatePacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, LoadoutUpdatePacket::protocolVersion,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESOURCE_ID_LENGTH)
                    .apply(ByteBufCodecs.list(ArcanaProtocol.MAX_LOADOUT_SLOTS)), LoadoutUpdatePacket::spellIds,
            LoadoutUpdatePacket::new);

    public LoadoutUpdatePacket {
        Objects.requireNonNull(spellIds, "spellIds");
        spellIds = List.copyOf(spellIds);
        new LoadoutUpdatePayload(protocolVersion, spellIds);
    }

    public static LoadoutUpdatePacket from(LoadoutUpdatePayload payload) {
        return new LoadoutUpdatePacket(payload.protocolVersion(), payload.spellIds());
    }

    public LoadoutUpdatePayload toDomain() {
        return new LoadoutUpdatePayload(protocolVersion, spellIds);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
