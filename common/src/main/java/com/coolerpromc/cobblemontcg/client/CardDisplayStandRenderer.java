package com.coolerpromc.cobblemontcg.client;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.custom.CardDisplayStandBlock;
import com.coolerpromc.cobblemontcg.block.entity.CardDisplayStandBlockEntity;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.ChatFormatting;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.renderer.entity.EntityRenderDispatcher;
import net.minecraft.client.renderer.entity.ItemRenderer;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import org.joml.Matrix4f;

import java.util.ArrayList;
import java.util.List;

public class CardDisplayStandRenderer implements BlockEntityRenderer<CardDisplayStandBlockEntity> {
    private static final String KEY = "screen." + Constants.MODID + ".card_display_stand.";
    private static final float BOARD_Y = 4.0F / 16.0F;
    private static final float BOARD_Z = 10.0F / 16.0F;
    private static final float BOARD_LEAN = 22.5F;
    private static final float CARD_SCALE = 0.68F;
    private static final float CARD_RISE = (1.0F + 8.0F * CARD_SCALE) / 16.0F;
    private static final float CARD_OFFSET = 1.2F / 16.0F;
    private static final float LABEL_SCALE = 0.02F;
    private static final double LABEL_DISTANCE_SQR = 8.0 * 8.0;

    public static boolean showLabel = true;

    private final ItemRenderer itemRenderer;
    private final EntityRenderDispatcher entityRenderer;
    private final Font font;

    public CardDisplayStandRenderer(BlockEntityRendererProvider.Context context) {
        this.itemRenderer = context.getItemRenderer();
        this.entityRenderer = context.getEntityRenderer();
        this.font = context.getFont();
    }

    @Override
    public void render(CardDisplayStandBlockEntity stand, float partialTick, PoseStack poseStack, MultiBufferSource buffer, int packedLight, int packedOverlay) {
        ItemStack card = stand.card();
        if (!card.isEmpty()) {
            Direction facing = stand.getBlockState().getValue(CardDisplayStandBlock.FACING);
            poseStack.pushPose();
            poseStack.translate(0.5F, 0.0F, 0.5F);
            poseStack.mulPose(Axis.YP.rotationDegrees(-(facing.toYRot() + 180.0F)));
            poseStack.translate(0.0F, BOARD_Y, BOARD_Z - 0.5F);
            poseStack.mulPose(Axis.XP.rotationDegrees(BOARD_LEAN));
            poseStack.translate(0.0F, CARD_RISE, -CARD_OFFSET);
            poseStack.scale(CARD_SCALE, CARD_SCALE, CARD_SCALE);
            itemRenderer.renderStatic(card, ItemDisplayContext.FIXED, packedLight, packedOverlay, poseStack, buffer, stand.getLevel(), (int) stand.getBlockPos().asLong());
            poseStack.popPose();
        }
        if (showLabel && isLookedAt(stand)) {
            renderLabel(stand, poseStack, buffer);
        }
    }

    private static boolean isLookedAt(CardDisplayStandBlockEntity stand) {
        Minecraft minecraft = Minecraft.getInstance();
        HitResult hit = minecraft.hitResult;
        return hit instanceof BlockHitResult blockHit && hit.getType() == HitResult.Type.BLOCK
                && blockHit.getBlockPos().equals(stand.getBlockPos())
                && minecraft.player != null && minecraft.player.distanceToSqr(stand.getBlockPos().getCenter()) < LABEL_DISTANCE_SQR;
    }

    private void renderLabel(CardDisplayStandBlockEntity stand, PoseStack poseStack, MultiBufferSource buffer) {
        List<Component> lines = new ArrayList<>();
        if (stand.card().isEmpty()) {
            lines.add(Component.translatable(KEY + "empty").withStyle(ChatFormatting.GRAY));
        } else {
            lines.add(stand.card().getHoverName().copy().withStyle(ChatFormatting.WHITE));
            lines.add(stand.isForSale()
                    ? Component.translatable(KEY + "price", stand.priceAmount(), stand.priceItem().getHoverName()).withStyle(ChatFormatting.GOLD)
                    : Component.translatable(KEY + "not_for_sale").withStyle(ChatFormatting.GRAY));
        }
        if (stand.hasOwner()) {
            lines.add(Component.translatable(KEY + "seller", stand.ownerName()).withStyle(ChatFormatting.DARK_GRAY));
        }

        poseStack.pushPose();
        poseStack.translate(0.5F, 1.25F + lines.size() * 0.2F, 0.5F);
        poseStack.mulPose(entityRenderer.cameraOrientation());
        poseStack.scale(LABEL_SCALE, -LABEL_SCALE, LABEL_SCALE);
        Matrix4f pose = poseStack.last().pose();
        int background = (int) (Minecraft.getInstance().options.getBackgroundOpacity(0.25F) * 255.0F) << 24;
        for (int i = 0; i < lines.size(); i++) {
            Component line = lines.get(i);
            font.drawInBatch(line, -font.width(line) / 2.0F, i * 10.0F, -1, false, pose, buffer, Font.DisplayMode.NORMAL, background, LightTexture.FULL_BRIGHT);
        }
        poseStack.popPose();
    }
}
