package com.coolerpromc.cobblemontcg.reward.trigger;

import com.coolerpromc.cobblemontcg.reward.PackSource;
import com.coolerpromc.cobblemontcg.reward.RewardContext;
import com.coolerpromc.cobblemontcg.reward.RewardRules;
import net.minecraft.resources.ResourceLocation;

public interface RewardTrigger {
    ResourceLocation id();

    PackSource source();

    default boolean enabled() {
        return true;
    }

    default int fire(RewardContext context) {
        return RewardRules.fire(this, context);
    }
}
