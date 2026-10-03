package com.coolerpromc.cobblemontcg.client.cobblemon;

import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.client.gui.PokemonGuiUtilsKt;
import com.cobblemon.mod.common.client.gui.ProfileTransformType;
import com.cobblemon.mod.common.client.render.models.blockbench.FloatingState;
import com.cobblemon.mod.common.entity.PoseType;
import com.cobblemon.mod.common.pokemon.Species;
import com.coolerpromc.cobblemontcg.client.CardArtPatcher;
import com.mojang.blaze3d.pipeline.TextureTarget;
import com.mojang.blaze3d.platform.NativeImage;
import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexSorting;
import net.minecraft.client.Minecraft;
import org.joml.Matrix4f;
import org.joml.Matrix4fStack;
import org.joml.Quaternionf;

import java.util.Optional;

/**
 * Draws Cobblemon's own Pokémon models for the card art, the way Cobblemon's Pokédex shows them.
 */
public final class CobblemonCardRenderer implements CardArtPatcher.PortraitRenderer {
    // the Pokédex portrait is 137 x 68 GUI units with the model at scale 2 and its origin 12 units above
    // the top; the canvas keeps that width and takes the height from the requested image's shape
    private static final float CANVAS_W = 137.0F;
    private static final float POKEDEX_H = 68.0F;
    private static final float MODEL_SCALE = 2.0F;
    private static final Quaternionf ROTATION = new Quaternionf().rotateXYZ((float) Math.toRadians(13), (float) Math.toRadians(35), 0);

    private CobblemonCardRenderer() {
    }

    public static CardArtPatcher.PortraitRenderer create() {
        return new CobblemonCardRenderer();
    }

    @Override
    public boolean ready() {
        return !PokemonSpecies.getImplemented().isEmpty();
    }

    @Override
    public Optional<NativeImage> render(int pokedex, int width, int height) {
        Species species = PokemonSpecies.getByPokedexNumber(pokedex, "cobblemon");
        if (species == null || !species.getImplemented()) {
            return Optional.empty();
        }

        Minecraft minecraft = Minecraft.getInstance();
        TextureTarget target = new TextureTarget(width, height, true, Minecraft.ON_OSX);
        Matrix4f oldProjection = new Matrix4f(RenderSystem.getProjectionMatrix());
        VertexSorting oldSorting = RenderSystem.getVertexSorting();
        Matrix4fStack modelView = RenderSystem.getModelViewStack();
        modelView.pushMatrix();
        try {
            target.setClearColor(0, 0, 0, 0);
            target.clear(Minecraft.ON_OSX);
            target.bindWrite(true);

            // same projection as the GUI, on a canvas the shape of the requested image
            float canvasH = CANVAS_W * height / width;
            RenderSystem.setProjectionMatrix(new Matrix4f().setOrtho(0, CANVAS_W, canvasH, 0, 1000, 21000), VertexSorting.ORTHOGRAPHIC_Z);
            modelView.identity().translate(0, 0, -11000);
            RenderSystem.applyModelViewMatrix();

            PoseStack pose = new PoseStack();
            // the model's profile origin, placed so the Pokédex framing sits in the middle of the canvas
            pose.translate(CANVAS_W / 2, (canvasH - POKEDEX_H) / 2 - 12, 1000);
            pose.scale(MODEL_SCALE, MODEL_SCALE, MODEL_SCALE);
            PokemonGuiUtilsKt.drawProfilePokemon(species.getResourceIdentifier(), pose, new Quaternionf(ROTATION), PoseType.PROFILE,
                    new FloatingState(), 0F, 20F, ProfileTransformType.POKEDEX, false, false,
                    1F, 1F, 1F, 1F, 0F, 0F, 15);

            NativeImage image = new NativeImage(width, height, false);
            RenderSystem.bindTexture(target.getColorTextureId());
            image.downloadTexture(0, false);
            image.flipY();
            return Optional.of(image);
        } finally {
            modelView.popMatrix();
            RenderSystem.applyModelViewMatrix();
            RenderSystem.setProjectionMatrix(oldProjection, oldSorting);
            target.destroyBuffers();
            minecraft.getMainRenderTarget().bindWrite(true);
        }
    }
}
