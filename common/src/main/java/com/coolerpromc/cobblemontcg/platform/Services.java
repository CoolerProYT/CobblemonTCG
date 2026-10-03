package com.coolerpromc.cobblemontcg.platform;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.platform.services.*;

import java.util.ServiceLoader;

public class Services {
    public static final IPlatformHelper PLATFORM = load(IPlatformHelper.class);
    public static final IRegistryHelper REGISTRY = load(IRegistryHelper.class);
    public static final IReloadListenerRegistrar RELOAD_LISTENERS = load(IReloadListenerRegistrar.class);
    public static final IPlayerDataHelper PLAYER_DATA = load(IPlayerDataHelper.class);
    public static final INetworkHelper NETWORK = load(INetworkHelper.class);
    public static final IVillagerTradeRegistrar VILLAGER_TRADES = load(IVillagerTradeRegistrar.class);

    public static <T> T load(Class<T> clazz) {
        final T loadedService = ServiceLoader.load(clazz, Services.class.getClassLoader())
                .findFirst()
                .orElseThrow(() -> new NullPointerException("Failed to load service for " + clazz.getName()));
        Constants.LOG.debug("Loaded {} for service {}", loadedService, clazz);
        return loadedService;
    }
}
