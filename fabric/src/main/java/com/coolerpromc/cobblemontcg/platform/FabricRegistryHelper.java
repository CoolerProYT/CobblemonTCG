package com.coolerpromc.cobblemontcg.platform;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.network.HandledCustomPacketPayload;
import com.coolerpromc.cobblemontcg.platform.services.IRegistryHelper;
import com.coolerpromc.cobblemontcg.platform.util.CreativeTabOutput;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.core.Holder;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

import java.util.ArrayList;
import java.util.List;
import java.util.function.BiConsumer;
import java.util.function.Function;
import java.util.function.Supplier;
import java.util.function.UnaryOperator;

public class FabricRegistryHelper implements IRegistryHelper {
    private final List<PayloadEntry<?>> clientboundPayloads = new ArrayList<>();

    @Override
    public <T extends Item> RegistryHandler.Items<T> registerItem(String name, Function<Item.Properties, T> func, Item.Properties p) {
        Holder<Item> holder = Registry.registerForHolder(BuiltInRegistries.ITEM, Constants.id(name), func.apply(p));
        return () -> holder;
    }

    @Override
    public <T> RegistryHandler.Components<T> registerDataComponent(String name, UnaryOperator<DataComponentType.Builder<T>> builder) {
        Holder<DataComponentType<?>> holder = Registry.registerForHolder(BuiltInRegistries.DATA_COMPONENT_TYPE, Constants.id(name), builder.apply(DataComponentType.builder()).build());
        return () -> holder;
    }

    @Override
    public RegistryHandler<SoundEvent, SoundEvent> registerSoundEvent(String name) {
        ResourceLocation id = Constants.id(name);
        Holder<SoundEvent> holder = Registry.registerForHolder(BuiltInRegistries.SOUND_EVENT, id, SoundEvent.createVariableRangeEvent(id));
        return () -> holder;
    }

    @Override
    public <T extends AbstractContainerMenu> RegistryHandler<MenuType<?>, MenuType<T>> registerMenuType(String name, MenuFactory<T> factory) {
        Holder<MenuType<?>> holder = Registry.registerForHolder(BuiltInRegistries.MENU, Constants.id(name), new MenuType<>(factory::create, FeatureFlags.VANILLA_SET));
        return () -> holder;
    }

    @Override
    public RegistryHandler<CreativeModeTab, CreativeModeTab> registerCreativeTab(String name, Supplier<ItemStack> icon, Component title, BiConsumer<CreativeTabOutput, CreativeModeTab.ItemDisplayParameters> entries) {
        Holder<CreativeModeTab> holder = Registry.registerForHolder(BuiltInRegistries.CREATIVE_MODE_TAB, Constants.id(name), FabricItemGroup.builder().icon(icon).title(title).displayItems((p, o) -> entries.accept(o::accept, p)).build());
        return () -> holder;
    }

    @Override
    public <T extends HandledCustomPacketPayload> void registerClientboundPayload(CustomPacketPayload.Type<T> type, StreamCodec<? super RegistryFriendlyByteBuf, T> streamCodec) {
        this.clientboundPayloads.add(new PayloadEntry<>(type, streamCodec));
    }

    @Override
    public void applyClientboundPayloadRegistrations(PayloadRegistrar registrar) {
        for (PayloadEntry<?> entry : clientboundPayloads) {
            entry.register(registrar);
        }
    }

    private record PayloadEntry<T extends HandledCustomPacketPayload>(CustomPacketPayload.Type<T> type, StreamCodec<? super RegistryFriendlyByteBuf, T> streamCodec){
        private void register(PayloadRegistrar registrar){
            registrar.register(this.type, this.streamCodec);
        }
    }
}
