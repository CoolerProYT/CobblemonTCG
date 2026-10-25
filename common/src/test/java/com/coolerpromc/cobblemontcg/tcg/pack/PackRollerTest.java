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

class PackRollerTest {
    private static final Path DATA = Path.of("src/main/resources/data/cobblemontcg/tcg");
    private static final int PACKS = 20_000;

    private static TcgSet base1;
    private static TcgSet base2;
    private static TcgSet basep;
    private static TcgSet base3;
    private static TcgSet base4;
    private static TcgSet base5;

    @BeforeAll
    static void loadSets() throws IOException {
        base1 = loadSet("base1");
        base2 = loadSet("base2");
        basep = loadSet("basep");
        base3 = loadSet("base3");
        base4 = loadSet("base4");
        base5 = loadSet("base5");
    }

    private static TcgSet loadSet(String name) throws IOException {
        SetDefinition definition = read(DATA.resolve("sets/" + name + ".json"), SetDefinition.CODEC);
        List<CardDefinition> cards;
        try (Stream<Path> files = Files.list(DATA.resolve("cards/" + name))) {
            cards = files.map(path -> read(path, CardDefinition.CODEC)).toList();
        }
        return new TcgSet(Constants.id(name), definition, cards);
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
    void jungleMatchesTheRealSetList() {
        assertEquals(64, base2.cards().size());
        assertEquals(16, base2.cardsOfRarity(CardRarity.RARE_HOLO).size());
        assertEquals(16, base2.cardsOfRarity(CardRarity.RARE).size());
        assertEquals(16, base2.cardsOfRarity(CardRarity.UNCOMMON).size());
        assertEquals(16, base2.cardsOfRarity(CardRarity.COMMON).size());
        assertEquals(11, base2.definition().packSize());
        assertEquals(List.of("scyther", "wigglytuff", "flareon"), base2.wrappers());
    }

    @Test
    void wizardsSetsMatchTheRealSetLists() {
        assertCounts(base3, 62, 15, 15, 16, 16);
        assertCounts(base4, 130, 20, 20, 42, 48);
        assertCounts(base5, 83, 18, 17, 24, 24);
        assertEquals(List.of("aerodactyl", "lapras", "gengar"), base3.wrappers());
        assertEquals(List.of("mewtwo", "gyarados", "ninetales"), base4.wrappers());
        assertEquals(List.of("dark_charizard", "dark_blastoise", "dark_dragonite"), base5.wrappers());
        RandomSource random = RandomSource.create(5L);
        for (TcgSet set : List.of(base3, base4, base5)) {
            for (int i = 0; i < PACKS / 4; i++) {
                List<RolledCard> pack = PackRoller.roll(set, random, 1.0 / 3.0, 11);
                assertEquals(11, pack.size());
                assertEquals(11, pack.stream().map(card -> card.card().number()).distinct().count(), "duplicate card in a " + set.definition().name() + " pack");
            }
        }
    }

    private static void assertCounts(TcgSet set, int total, int holo, int rare, int uncommon, int common) {
        String name = set.definition().name();
        assertEquals(total, set.cards().size(), name);
        assertEquals(total, set.definition().total(), name);
        assertEquals(holo, set.cardsOfRarity(CardRarity.RARE_HOLO).size(), name + " holo rares");
        assertEquals(rare, set.cardsOfRarity(CardRarity.RARE).size(), name + " rares");
        assertEquals(uncommon, set.cardsOfRarity(CardRarity.UNCOMMON).size(), name + " uncommons");
        assertEquals(common, set.cardsOfRarity(CardRarity.COMMON).size(), name + " commons");
        assertEquals(11, set.definition().packSize(), name);
    }

    @Test
    void promosFillEveryPackSlot() {
        assertEquals(53, basep.cards().size());
        assertEquals(11, basep.cardsOfRarity(CardRarity.RARE_HOLO).size());
        assertEquals(13, basep.cardsOfRarity(CardRarity.RARE).size());
        assertEquals(16, basep.cardsOfRarity(CardRarity.UNCOMMON).size());
        assertEquals(13, basep.cardsOfRarity(CardRarity.COMMON).size());
        assertEquals(List.of("pikachu", "mew", "hooh"), basep.wrappers());
        RandomSource random = RandomSource.create(3L);
        for (int i = 0; i < PACKS; i++) {
            List<RolledCard> pack = PackRoller.roll(basep, random, 1.0 / 3.0, 11);
            assertEquals(11, pack.size());
            assertEquals(11, pack.stream().map(card -> card.card().number()).distinct().count(), "duplicate card in a promo pack");
        }
    }

    @Test
    void setsUseSeparateModelDataRanges() {
        int base1Last = base1.modelData(base1.definition().total(), true);
        int base2First = base2.modelData(1, false);
        assertTrue(base1Last < base2First, "Jungle's custom_model_data range overlaps Base Set's");
        List<TcgSet> byRange = List.of(base1, base2, basep, base3, base4, base5);
        for (int i = 1; i < byRange.size(); i++) {
            TcgSet before = byRange.get(i - 1);
            TcgSet after = byRange.get(i);
            assertTrue(before.modelData(before.definition().total(), true) < after.modelData(1, false),
                    after.definition().name() + "'s custom_model_data range overlaps " + before.definition().name() + "'s");
        }
    }

    @Test
    void junglePacksHaveNoDuplicates() {
        RandomSource random = RandomSource.create(7L);
        for (int i = 0; i < PACKS; i++) {
            List<RolledCard> pack = PackRoller.roll(base2, random, 1.0 / 3.0, 11);
            assertEquals(11, pack.size());
            Set<Integer> numbers = new HashSet<>();
            for (RolledCard card : pack) {
                assertTrue(numbers.add(card.card().number()), "duplicate card in a Jungle pack");
            }
        }
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
