package com.coolerpromc.cobblemontcg.gametest;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.events.pokemon.PokemonCapturedEvent;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.experience.SidemodExperienceSource;
import com.cobblemon.mod.common.entity.pokeball.EmptyPokeBallEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.component.ModDataComponents;
import com.coolerpromc.cobblemontcg.component.custom.BoosterPackData;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.mojang.authlib.GameProfile;
import io.netty.channel.embedded.EmbeddedChannel;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.PacketFlow;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.server.network.CommonListenerCookie;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.neoforged.neoforge.network.registration.ChannelAttributes;
import net.neoforged.neoforge.network.registration.NetworkPayloadSetup;

import java.util.AbstractSet;
import java.util.Collections;
import java.util.Iterator;
import java.util.Set;
import java.util.UUID;

@GameTestHolder(Constants.MODID)
@PrefixGameTestTemplate(false)
public class PackRewardGameTests {
    private static final String EMPTY = "empty";
    private static final ResourceLocation BASE_SET = Constants.id("base1");
    private static final ResourceLocation JUNGLE = Constants.id("base2");
    private static int nextPlayer;

    @GameTest(template = EMPTY)
    public static void levelRewardsPayForEveryPokemonOnTheWayUp(GameTestHelper helper) {
        ServerPlayer player = mockPlayer(helper);
        Pokemon pikachu = give(player, "pikachu level=24");
        Pokemon bulbasaur = give(player, "bulbasaur level=24");
        check(helper, packs(player, BASE_SET) == 0, "no packs before levelling, got " + packs(player, BASE_SET));

        levelTo(pikachu, 25);
        check(helper, pikachu.getLevel() == 25, "pikachu should be level 25, is " + pikachu.getLevel());
        check(helper, packs(player, BASE_SET) == 1, "reaching level 25 pays 1 Base Set pack, got " + packs(player, BASE_SET));

        levelTo(bulbasaur, 25);
        check(helper, packs(player, BASE_SET) == 2, "a second Pokemon reaching 25 pays again, got " + packs(player, BASE_SET));

        levelTo(pikachu, 26);
        check(helper, packs(player, BASE_SET) == 2, "levelling past 25 does not pay again, got " + packs(player, BASE_SET));

        levelTo(pikachu, 50);
        check(helper, packs(player, JUNGLE) == 1, "reaching level 50 pays 1 Jungle pack, got " + packs(player, JUNGLE));
        helper.succeed();
    }

    @GameTest(template = EMPTY)
    public static void caughtHighLevelPokemonDoNotPayForLowerLevels(GameTestHelper helper) {
        ServerPlayer player = mockPlayer(helper);
        Pokemon pidgey = give(player, "pidgey level=40");
        levelTo(pidgey, 41);
        check(helper, totalPacks(player) == 0, "40 to 41 crosses no reward level, got " + totalPacks(player));
        helper.succeed();
    }

    @GameTest(template = EMPTY)
    public static void firstCatchIsDetectedAndShiniesAlwaysPay(GameTestHelper helper) {
        ServerPlayer player = mockPlayer(helper);
        String firstCatch = "cobblemontcg:capture/first_catch/charmander";

        capture(helper, player, "charmander level=5 shiny=yes");
        Set<String> claimed = Services.PLAYER_DATA.getMilestoneData(player).claimed();
        check(helper, claimed.contains(firstCatch), "the first charmander is a first catch, claimed " + claimed);
        int afterFirst = packs(player, BASE_SET);
        check(helper, afterFirst >= 1 && afterFirst <= 3, "a shiny catch pays 1 to 3 Base Set packs, got " + afterFirst);

        capture(helper, player, "charmander level=5 shiny=yes");
        int afterSecond = packs(player, BASE_SET);
        check(helper, afterSecond - afterFirst >= 1 && afterSecond - afterFirst <= 2, "a repeat shiny catch pays 1 or 2 packs, got " + (afterSecond - afterFirst));
        check(helper, Services.PLAYER_DATA.getMilestoneData(player).claimed().equals(claimed), "a repeat catch claims no new milestone");
        helper.succeed();
    }

