package com.coolerpromc.cobblemontcg;

import com.coolerpromc.cobblemontcg.creativetab.ModCreativeTabs;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import net.minecraft.client.Minecraft;
import net.minecraft.world.item.CreativeModeTab;

/**
 * Client-only setup, called from each loader's client entry point.
 */
public class CobblemonTCGClient {
    public static void init() {
        TcgDataManager.CLIENT.addListener(CobblemonTCGClient::rebuildCreativeTab);
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
