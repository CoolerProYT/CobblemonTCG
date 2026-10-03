package com.coolerpromc.cobblemontcg.reward;

import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Optional;

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
        assertFalse(conditions.test(new RewardContext(null, Optional.empty(), Optional.of("pikachu"), Optional.of(true))), "unknown level fails");
        assertTrue(RewardConditions.NONE.test(new RewardContext(null, Optional.empty(), Optional.empty(), Optional.empty())));
    }

    @Test
    void rejectsAChanceAboveOne() {
        assertTrue(RewardRule.CODEC.listOf().parse(JsonOps.INSTANCE, JsonParser.parseString(
                "[{\"trigger\": \"a:b\", \"set\": \"a:c\", \"chance\": 2}]")).isError());
    }

    private static RewardContext context(int level, String species, boolean shiny) {
        return new RewardContext(null, Optional.of(level), Optional.of(species), Optional.of(shiny));
    }

    private static RewardRule parse(String json) {
        List<RewardRule> rules = RewardRule.CODEC.listOf().parse(JsonOps.INSTANCE, JsonParser.parseString("[" + json + "]")).getOrThrow();
        return rules.getFirst();
    }
}
