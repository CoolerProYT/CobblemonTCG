package com.coolerpromc.cobblemontcg.reward;

import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.reward.trigger.RewardTrigger;
import net.minecraft.resources.ResourceLocation;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.DoubleSupplier;
import java.util.function.Predicate;
import java.util.function.ToIntFunction;

public class RewardRules {
    private static volatile List<RewardRule> rules = List.of();

    static void replace(List<RewardRule> newRules) {
        rules = List.copyOf(newRules);
    }

    public static List<RewardRule> all() {
        return rules;
    }

    public static List<RewardRule> forTrigger(ResourceLocation triggerId) {
        return rules.stream().filter(rule -> rule.trigger().equals(triggerId)).toList();
    }

    public static int fire(RewardTrigger trigger, RewardContext context) {
        if (!trigger.enabled()) {
            return 0;
        }
        List<RewardRule> matching = forTrigger(trigger.id());
        if (matching.isEmpty()) {
            return 0;
        }
        MilestoneData milestones = Services.PLAYER_DATA.getMilestoneData(context.player());
        Set<String> newlyClaimed = new HashSet<>();
        int granted = evaluate(trigger.id(), matching, context, milestones, newlyClaimed,
                rule -> PackRewardService.canReward(context.player(), rule.set()),
                () -> context.player().getRandom().nextFloat(),
                rule -> PackRewardService.grantPack(context.player(), rule.set(), rule.amount(), trigger.source()));
        if (!newlyClaimed.isEmpty()) {
            Services.PLAYER_DATA.setMilestoneData(context.player(), milestones.with(newlyClaimed));
        }
        return granted;
    }

    static int evaluate(ResourceLocation triggerId, List<RewardRule> rules, RewardContext context, MilestoneData claimed,
                        Set<String> newlyClaimed, Predicate<RewardRule> canReward, DoubleSupplier random, ToIntFunction<RewardRule> grant) {
        int granted = 0;
        for (RewardRule rule : rules) {
            if (!rule.conditions().test(context)) {
                continue;
            }
            String milestone = rule.conditions().milestone(context).map(key -> triggerId + "/" + key).orElse(null);
            if (milestone != null && claimed.isClaimed(milestone)) {
                continue;
            }
            if (!canReward.test(rule)) {
                continue;
            }
            if (milestone != null) {
                newlyClaimed.add(milestone);
            }
            if (random.getAsDouble() >= rule.chance()) {
                continue;
            }
            granted += grant.applyAsInt(rule);
        }
        return granted;
    }
}