    @GameTest(template = EMPTY)
    public static void jungleSpeciesGiveJunglePacks(GameTestHelper helper) {
        ServerPlayer player = mockPlayer(helper);
        capture(helper, player, "scyther level=5 shiny=yes");
        check(helper, packs(player, JUNGLE) >= 1, "a shiny Scyther pays Jungle packs, got " + packs(player, JUNGLE));
        check(helper, packs(player, BASE_SET) == 0, "and no Base Set packs, got " + packs(player, BASE_SET));
        helper.succeed();
    }

    @GameTest(template = EMPTY)
    public static void everyTenSpeciesOwnedPaysAPack(GameTestHelper helper) {
        ServerPlayer player = mockPlayer(helper);
        String[] species = {"bulbasaur", "charmander", "squirtle", "caterpie", "weedle", "pidgey", "rattata", "spearow", "ekans", "sandshrew"};
        for (int i = 0; i < species.length; i++) {
            give(player, species[i] + " level=5");
            int expected = i == species.length - 1 ? 1 : 0;
            check(helper, totalPacks(player) == expected, "after " + (i + 1) + " species expected " + expected + " pack(s), got " + totalPacks(player));
        }
        check(helper, packs(player, BASE_SET) == 1, "the 10th species pays a Base Set pack");
        helper.succeed();
    }

    @GameTest(template = EMPTY)
    public static void theDailyCapStopsRewardPacks(GameTestHelper helper) {
        ServerPlayer player = mockPlayer(helper);
        for (int i = 0; i < 12; i++) {
            capture(helper, player, "rattata level=5 shiny=yes");
        }
        check(helper, totalPacks(player) == 10, "12 shiny catches stop at the daily cap of 10, got " + totalPacks(player));
        helper.succeed();
    }

    private static ServerPlayer mockPlayer(GameTestHelper helper) {
        MinecraftServer server = helper.getLevel().getServer();
        CommonListenerCookie cookie = CommonListenerCookie.createInitial(new GameProfile(UUID.randomUUID(), "tcg-test-" + nextPlayer++), false);
        ServerPlayer player = new ServerPlayer(server, helper.getLevel(), cookie.gameProfile(), cookie.clientInformation());
        Connection connection = new Connection(PacketFlow.SERVERBOUND);
        new EmbeddedChannel(connection);
        ChannelAttributes.setPayloadSetup(connection, NetworkPayloadSetup.empty());
        connection.channel().attr(ChannelAttributes.ADHOC_CHANNELS).set(new AbstractSet<>() {
            @Override
            public boolean contains(Object o) {
                return true;
            }

            @Override
            public Iterator<ResourceLocation> iterator() {
                return Collections.emptyIterator();
            }

            @Override
            public int size() {
                return 0;
            }
        });
        server.getPlayerList().placeNewPlayer(connection, player, cookie);
        return player;
    }

    private static Pokemon give(ServerPlayer player, String properties) {
        Pokemon pokemon = PokemonProperties.Companion.parse(properties).create();
        Cobblemon.INSTANCE.getStorage().getParty(player).add(pokemon);
        return pokemon;
    }

    private static void capture(GameTestHelper helper, ServerPlayer player, String properties) {
        Pokemon pokemon = PokemonProperties.Companion.parse(properties).create();
        Cobblemon.INSTANCE.getStorage().getParty(player).add(pokemon);
        CobblemonEvents.POKEMON_CAPTURED.emit(new PokemonCapturedEvent(pokemon, player, new EmptyPokeBallEntity(helper.getLevel())));
    }

    private static void levelTo(Pokemon pokemon, int level) {
        pokemon.addExperience(new SidemodExperienceSource(Constants.MODID), pokemon.getExperienceToLevel(level));
    }

    private static int packs(ServerPlayer player, ResourceLocation set) {
        int count = 0;
        for (ItemStack stack : player.getInventory().items) {
            BoosterPackData data = stack.get(ModDataComponents.BOOSTER_PACK.get());
            if (data != null && data.setId().equals(set)) {
                count += stack.getCount();
            }
        }
        return count;
    }

    private static int totalPacks(ServerPlayer player) {
        return packs(player, BASE_SET) + packs(player, JUNGLE);
    }

    private static void check(GameTestHelper helper, boolean condition, String message) {
        if (!condition) {
            helper.fail(message);
        }
    }
}
