package com.coolerpromc.cobblemontcg.menu;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import net.minecraft.world.inventory.MenuType;

public class ModMenuTypes {
    public static final RegistryHandler<MenuType<?>, MenuType<CardBinderMenu>> CARD_BINDER = Services.REGISTRY.registerMenuType("card_binder", CardBinderMenu::new);
    public static final RegistryHandler<MenuType<?>, MenuType<CardStandOwnerMenu>> CARD_STAND_OWNER = Services.REGISTRY.registerMenuType("card_stand_owner", CardStandOwnerMenu::new);
    public static final RegistryHandler<MenuType<?>, MenuType<CardStandBuyerMenu>> CARD_STAND_BUYER = Services.REGISTRY.registerMenuType("card_stand_buyer", CardStandBuyerMenu::new);

    public static void init(){
        Constants.LOG.info("Registering menu types.");
    }
}
