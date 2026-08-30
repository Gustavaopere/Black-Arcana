package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.forbidden.DomainReturnPoint;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainSafetyCeilings;
import dev.gustavopere.blackarcana.content.forbidden.InnerDominionSessionJournal;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.Tag;
import net.minecraft.world.level.saveddata.SavedData;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Persistent recovery snapshot for localized Inner Dominion sessions. */
public final class InnerDominionSavedData extends SavedData {
    public static final String DATA_NAME = "black_arcana_inner_dominion";
    private static final String SESSIONS = "sessions";
    private static final String SESSION_ID = "sessionId";
    private static final String OWNER_ID = "ownerId";
    private static final String EXPIRES_AT = "expiresAtTick";
    private static final String PARTICIPANTS = "participants";
    private static final String PLAYER_ID = "playerId";
    private static final String ORIGIN = "origin";
    private static final String FALLBACK = "fallback";
    private static final String DIMENSION = "dimension";
    private static final String X = "x";
    private static final String Y = "y";
    private static final String Z = "z";

    private List<InnerDominionSessionJournal.Session> sessions = List.of();

    public InnerDominionSavedData() { }

    public static SavedData.Factory<InnerDominionSavedData> factory() {
        return new SavedData.Factory<>(InnerDominionSavedData::new, InnerDominionSavedData::load, null);
    }

    private static InnerDominionSavedData load(CompoundTag tag, HolderLookup.Provider registries) {
        InnerDominionSavedData data = new InnerDominionSavedData();
        data.sessions = decode(tag);
        return data;
    }

    public List<InnerDominionSessionJournal.Session> sessions() {
        return List.copyOf(sessions);
    }

    public void replaceSessions(List<InnerDominionSessionJournal.Session> snapshots) {
        sessions = validateSnapshots(snapshots);
        setDirty();
    }

    @Override
    public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
        tag.put(SESSIONS, encodeSessions(sessions));
        return tag;
    }

    static CompoundTag encode(List<InnerDominionSessionJournal.Session> snapshots) {
        CompoundTag root = new CompoundTag();
        root.put(SESSIONS, encodeSessions(validateSnapshots(snapshots)));
        return root;
    }

    static List<InnerDominionSessionJournal.Session> decode(CompoundTag root) {
        Objects.requireNonNull(root, "root");
        ListTag encodedSessions = root.getList(SESSIONS, Tag.TAG_COMPOUND);
        if (encodedSessions.size() > ForbiddenDomainSafetyCeilings.MAX_ACTIVE_SESSIONS) {
            throw new IllegalArgumentException("Inner Dominion saved session count exceeds hard ceiling");
        }

        List<InnerDominionSessionJournal.Session> decoded = new ArrayList<>(encodedSessions.size());
        for (int i = 0; i < encodedSessions.size(); i++) {
            CompoundTag sessionTag = encodedSessions.getCompound(i);
            UUID sessionId = sessionTag.getUUID(SESSION_ID);
            UUID ownerId = sessionTag.getUUID(OWNER_ID);
            long expiresAtTick = sessionTag.getLong(EXPIRES_AT);
            ListTag encodedParticipants = sessionTag.getList(PARTICIPANTS, Tag.TAG_COMPOUND);
            if (encodedParticipants.isEmpty()
                    || encodedParticipants.size() > ForbiddenDomainSafetyCeilings.MAX_PARTICIPANTS) {
                throw new IllegalArgumentException("Inner Dominion saved participant count is outside hard ceiling");
            }

            Map<UUID, InnerDominionSessionJournal.ReturnRoute> participants = new LinkedHashMap<>();
            for (int participantIndex = 0; participantIndex < encodedParticipants.size(); participantIndex++) {
                CompoundTag participantTag = encodedParticipants.getCompound(participantIndex);
                UUID playerId = participantTag.getUUID(PLAYER_ID);
                InnerDominionSessionJournal.ReturnRoute previous = participants.put(
                    playerId,
                    new InnerDominionSessionJournal.ReturnRoute(
                        decodePoint(participantTag.getCompound(ORIGIN)),
                        decodePoint(participantTag.getCompound(FALLBACK))));
                if (previous != null) {
                    throw new IllegalArgumentException("Inner Dominion saved participant ids must be unique");
                }
            }
            decoded.add(new InnerDominionSessionJournal.Session(sessionId, ownerId, expiresAtTick, participants));
        }
        return validateSnapshots(decoded);
    }

    private static ListTag encodeSessions(List<InnerDominionSessionJournal.Session> snapshots) {
        ListTag encodedSessions = new ListTag();
        for (InnerDominionSessionJournal.Session session : snapshots) {
            CompoundTag sessionTag = new CompoundTag();
            sessionTag.putUUID(SESSION_ID, session.sessionId());
            sessionTag.putUUID(OWNER_ID, session.ownerId());
            sessionTag.putLong(EXPIRES_AT, session.expiresAtTick());

            ListTag encodedParticipants = new ListTag();
            for (Map.Entry<UUID, InnerDominionSessionJournal.ReturnRoute> entry : session.participants().entrySet()) {
                CompoundTag participantTag = new CompoundTag();
                participantTag.putUUID(PLAYER_ID, entry.getKey());
                participantTag.put(ORIGIN, encodePoint(entry.getValue().origin()));
                participantTag.put(FALLBACK, encodePoint(entry.getValue().fallback()));
                encodedParticipants.add(participantTag);
            }
            sessionTag.put(PARTICIPANTS, encodedParticipants);
            encodedSessions.add(sessionTag);
        }
        return encodedSessions;
    }

    private static CompoundTag encodePoint(DomainReturnPoint point) {
        CompoundTag tag = new CompoundTag();
        tag.putString(DIMENSION, point.dimensionId());
        tag.putDouble(X, point.x());
        tag.putDouble(Y, point.y());
        tag.putDouble(Z, point.z());
        return tag;
    }

    private static DomainReturnPoint decodePoint(CompoundTag tag) {
        return new DomainReturnPoint(
            tag.getString(DIMENSION),
            tag.getDouble(X),
            tag.getDouble(Y),
            tag.getDouble(Z));
    }

    private static List<InnerDominionSessionJournal.Session> validateSnapshots(
            List<InnerDominionSessionJournal.Session> snapshots
    ) {
        Objects.requireNonNull(snapshots, "snapshots");
        if (snapshots.size() > ForbiddenDomainSafetyCeilings.MAX_ACTIVE_SESSIONS) {
            throw new IllegalArgumentException("Inner Dominion snapshot count exceeds hard ceiling");
        }

        java.util.HashSet<UUID> sessionIds = new java.util.HashSet<>();
        java.util.HashSet<UUID> participantIds = new java.util.HashSet<>();
        List<InnerDominionSessionJournal.Session> copy = new ArrayList<>(snapshots.size());
        for (InnerDominionSessionJournal.Session session : snapshots) {
            Objects.requireNonNull(session, "session");
            if (!sessionIds.add(session.sessionId())) {
                throw new IllegalArgumentException("Inner Dominion snapshot session ids must be unique");
            }
            if (session.participants().isEmpty()
                    || session.participants().size() > ForbiddenDomainSafetyCeilings.MAX_PARTICIPANTS) {
                throw new IllegalArgumentException("Inner Dominion snapshot participant count is outside hard ceiling");
            }
            for (UUID participantId : session.participants().keySet()) {
                if (!participantIds.add(participantId)) {
                    throw new IllegalArgumentException("Inner Dominion snapshot participants cannot overlap sessions");
                }
            }
            copy.add(session);
        }
        return List.copyOf(copy);
    }
}
