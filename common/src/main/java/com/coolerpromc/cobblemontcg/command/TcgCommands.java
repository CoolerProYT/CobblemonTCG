package com.coolerpromc.cobblemontcg.command;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.reward.PackRewardService;
import com.coolerpromc.cobblemontcg.reward.PackSource;
import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.coolerpromc.cobblemontcg.util.TcgStacks;
import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.BoolArgumentType;
import com.mojang.brigadier.arguments.IntegerArgumentType;
import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.exceptions.CommandSyntaxException;
import com.mojang.brigadier.exceptions.DynamicCommandExceptionType;
import com.mojang.brigadier.exceptions.Dynamic2CommandExceptionType;
import com.mojang.brigadier.suggestion.SuggestionProvider;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.commands.SharedSuggestionProvider;
import net.minecraft.commands.arguments.ResourceLocationArgument;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;

public final class TcgCommands {
    private static final String PREFIX = "commands." + Constants.MODID + ".";
    private static final DynamicCommandExceptionType UNKNOWN_SET = new DynamicCommandExceptionType(id -> Component.translatable(PREFIX + "unknown_set", id));
    private static final Dynamic2CommandExceptionType UNKNOWN_CARD = new Dynamic2CommandExceptionType((set, number) -> Component.translatable(PREFIX + "unknown_card", set, number));
    private static final SuggestionProvider<CommandSourceStack> SETS = (context, builder) -> SharedSuggestionProvider.suggestResource(TcgDataManager.SERVER.setIds(), builder);

    private TcgCommands() {
    }

    public static void register(CommandDispatcher<CommandSourceStack> dispatcher) {
        dispatcher.register(Commands.literal("tcg")
                .requires(source -> source.hasPermission(Commands.LEVEL_GAMEMASTERS))
                .then(Commands.literal("give")
                        .then(Commands.literal("pack")
                                .then(Commands.argument("set", ResourceLocationArgument.id()).suggests(SETS)
                                        .executes(context -> givePack(context, 1))
                                        .then(Commands.argument("amount", IntegerArgumentType.integer(1, 6400))
                                                .executes(context -> givePack(context, IntegerArgumentType.getInteger(context, "amount"))))))
                        .then(Commands.literal("card")
                                .then(Commands.argument("set", ResourceLocationArgument.id()).suggests(SETS)
                                        .then(Commands.argument("number", IntegerArgumentType.integer(1))
                                                .executes(context -> giveCard(context, false))
                                                .then(Commands.argument("holo", BoolArgumentType.bool())
                                                        .executes(context -> giveCard(context, BoolArgumentType.getBool(context, "holo")))))))));
    }

    private static int givePack(CommandContext<CommandSourceStack> context, int amount) throws CommandSyntaxException {
        ServerPlayer player = context.getSource().getPlayerOrException();
        TcgSet set = getSet(context);
        int granted = PackRewardService.grantPack(player, set.id(), amount, PackSource.COMMAND);
        context.getSource().sendSuccess(() -> Component.translatable(PREFIX + "give.pack", granted, set.definition().name(), player.getDisplayName()), true);
        return granted;
    }

    private static int giveCard(CommandContext<CommandSourceStack> context, boolean holo) throws CommandSyntaxException {
        ServerPlayer player = context.getSource().getPlayerOrException();
        TcgSet set = getSet(context);
        int number = IntegerArgumentType.getInteger(context, "number");
        CardDefinition card = set.card(number).orElseThrow(() -> UNKNOWN_CARD.create(set.id().toString(), number));

        ItemStack stack = TcgStacks.card(set, number, holo);
        PackRewardService.giveOrDrop(player, stack);
        context.getSource().sendSuccess(() -> Component.translatable(PREFIX + (holo ? "give.card_holo" : "give.card"), card.name(), number, set.definition().total(), player.getDisplayName()), true);
        return 1;
    }

    /**
     * Accepts full ids ({@code cobblemontcg:base1}) and, for convenience, bare set names ({@code base1}).
     */
    private static TcgSet getSet(CommandContext<CommandSourceStack> context) throws CommandSyntaxException {
        ResourceLocation id = ResourceLocationArgument.getId(context, "set");
        TcgSet set = TcgDataManager.SERVER.set(id).orElse(null);
        if (set == null && id.getNamespace().equals(ResourceLocation.DEFAULT_NAMESPACE)) {
            set = TcgDataManager.SERVER.set(Constants.id(id.getPath())).orElse(null);
        }
        if (set == null) {
            throw UNKNOWN_SET.create(id.toString());
        }
        return set;
    }
}
