package com.coolerpromc.cobblemontcg.sound;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import net.minecraft.sounds.SoundEvent;

public class ModSounds {
    public static final RegistryHandler<SoundEvent, SoundEvent> BOOSTER_PACK_OPEN = register("item.booster_pack.open");
    public static final RegistryHandler<SoundEvent, SoundEvent> BOOSTER_PACK_OPEN_RARE = register("item.booster_pack.open_rare");

    public static RegistryHandler<SoundEvent, SoundEvent> register(String name){
        return Services.REGISTRY.registerSoundEvent(name);
    }

    public static void init(){
        Constants.LOG.info("Registering sounds.");
    }
}
