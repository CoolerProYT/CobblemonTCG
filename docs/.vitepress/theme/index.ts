import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import { h } from 'vue'
import BoosterPack from './components/BoosterPack.vue'
import CardGallery from './components/CardGallery.vue'
import EnergyIcon from './components/EnergyIcon.vue'
import HeroHand from './components/HeroHand.vue'
import ItemSlot from './components/ItemSlot.vue'
import PackOdds from './components/PackOdds.vue'
import PackWrappers from './components/PackWrappers.vue'
import RecipeCard from './components/RecipeCard.vue'
import RewardTable from './components/RewardTable.vue'
import SetList from './components/SetList.vue'
import TcgCard from './components/TcgCard.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  Layout: () => h(DefaultTheme.Layout, null, { 'home-hero-image': () => h(HeroHand) }),
  enhanceApp({ app }) {
    app.component('BoosterPack', BoosterPack)
    app.component('CardGallery', CardGallery)
    app.component('EnergyIcon', EnergyIcon)
    app.component('ItemSlot', ItemSlot)
    app.component('PackOdds', PackOdds)
    app.component('PackWrappers', PackWrappers)
    app.component('RecipeCard', RecipeCard)
    app.component('RewardTable', RewardTable)
    app.component('SetList', SetList)
    app.component('TcgCard', TcgCard)
  },
} satisfies Theme
