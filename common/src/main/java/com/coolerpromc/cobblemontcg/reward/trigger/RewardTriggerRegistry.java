package com.coolerpromc.cobblemontcg.reward.trigger;

import com.coolerpromc.cobblemontcg.Constants;
import net.minecraft.resources.ResourceLocation;

import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

/**
 * Triggers register themselves here, so integrations can add new ones without touching core code.
 */
public final class RewardTriggerRegistry {
    private static final Map<ResourceLocation, RewardTrigger> TRIGGERS = new LinkedHashMap<>();

    private RewardTriggerRegistry() {
    }

    public static synchronized <T extends RewardTrigger> T register(T trigger) {
        RewardTrigger previous = TRIGGERS.putIfAbsent(trigger.id(), trigger);
        if (previous != null) {
            throw new IllegalStateException("Duplicate reward trigger " + trigger.id());
        }
        Constants.LOG.debug("Registered reward trigger {}", trigger.id());
        return trigger;
    }

    public static Optional<RewardTrigger> get(ResourceLocation id) {
        return Optional.ofNullable(TRIGGERS.get(id));
    }

    public static Collection<RewardTrigger> all() {
        return Collections.unmodifiableCollection(TRIGGERS.values());
    }
}
