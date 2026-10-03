package com.coolerpromc.cobblemontcg;

import com.coolerpromc.cobblemontcg.client.CardArtPatcher;
import com.coolerpromc.cobblemontcg.client.PackOpeningScreen;
import com.coolerpromc.cobblemontcg.client.cobblemon.CobblemonCardRenderer;
import com.coolerpromc.cobblemontcg.config.TcgClientConfig;
import com.coolerpromc.cobblemontcg.creativetab.ModCreativeTabs;
import com.coolerpromc.cobblemontcg.network.ClientPacketHooks;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import net.minecraft.client.Minecraft;
import net.minecraft.world.item.CreativeModeTab;

/**
 * Client-only setup, called from each loader's client entry point.
 */
public class CobblemonTCGClient {
    public static void init() {
        TcgClientConfig.init();
        TcgDataManager.CLIENT.addListener(CobblemonTCGClient::rebuildCreativeTab);
        ClientPacketHooks.packOpened = PackOpeningScreen::show;
        // draw Cobblemon's models into the card art instead of the built-in drawings
        CardArtPatcher.INSTANCE.setRenderer(CobblemonCardRenderer.create());
    }

    /**
     * Called at the end of every client tick by each loader.
     */
    public static void tick() {
        CardArtPatcher.INSTANCE.tick();
    }

    /**
     * The creative tab lists cards from synced data, which can arrive after the tab was first built.
     */
    private static void rebuildCreativeTab() {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null || minecraft.player == null) {
            return;
        }
        CreativeModeTab.ItemDisplayParameters parameters = new CreativeModeTab.ItemDisplayParameters(
                minecraft.level.enabledFeatures(),
                minecraft.player.canUseGameMasterBlocks() && minecraft.options.operatorItemsTab().get(),
                minecraft.level.registryAccess());
        ModCreativeTabs.TAB.get().buildContents(parameters);
    }
}
