package com.coolerpromc.cobblemontcg.platform;

import com.coolerpromc.cobblemontcg.platform.services.IPlatformHelper;
import net.neoforged.fml.loading.FMLLoader;

public class NeoForgePlatformHelper implements IPlatformHelper {
    @Override
    public String getPlatformName() {
        return "NeoForge";
    }

    @Override
    public boolean isDevelopmentEnvironment() {
        return !FMLLoader.isProduction();
    }
}
