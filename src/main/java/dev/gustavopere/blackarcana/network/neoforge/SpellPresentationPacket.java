package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.SpellPresentationPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.List;
import java.util.Objects;

public record SpellPresentationPacket(int protocolVersion, List<Entry> entries) implements CustomPacketPayload {
    private static final int MAX_SPELL_ID_LENGTH = 192;
    private static final int MAX_TRANSLATION_KEY_LENGTH = 160;
    private static final int MAX_ICON_ID_LENGTH = 192;

    public static final Type<SpellPresentationPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "spell_presentation"));

    private static final StreamCodec<ByteBuf, Entry> ENTRY_CODEC = StreamCodec.composite(
            ByteBufCodecs.stringUtf8(MAX_SPELL_ID_LENGTH), Entry::spellId,
            ByteBufCodecs.stringUtf8(MAX_TRANSLATION_KEY_LENGTH), Entry::translationKey,
            ByteBufCodecs.stringUtf8(MAX_ICON_ID_LENGTH), Entry::iconId,
            Entry::new);

    public static final StreamCodec<ByteBuf, SpellPresentationPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, SpellPresentationPacket::protocolVersion,
            ENTRY_CODEC.apply(ByteBufCodecs.list(ArcanaProtocol.MAX_PRESENTATION_ENTRIES)), SpellPresentationPacket::entries,
            SpellPresentationPacket::new);

    public SpellPresentationPacket {
        Objects.requireNonNull(entries, "entries");
        entries = List.copyOf(entries);
        toDomain(protocolVersion, entries);
    }

    public static SpellPresentationPacket from(SpellPresentationPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new SpellPresentationPacket(
                payload.protocolVersion(),
                payload.entries().stream()
                        .map(entry -> new Entry(entry.spellId(), entry.translationKey(), entry.iconId()))
                        .toList());
    }

    public SpellPresentationPayload toDomain() {
        return toDomain(protocolVersion, entries);
    }

    private static SpellPresentationPayload toDomain(int version, List<Entry> entries) {
        return new SpellPresentationPayload(
                version,
                entries.stream()
                        .map(entry -> new SpellPresentationPayload.Entry(entry.spellId(), entry.translationKey(), entry.iconId()))
                        .toList());
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }

    public record Entry(String spellId, String translationKey, String iconId) {
        public Entry {
            Objects.requireNonNull(spellId, "spellId");
            Objects.requireNonNull(translationKey, "translationKey");
            Objects.requireNonNull(iconId, "iconId");
            new SpellPresentationPayload.Entry(spellId, translationKey, iconId);
        }
    }
}
