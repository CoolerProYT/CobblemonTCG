package com.coolerpromc.cobblemontcg.platform;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.network.HandledCustomPacketPayload;
import com.coolerpromc.cobblemontcg.platform.services.IRegistryHelper;
import com.coolerpromc.cobblemontcg.platform.util.CreativeTabOutput;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import com.google.common.collect.ImmutableSet;
import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.fabricmc.fabric.api.object.builder.v1.world.poi.PointOfInterestHelper;
import net.minecraft.core.Holder;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.entity.ai.village.poi.PoiType;
import net.minecraft.world.entity.npc.VillagerProfession;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import org.jetbrains.annotations.Nullable;

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
    public <T extends Block> RegistryHandler.Blocks<T> registerBlock(String name, Function<BlockBehaviour.Properties, T> func, BlockBehaviour.Properties p) {
        Holder<Block> holder = Registry.registerForHolder(BuiltInRegistries.BLOCK, Constants.id(name), func.apply(p));
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
    public RegistryHandler<PoiType, PoiType> registerPoiType(String name, Supplier<? extends Block> block, int maxTickets, int validRange) {
        // PointOfInterestHelper also fills the block state -> POI map, which vanilla keeps private
        PoiType poiType = PointOfInterestHelper.register(Constants.id(name), maxTickets, validRange, block.get());
        Holder<PoiType> holder = BuiltInRegistries.POINT_OF_INTEREST_TYPE.wrapAsHolder(poiType);
        return () -> holder;
    }

    @Override
    public RegistryHandler<VillagerProfession, VillagerProfession> registerVillagerProfession(String name, ResourceKey<PoiType> jobSite, @Nullable SoundEvent workSound) {
        ResourceLocation id = Constants.id(name);
        VillagerProfession profession = new VillagerProfession(id.toString(), poi -> poi.is(jobSite), poi -> poi.is(jobSite), ImmutableSet.of(), ImmutableSet.of(), workSound);
        Holder<VillagerProfession> holder = Registry.registerForHolder(BuiltInRegistries.VILLAGER_PROFESSION, id, profession);
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
