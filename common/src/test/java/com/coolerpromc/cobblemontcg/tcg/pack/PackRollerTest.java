package com.coolerpromc.cobblemontcg.tcg.pack;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.card.CardRarity;
import com.coolerpromc.cobblemontcg.tcg.set.SetDefinition;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.google.gson.JsonParser;
import com.mojang.serialization.Codec;
import com.mojang.serialization.JsonOps;
import net.minecraft.util.RandomSource;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Rolls packs from the real Base Set data shipped in src/main/resources.
 */
class PackRollerTest {
    private static final Path DATA = Path.of("src/main/resources/data/cobblemontcg/tcg");
    private static final int PACKS = 20_000;

    private static TcgSet base1;

    @BeforeAll
    static void loadBaseSet() throws IOException {
        SetDefinition definition = read(DATA.resolve("sets/base1.json"), SetDefinition.CODEC);
        List<CardDefinition> cards;
        try (Stream<Path> files = Files.list(DATA.resolve("cards/base1"))) {
            cards = files.map(path -> read(path, CardDefinition.CODEC)).toList();
        }
        base1 = new TcgSet(Constants.id("base1"), definition, cards);
    }

    @Test
    void baseSetMatchesTheRealSetList() {
        assertEquals(102, base1.cards().size());
        assertEquals(16, base1.cardsOfRarity(CardRarity.RARE_HOLO).size());
        assertEquals(16, base1.cardsOfRarity(CardRarity.RARE).size());
        assertEquals(32, base1.cardsOfRarity(CardRarity.UNCOMMON).size());
        assertEquals(38, base1.cardsOfRarity(CardRarity.COMMON).size());
        assertEquals(11, base1.definition().packSize());
    }

    @Test
    void everyPackHasElevenCardsInSlotOrder() {
        RandomSource random = RandomSource.create(1L);
        for (int i = 0; i < PACKS; i++) {
            List<RolledCard> pack = PackRoller.roll(base1, random, 1.0 / 3.0, 11);
            assertEquals(11, pack.size());

            CardRarity rareSlot = pack.getFirst().card().rarity();
            assertTrue(rareSlot == CardRarity.RARE || rareSlot == CardRarity.RARE_HOLO, "slot 1 must be a rare, was " + rareSlot);
            for (int n = 1; n <= 3; n++) {
                assertEquals(CardRarity.UNCOMMON, pack.get(n).card().rarity(), "slots 2-4 must be uncommon");
            }
            for (int n = 4; n < 11; n++) {
                assertEquals(CardRarity.COMMON, pack.get(n).card().rarity(), "slots 5-11 must be common");
            }
        }
    }

    @Test
    void noDuplicateCardInAPack() {
        RandomSource random = RandomSource.create(2L);
        for (int i = 0; i < PACKS; i++) {
            List<RolledCard> pack = PackRoller.roll(base1, random, 1.0 / 3.0, 11);
            Set<Integer> numbers = new HashSet<>();
            for (RolledCard card : pack) {
                assertTrue(numbers.add(card.card().number()), "duplicate card " + card.card().number());
            }
        }
    }

    @Test
    void holoRateFollowsTheConfiguredChance() {
        RandomSource random = RandomSource.create(3L);
        int holos = 0;
        for (int i = 0; i < PACKS; i++) {
            List<RolledCard> pack = PackRoller.roll(base1, random, 1.0 / 3.0, 11);
            long count = pack.stream().filter(RolledCard::holo).count();
            assertTrue(count <= 1, "at most one holo per pack");
            assertEquals(count == 1, pack.getFirst().holo(), "only the rare slot can be holo");
            holos += (int) count;
        }
        double rate = holos / (double) PACKS;
        assertEquals(1.0 / 3.0, rate, 0.015, "holo rate was " + rate);
    }

    @Test
    void holoChanceZeroAndOne() {
        RandomSource random = RandomSource.create(4L);
        for (int i = 0; i < 2_000; i++) {
            assertFalse(PackRoller.roll(base1, random, 0.0, 11).getFirst().holo());
            assertTrue(PackRoller.roll(base1, random, 1.0, 11).getFirst().holo());
        }
    }

    @Test
    void packSizeChangesTheLastSlots() {
        RandomSource random = RandomSource.create(5L);
        List<RolledCard> small = PackRoller.roll(base1, random, 1.0 / 3.0, 9);
        assertEquals(9, small.size());
        assertEquals(5, small.stream().filter(c -> c.card().rarity() == CardRarity.COMMON).count());

        List<RolledCard> large = PackRoller.roll(base1, random, 1.0 / 3.0, 14);
        assertEquals(14, large.size());
        assertEquals(10, large.stream().filter(c -> c.card().rarity() == CardRarity.COMMON).count());

        List<RolledCard> one = PackRoller.roll(base1, random, 1.0 / 3.0, 1);
        assertEquals(1, one.size());
        assertNotEquals(CardRarity.COMMON, one.getFirst().card().rarity());
    }

    private static <T> T read(Path path, Codec<T> codec) {
        try (Reader reader = Files.newBufferedReader(path)) {
            return codec.parse(JsonOps.INSTANCE, JsonParser.parseReader(reader)).getOrThrow();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
