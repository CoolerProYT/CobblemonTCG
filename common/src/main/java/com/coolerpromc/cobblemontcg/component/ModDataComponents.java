package com.coolerpromc.cobblemontcg.component;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.component.custom.BoosterPackData;
import com.coolerpromc.cobblemontcg.component.custom.TcgCardData;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import net.minecraft.core.component.DataComponentType;

import java.util.function.UnaryOperator;

public class ModDataComponents {
    public static final RegistryHandler.Components<BoosterPackData> BOOSTER_PACK = register("booster_pack", b -> b.persistent(BoosterPackData.CODEC).networkSynchronized(BoosterPackData.STREAM_CODEC).cacheEncoding());
    public static final RegistryHandler.Components<TcgCardData> TCG_CARD = register("tcg_card", b -> b.persistent(TcgCardData.CODEC).networkSynchronized(TcgCardData.STREAM_CODEC).cacheEncoding());

    public static <T> RegistryHandler.Components<T> register(String name, UnaryOperator<DataComponentType.Builder<T>> unaryOperator){
        return Services.REGISTRY.registerDataComponent(name, unaryOperator);
    }

    public static void init(){
        Constants.LOG.info("Registering data components.");
    }
}
