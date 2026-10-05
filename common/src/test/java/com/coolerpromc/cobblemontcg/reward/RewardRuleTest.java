package com.coolerpromc.cobblemontcg.reward;

import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class RewardRuleTest {
    @Test
    void dailyCountResetsOnANewDay() {
        DailyPackData data = DailyPackData.EMPTY.add(100, 3).add(100, 2);
        assertEquals(5, data.countOn(100));
        assertEquals(0, data.countOn(101));
        assertEquals(1, data.add(101, 1).countOn(101));
    }

    @Test
    void parsesARuleWithDefaults() {
        RewardRule rule = parse("{\"trigger\": \"cobblemontcg:capture\", \"set\": \"cobblemontcg:base1\"}");
        assertEquals(1, rule.amount());
        assertEquals(1.0F, rule.chance());
        assertEquals(RewardConditions.NONE, rule.conditions());
    }

    @Test
    void conditionsNeedTheContextToMatch() {
        RewardRule rule = parse("""
                {
                  "trigger": "cobblemontcg:capture",
                  "set": "cobblemontcg:base1",
                  "amount": 2,
                  "chance": 0.25,
                  "conditions": {"min_level": 20, "species": ["pikachu"], "shiny": true}
                }""");
        RewardConditions conditions = rule.conditions();
        assertTrue(conditions.test(context(25, "Pikachu", true)));
        assertFalse(conditions.test(context(10, "pikachu", true)), "level too low");
        assertFalse(conditions.test(context(25, "eevee", true)), "wrong species");
        assertFalse(conditions.test(context(25, "pikachu", false)), "not shiny");
        assertFalse(conditions.test(new RewardContext(null, Optional.empty(), Optional.of("pikachu"), Optional.of(true), Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty())), "unknown level fails");
        assertTrue(RewardConditions.NONE.test(RewardContext.of(null)));
    }

    @Test
    void rejectsAChanceAboveOne() {
        assertTrue(RewardRule.CODEC.listOf().parse(JsonOps.INSTANCE, JsonParser.parseString(
                "[{\"trigger\": \"a:b\", \"set\": \"a:c\", \"chance\": 2}]")).isError());
    }

    @Test
    void levelMilestonesAreReachedAtOrAboveTheLevel() {
        RewardConditions conditions = parse("{\"trigger\": \"a:b\", \"set\": \"a:c\", \"conditions\": {\"level\": 25}}").conditions();
        assertTrue(conditions.isMilestone());
        assertFalse(conditions.test(context(24, "eevee", false)));
        assertTrue(conditions.test(context(25, "eevee", false)));
        assertTrue(conditions.test(context(60, "eevee", false)));
        assertEquals(Optional.of("level/25"), conditions.milestone(context(60, "eevee", false)));
    }

    @Test
    void aLevelUpMustCrossTheLevel() {
        RewardConditions conditions = parse("{\"trigger\": \"a:b\", \"set\": \"a:c\", \"conditions\": {\"level\": 25}}").conditions();
        assertTrue(conditions.test(RewardContext.levelUp(null, "eevee", 24, 25, false)));
        assertTrue(conditions.test(RewardContext.levelUp(null, "eevee", 9, 30, false)), "a big jump crosses every level on the way");
        assertFalse(conditions.test(RewardContext.levelUp(null, "eevee", 25, 26, false)), "already past it");
        assertFalse(conditions.test(RewardContext.levelUp(null, "eevee", 40, 41, false)), "a high level catch levelling up");
        assertFalse(conditions.test(RewardContext.levelUp(null, "eevee", 23, 24, false)));
    }

    @Test
    void perPokemonLevelsPayForEveryPokemon() {
        ResourceLocation trigger = ResourceLocation.parse("cobblemontcg:level_up");
        List<RewardRule> rules = List.of(parse("{\"trigger\": \"cobblemontcg:level_up\", \"set\": \"a:c\", \"conditions\": {\"level\": 10, \"per_pokemon\": true}}"));
        assertFalse(rules.getFirst().conditions().isMilestone());

        Set<String> claimed = new HashSet<>();
        assertEquals(1, RewardRules.evaluate(trigger, rules, RewardContext.levelUp(null, "eevee", 9, 10, false), MilestoneData.EMPTY, claimed, rule -> true, () -> 0.0, RewardRule::amount));
        assertEquals(1, RewardRules.evaluate(trigger, rules, RewardContext.levelUp(null, "pikachu", 8, 11, false), MilestoneData.EMPTY, claimed, rule -> true, () -> 0.0, RewardRule::amount),
                "a second Pokemon reaching the level pays too");
        assertTrue(claimed.isEmpty(), "nothing to store, a Pokemon crosses a level only once");
        assertEquals(0, RewardRules.evaluate(trigger, rules, RewardContext.levelUp(null, "eevee", 10, 11, false), MilestoneData.EMPTY, claimed, rule -> true, () -> 0.0, RewardRule::amount));
    }

    @Test
    void shippedLevelRulesPayOnTheWayUp() throws Exception {
        ResourceLocation trigger = ResourceLocation.parse("cobblemontcg:level_up");
        List<RewardRule> rules = RewardRule.CODEC.listOf().parse(JsonOps.INSTANCE, JsonParser.parseString(java.nio.file.Files.readString(
                java.nio.file.Path.of("src/main/resources/data/cobblemontcg/tcg/rewards/level_up.json")))).getOrThrow();
        assertEquals(List.of(ResourceLocation.parse("cobblemontcg:base1")), paidSets(trigger, rules, RewardContext.levelUp(null, "eevee", 9, 10, false)));
        assertEquals(List.of(ResourceLocation.parse("cobblemontcg:base1")), paidSets(trigger, rules, RewardContext.levelUp(null, "pikachu", 9, 10, false)));
        assertEquals(List.of(), paidSets(trigger, rules, RewardContext.levelUp(null, "eevee", 11, 12, false)));
    }

    @Test
    void firstCatchMilestoneIsPerSpecies() {
        RewardConditions conditions = parse("{\"trigger\": \"a:b\", \"set\": \"a:c\", \"conditions\": {\"first_catch_of_species\": true}}").conditions();
        RewardContext first = RewardContext.capture(null, "Eevee", 5, false, true);
        assertTrue(conditions.test(first));
        assertFalse(conditions.test(RewardContext.capture(null, "eevee", 5, false, false)));
        assertEquals(Optional.of("first_catch/eevee"), conditions.milestone(first));

        RewardConditions shiny = parse("{\"trigger\": \"a:b\", \"set\": \"a:c\", \"conditions\": {\"shiny\": true}}").conditions();
        assertFalse(shiny.isMilestone(), "shiny catches pay every time");
    }

    @Test
    void dexMilestones() {
        RewardConditions every = parse("{\"trigger\": \"a:b\", \"set\": \"a:c\", \"conditions\": {\"dex_every\": 10}}").conditions();
        assertFalse(every.test(RewardContext.dexProgress(null, "eevee", 9, 1025)));
        assertTrue(every.test(RewardContext.dexProgress(null, "eevee", 30, 1025)));
        assertEquals(Optional.of("dex_every/10/30"), every.milestone(RewardContext.dexProgress(null, "eevee", 30, 1025)));
        // a multiple the daily cap held back is still open on the next species, under the same key
        assertTrue(every.test(RewardContext.dexProgress(null, "eevee", 31, 1025)));
        assertEquals(Optional.of("dex_every/10/30"), every.milestone(RewardContext.dexProgress(null, "eevee", 31, 1025)));

        RewardConditions quarter = parse("{\"trigger\": \"a:b\", \"set\": \"a:c\", \"conditions\": {\"dex_percent\": 25}}").conditions();
        assertFalse(quarter.test(RewardContext.dexProgress(null, "eevee", 24, 100)));
        assertTrue(quarter.test(RewardContext.dexProgress(null, "eevee", 25, 100)));
        assertTrue(quarter.test(RewardContext.dexProgress(null, "eevee", 90, 100)));
        assertFalse(quarter.test(RewardContext.dexProgress(null, "eevee", 5, 0)), "unknown total");
        assertTrue(RewardRule.CODEC.listOf().parse(JsonOps.INSTANCE, JsonParser.parseString(
                "[{\"trigger\": \"a:b\", \"set\": \"a:c\", \"conditions\": {\"dex_percent\": 101}}]")).isError());
    }

    @Test
    void milestonesPayOutOnce() {
        ResourceLocation trigger = ResourceLocation.parse("cobblemontcg:level_up");
        List<RewardRule> rules = List.of(
                parse("{\"trigger\": \"cobblemontcg:level_up\", \"set\": \"a:c\", \"conditions\": {\"level\": 10}}"),
                parse("{\"trigger\": \"cobblemontcg:level_up\", \"set\": \"a:c\", \"conditions\": {\"level\": 25}}"),
                parse("{\"trigger\": \"cobblemontcg:level_up\", \"set\": \"a:c\", \"amount\": 3}"));
        RewardContext context = context(30, "eevee", false);

        Set<String> claimed = new HashSet<>();
        int granted = RewardRules.evaluate(trigger, rules, context, MilestoneData.EMPTY, claimed, rule -> true, () -> 0.0, RewardRule::amount);
        assertEquals(5, granted, "both milestones and the repeatable rule");
        assertEquals(Set.of("cobblemontcg:level_up/level/10", "cobblemontcg:level_up/level/25"), claimed);

        Set<String> again = new HashSet<>();
        MilestoneData stored = MilestoneData.EMPTY.with(claimed);
        assertEquals(3, RewardRules.evaluate(trigger, rules, context, stored, again, rule -> true, () -> 0.0, RewardRule::amount),
                "only the repeatable rule pays again");
        assertTrue(again.isEmpty());
    }

    @Test
    void lostChanceRollStillClaimsButBlockedRewardDoesNot() {
        ResourceLocation trigger = ResourceLocation.parse("cobblemontcg:capture");
        List<RewardRule> rules = List.of(parse(
                "{\"trigger\": \"cobblemontcg:capture\", \"set\": \"a:c\", \"chance\": 0.1, \"conditions\": {\"first_catch_of_species\": true}}"));
        RewardContext context = RewardContext.capture(null, "eevee", 5, false, true);

        Set<String> claimed = new HashSet<>();
        assertEquals(0, RewardRules.evaluate(trigger, rules, context, MilestoneData.EMPTY, claimed, rule -> true, () -> 0.5, RewardRule::amount));
        assertEquals(Set.of("cobblemontcg:capture/first_catch/eevee"), claimed);

        Set<String> blocked = new HashSet<>();
        assertEquals(0, RewardRules.evaluate(trigger, rules, context, MilestoneData.EMPTY, blocked, rule -> false, () -> 0.0, RewardRule::amount));
        assertTrue(blocked.isEmpty(), "daily cap or rewards off keep the milestone open");
    }

    @Test
    void milestoneDataRoundTrips() {
        MilestoneData data = MilestoneData.EMPTY.with(Set.of("a:b/level/10", "a:b/dex_percent/25"));
        MilestoneData decoded = MilestoneData.CODEC.parse(JsonOps.INSTANCE, MilestoneData.CODEC.encodeStart(JsonOps.INSTANCE, data).getOrThrow()).getOrThrow();
        assertEquals(data, decoded);
    }

    @Test
    void shippedRulesParse() throws Exception {
        java.nio.file.Path dir = java.nio.file.Path.of("src/main/resources/data/cobblemontcg/tcg/rewards");
        int total = 0;
        try (var files = java.nio.file.Files.list(dir)) {
            for (java.nio.file.Path file : files.toList()) {
                List<RewardRule> rules = RewardRule.CODEC.listOf().parse(JsonOps.INSTANCE, JsonParser.parseString(java.nio.file.Files.readString(file))).getOrThrow();
                assertFalse(rules.isEmpty(), file.toString());
                total += rules.size();
            }
        }
        assertEquals(15, total);
    }

    @Test
    void excludedSpeciesDoNotMatch() {
        RewardConditions conditions = parse("{\"trigger\": \"a:b\", \"set\": \"a:c\", \"conditions\": {\"exclude_species\": [\"scyther\"]}}").conditions();
        assertFalse(conditions.test(context(5, "Scyther", false)));
        assertTrue(conditions.test(context(5, "pikachu", false)));
        assertTrue(conditions.test(RewardContext.of(null)), "no species, nothing to exclude");
    }

    @Test
    void jungleSpeciesGiveJunglePacksAndOthersBaseSet() throws Exception {
        ResourceLocation trigger = ResourceLocation.parse("cobblemontcg:capture");
        List<RewardRule> rules = RewardRule.CODEC.listOf().parse(JsonOps.INSTANCE, JsonParser.parseString(java.nio.file.Files.readString(
                java.nio.file.Path.of("src/main/resources/data/cobblemontcg/tcg/rewards/capture.json")))).getOrThrow();
        assertEquals(List.of(ResourceLocation.parse("cobblemontcg:base2"), ResourceLocation.parse("cobblemontcg:base2")), paidSets(trigger, rules, RewardContext.capture(null, "scyther", 5, false, true)));
        assertEquals(List.of(ResourceLocation.parse("cobblemontcg:base1"), ResourceLocation.parse("cobblemontcg:base1")), paidSets(trigger, rules, RewardContext.capture(null, "pikachu", 5, false, true)));
        assertEquals(List.of(ResourceLocation.parse("cobblemontcg:base1")), paidSets(trigger, rules, RewardContext.capture(null, "pikachu", 5, false, false)),
                "a repeat catch still has a chance");
        assertEquals(List.of(ResourceLocation.parse("cobblemontcg:base2"), ResourceLocation.parse("cobblemontcg:base2")), paidSets(trigger, rules, RewardContext.capture(null, "mrmime", 5, true, false)),
                "a shiny Jungle Pokemon pays Jungle packs");
        assertEquals(List.of(ResourceLocation.parse("cobblemontcg:base1"), ResourceLocation.parse("cobblemontcg:base1"), ResourceLocation.parse("cobblemontcg:base1")),
                paidSets(trigger, rules, RewardContext.capture(null, "charmander", 5, true, true)), "first shiny catch pays every Base Set rule");
    }

    private static List<ResourceLocation> paidSets(ResourceLocation trigger, List<RewardRule> rules, RewardContext context) {
        List<ResourceLocation> sets = new java.util.ArrayList<>();
        RewardRules.evaluate(trigger, rules, context, MilestoneData.EMPTY, new HashSet<>(), rule -> true, () -> 0.0, rule -> {
            sets.add(rule.set());
            return rule.amount();
        });
        return sets;
    }

    private static RewardContext context(int level, String species, boolean shiny) {
        return RewardContext.capture(null, species, level, shiny, false);
    }

    private static RewardRule parse(String json) {
        List<RewardRule> rules = RewardRule.CODEC.listOf().parse(JsonOps.INSTANCE, JsonParser.parseString("[" + json + "]")).getOrThrow();
        return rules.getFirst();
    }
}
