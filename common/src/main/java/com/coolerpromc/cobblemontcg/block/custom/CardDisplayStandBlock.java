package com.coolerpromc.cobblemontcg.block.custom;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.entity.CardDisplayStandBlockEntity;
import com.coolerpromc.cobblemontcg.menu.CardBinderMenu;
import com.coolerpromc.cobblemontcg.menu.CardStandBuyerMenu;
import com.coolerpromc.cobblemontcg.menu.CardStandOwnerMenu;
import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;
import org.jetbrains.annotations.Nullable;

import java.util.EnumMap;
import java.util.Map;

public class CardDisplayStandBlock extends HorizontalDirectionalBlock implements EntityBlock {
    public static final MapCodec<CardDisplayStandBlock> CODEC = simpleCodec(CardDisplayStandBlock::new);
    private static final String MESSAGE = "message." + Constants.MODID + ".card_display_stand.";

    private static final Map<Direction, VoxelShape> SHAPES = new EnumMap<>(Direction.class);

    static {
        for (Direction facing : Direction.Plane.HORIZONTAL) {
            SHAPES.put(facing, Shapes.or(Block.box(2, 0, 2, 14, 4, 14), CardDealerTableBlock.rotated(facing, 3.5, 4, 7.5, 12.5, 15.5, 14.5)));
        }
    }

    public CardDisplayStandBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH));
    }

    @Override
    protected MapCodec<? extends HorizontalDirectionalBlock> codec() {
        return CODEC;
    }

    @Override
    public @Nullable BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new CardDisplayStandBlockEntity(pos, state);
    }

    @Override
    public void setPlacedBy(Level level, BlockPos pos, BlockState state, @Nullable LivingEntity placer, ItemStack stack) {
        super.setPlacedBy(level, pos, state, placer, stack);
        if (!level.isClientSide() && placer instanceof Player player && level.getBlockEntity(pos) instanceof CardDisplayStandBlockEntity stand) {
            stand.setOwner(player);
        }
    }

    @Override
    protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hitResult) {
        if (!CardBinderMenu.isCard(stack) || !(level.getBlockEntity(pos) instanceof CardDisplayStandBlockEntity stand) || !stand.isOwner(player)) {
            return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
        }
        ItemStack shown = stand.card();
        if (!shown.isEmpty() && !ItemStack.isSameItemSameComponents(shown, stack)) {
            return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
        }
        if (!level.isClientSide()) {
            claim(stand, player);
            if (stand.placeCard(stack)) {
                level.playSound(null, pos, SoundEvents.BOOK_PAGE_TURN, SoundSource.BLOCKS, 1.0F, 1.2F);
            }
            openOwnerMenu(stand, player);
        }
        return ItemInteractionResult.sidedSuccess(level.isClientSide());
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hitResult) {
        if (!(level.getBlockEntity(pos) instanceof CardDisplayStandBlockEntity stand)) {
            return InteractionResult.PASS;
        }
        if (level.isClientSide()) {
            return InteractionResult.SUCCESS;
        }
        claim(stand, player);
        if (!stand.isOwner(player)) {
            player.openMenu(new SimpleMenuProvider((id, inventory, p) -> new CardStandBuyerMenu(id, inventory, stand),
                    Component.translatable("container." + Constants.MODID + ".card_display_stand.shop", stand.ownerName())));
        } else if (player.isSecondaryUseActive()) {
            if (stand.takeCard(player)) {
                level.playSound(null, pos, SoundEvents.ITEM_FRAME_REMOVE_ITEM, SoundSource.BLOCKS, 1.0F, 1.0F);
            }
        } else {
            openOwnerMenu(stand, player);
        }
        return InteractionResult.CONSUME;
    }

    private static void claim(CardDisplayStandBlockEntity stand, Player player) {
        if (!stand.hasOwner()) {
            stand.setOwner(player);
        }
    }

    private static void openOwnerMenu(CardDisplayStandBlockEntity stand, Player player) {
        player.openMenu(new SimpleMenuProvider((id, inventory, p) -> new CardStandOwnerMenu(id, inventory, stand),
                Component.translatable("container." + Constants.MODID + ".card_display_stand")));
    }

    public static boolean canBreak(BlockGetter level, BlockPos pos, Player player) {
        return !(level.getBlockEntity(pos) instanceof CardDisplayStandBlockEntity stand) || stand.canBreak(player);
    }

    public static void refuseBreak(Level level, BlockPos pos, Player player) {
        if (level.getBlockEntity(pos) instanceof CardDisplayStandBlockEntity stand) {
            player.displayClientMessage(Component.translatable(MESSAGE + "owned", stand.ownerName()), true);
        }
    }

    @Override
    protected float getDestroyProgress(BlockState state, Player player, BlockGetter level, BlockPos pos) {
        return canBreak(level, pos, player) ? super.getDestroyProgress(state, player, level, pos) : 0.0F;
    }

    @Override
    protected void attack(BlockState state, Level level, BlockPos pos, Player player) {
        if (!level.isClientSide() && !canBreak(level, pos, player)) {
            refuseBreak(level, pos, player);
        }
    }

    @Override
    protected void onRemove(BlockState state, Level level, BlockPos pos, BlockState newState, boolean movedByPiston) {
        if (!state.is(newState.getBlock()) && level.getBlockEntity(pos) instanceof CardDisplayStandBlockEntity stand) {
            stand.dropContents(level, pos);
        }
        super.onRemove(state, level, pos, newState, movedByPiston);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPES.get(state.getValue(FACING));
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        return defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING);
    }
}
