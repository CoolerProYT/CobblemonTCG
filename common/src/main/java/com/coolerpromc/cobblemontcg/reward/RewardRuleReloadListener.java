package com.coolerpromc.cobblemontcg.reward;

import com.coolerpromc.cobblemontcg.Constants;
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.mojang.serialization.JsonOps;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Loads reward rules from {@code tcg/rewards}. A file may hold one rule or a list of rules.
 */
public class RewardRuleReloadListener extends SimpleJsonResourceReloadListener {
    public static final ResourceLocation ID = Constants.id("tcg_rewards");

    public RewardRuleReloadListener() {
        super(new Gson(), "tcg/rewards");
    }

    @Override
    protected void apply(Map<ResourceLocation, JsonElement> files, ResourceManager resourceManager, ProfilerFiller profiler) {
        List<RewardRule> rules = new ArrayList<>();
        files.forEach((id, json) -> RewardRule.CODEC.listOf().parse(JsonOps.INSTANCE, json.isJsonArray() ? json : wrap(json))
                .resultOrPartial(error -> Constants.LOG.error("Failed to parse reward rule {}: {}", id, error))
                .ifPresent(rules::addAll));
        RewardRules.replace(rules);
        Constants.LOG.info("Loaded {} TCG reward rule(s)", rules.size());
    }

    private static JsonElement wrap(JsonElement json) {
        com.google.gson.JsonArray array = new com.google.gson.JsonArray();
        array.add(json);
        return array;
    }
}
