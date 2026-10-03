package com.coolerpromc.cobblemontcg.platform;

import com.coolerpromc.cobblemontcg.platform.services.IReloadListenerRegistrar;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.PreparableReloadListener;

import java.util.LinkedHashMap;
import java.util.Map;

public class FabricReloadListenerRegistrar implements IReloadListenerRegistrar {
    private final Map<ResourceLocation, PreparableReloadListener> serverReloadListeners = new LinkedHashMap<>();

    @Override
    public void registerServerReloadListener(ResourceLocation id, PreparableReloadListener listener) {
        this.serverReloadListeners.put(id, listener);
    }

    @Override
    public void applyServerReloadListenerRegistrations(ReloadListenerRegistrar registrar) {
        this.serverReloadListeners.forEach(registrar::register);
    }
}
