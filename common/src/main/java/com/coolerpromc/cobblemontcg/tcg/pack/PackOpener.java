package com.coolerpromc.cobblemontcg.tcg.pack;

import com.coolerpromc.cobblemontcg.config.TcgConfig;
import com.coolerpromc.cobblemontcg.network.ClientboundPackOpenedPacket;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.reward.PackRewardService;
import com.coolerpromc.cobblemontcg.sound.ModSounds;
import com.coolerpromc.cobblemontcg.tcg.card.CardRarity;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.coolerpromc.cobblemontcg.util.TcgStacks;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;

import java.util.List;

public class PackOpener {
    public static List<RolledCard> open(ServerPlayer player, TcgSet set, String wrapper) {
        List<RolledCard> cards = PackRoller.roll(set, player.getRandom(), TcgConfig.holoChance(), TcgConfig.packSize());
        for (RolledCard rolled : cards) {
            PackRewardService.giveOrDrop(player, TcgStacks.card(set, rolled.card().number(), rolled.holo()));
        }
        playEffects(player, cards.stream().anyMatch(RolledCard::holo), cards.stream().anyMatch(c -> c.card().rarity() == CardRarity.RARE));

        List<ClientboundPackOpenedPacket.Pull> pulls = cards.stream().map(c -> new ClientboundPackOpenedPacket.Pull(c.card().number(), c.holo())).toList();
        Services.NETWORK.sendToPlayer(player, new ClientboundPackOpenedPacket(set.id(), wrapper, pulls, TcgConfig.soundsEnabled()));
        return cards;
    }

    private static void playEffects(ServerPlayer player, boolean holo, boolean rare) {
        ServerLevel level = player.serverLevel();
        double x = player.getX();
        double y = player.getY() + player.getBbHeight() * 0.6;
        double z = player.getZ();

        if (TcgConfig.soundsEnabled()) {
            SoundEvent sound = holo ? ModSounds.BOOSTER_PACK_OPEN_RARE.get() : ModSounds.BOOSTER_PACK_OPEN.get();
            level.playSound(player, x, y, z, sound, SoundSource.PLAYERS, 1.0F, 0.9F + level.getRandom().nextFloat() * 0.2F);
        }

        level.sendParticles(ParticleTypes.ENCHANT, x, y, z, 24, 0.4, 0.4, 0.4, 0.6);
        if (holo) {
            level.sendParticles(ParticleTypes.END_ROD, x, y, z, 20, 0.3, 0.4, 0.3, 0.08);
        } else if (rare) {
            level.sendParticles(ParticleTypes.HAPPY_VILLAGER, x, y, z, 8, 0.4, 0.3, 0.4, 0.0);
        }
    }
}
