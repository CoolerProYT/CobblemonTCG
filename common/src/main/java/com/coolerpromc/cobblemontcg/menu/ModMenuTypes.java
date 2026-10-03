package com.coolerpromc.cobblemontcg.menu;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import net.minecraft.world.inventory.MenuType;

public class ModMenuTypes {
    public static final RegistryHandler<MenuType<?>, MenuType<CardBinderMenu>> CARD_BINDER = Services.REGISTRY.registerMenuType("card_binder", CardBinderMenu::new);

    public static void init(){
        Constants.LOG.info("Registering menu types.");
    }
}
