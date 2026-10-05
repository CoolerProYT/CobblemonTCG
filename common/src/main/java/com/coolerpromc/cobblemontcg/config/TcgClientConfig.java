package com.coolerpromc.cobblemontcg.config;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.coolerconfig.config.ConfigBuilder;
import com.coolerpromc.coolerconfig.config.ConfigFormat;
import com.coolerpromc.coolerconfig.config.ConfigSide;
import com.coolerpromc.coolerconfig.config.ConfigSpec;
import com.coolerpromc.coolerconfig.config.ConfigValue;

public class TcgClientConfig {
    public static ConfigSpec CONFIG_SPEC;

    private static ConfigValue<Boolean> animation;

    public static void init() {
        if (CONFIG_SPEC != null) {
            return;
        }
        Constants.LOG.info("Registering client config.");
        ConfigBuilder builder = ConfigSpec.builder(Constants.MODID, ConfigFormat.TOML).side(ConfigSide.CLIENT).watchForChanges();
        animation = builder.defineBoolean("packOpening.animation", true, "Show the pack opening animation and swipe through the cards one by one. When off, cards go straight to the inventory");
        CONFIG_SPEC = builder.build();
    }

    public static boolean animationEnabled() {
        return animation == null || animation.get();
    }
}
