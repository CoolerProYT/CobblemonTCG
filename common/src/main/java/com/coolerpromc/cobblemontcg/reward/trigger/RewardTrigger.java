package com.coolerpromc.cobblemontcg.reward.trigger;

import com.coolerpromc.cobblemontcg.reward.PackSource;
import com.coolerpromc.cobblemontcg.reward.RewardContext;
import com.coolerpromc.cobblemontcg.reward.RewardRules;
import net.minecraft.resources.ResourceLocation;

/**
 * A game event that can hand out booster packs. Implementations hook into their event however they
 * like and call {@link #fire} when it happens; reward rules refer to them by {@link #id()}.
 */
public interface RewardTrigger {
    ResourceLocation id();

    PackSource source();

    default int fire(RewardContext context) {
        return RewardRules.fire(this, context);
    }
}
