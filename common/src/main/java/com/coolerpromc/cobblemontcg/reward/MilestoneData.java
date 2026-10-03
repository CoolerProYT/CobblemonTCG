package com.coolerpromc.cobblemontcg.reward;

import com.mojang.serialization.Codec;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * The milestone ids (for example {@code cobblemontcg:level_up/level/10}) a player has already been rewarded for.
 */
public record MilestoneData(Set<String> claimed) {
    public static final MilestoneData EMPTY = new MilestoneData(Set.of());

    public static final Codec<MilestoneData> CODEC = Codec.STRING.listOf().xmap(
            list -> new MilestoneData(Set.copyOf(list)),
            data -> List.copyOf(data.claimed()));

    public MilestoneData {
        claimed = Set.copyOf(claimed);
    }

    public boolean isClaimed(String id) {
        return claimed.contains(id);
    }

    public MilestoneData with(Set<String> ids) {
        Set<String> merged = new HashSet<>(claimed);
        merged.addAll(ids);
        return new MilestoneData(merged);
    }
}
