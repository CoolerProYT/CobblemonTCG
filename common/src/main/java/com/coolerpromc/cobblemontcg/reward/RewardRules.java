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

    /**
     * Runs the rules of one trigger. A milestone rule is skipped when its milestone was claimed before this
     * call; otherwise the milestone is claimed as soon as the rule gets to roll its chance, win or lose, so it
     * never pays out twice. When no pack can be given (rewards off, unknown set, daily cap reached) the
     * milestone stays open for a later event.
     *
     * @param newlyClaimed receives the milestone ids to store
     * @return total packs granted
     */
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
