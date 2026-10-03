package com.coolerpromc.cobblemontcg.reward;

import com.coolerpromc.cobblemontcg.reward.trigger.RewardTrigger;
import net.minecraft.resources.ResourceLocation;

import java.util.List;

/**
 * The loaded reward rules, and the dispatch from a fired trigger to {@link PackRewardService}.
 */
public final class RewardRules {
    private static volatile List<RewardRule> rules = List.of();

    private RewardRules() {
    }

    static void replace(List<RewardRule> newRules) {
        rules = List.copyOf(newRules);
    }

    public static List<RewardRule> all() {
        return rules;
    }

    public static List<RewardRule> forTrigger(ResourceLocation triggerId) {
        return rules.stream().filter(rule -> rule.trigger().equals(triggerId)).toList();
    }

    /**
     * Called by a {@link RewardTrigger} when its event happens.
     *
     * @return total packs granted
     */
    public static int fire(RewardTrigger trigger, RewardContext context) {
        int granted = 0;
        for (RewardRule rule : forTrigger(trigger.id())) {
            if (!rule.conditions().test(context)) {
                continue;
            }
            if (context.player().getRandom().nextFloat() >= rule.chance()) {
                continue;
            }
            granted += PackRewardService.grantPack(context.player(), rule.set(), rule.amount(), trigger.source());
        }
        return granted;
    }
}
