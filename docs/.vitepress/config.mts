import { defineConfig } from 'vitepress'

// GitHub Pages serves a project site from /<repository>/. For a custom domain or a user site, build with DOCS_BASE=/.
const base = process.env.DOCS_BASE ?? '/CobblemonTCG/'

export default defineConfig({
  title: 'Cobblemon: TCG',
  description: 'Open booster packs and collect trading cards in Cobblemon: sets, pack odds, rewards, the Card Dealer and datapacks.',
  base,
  cleanUrls: true,
  srcExclude: ['README.md', 'scripts/**'],
  head: [['link', { rel: 'icon', type: 'image/png', href: `${base}items/icon.png` }]],
  themeConfig: {
    logo: { src: '/items/icon.png', alt: '' },
    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Cards', link: '/sets/' },
      { text: 'Datapacks', link: '/datapacks/' },
    ],
    sidebar: [
      {
        text: 'Guide',
        items: [
          { text: 'Getting started', link: '/guide/getting-started' },
          { text: 'Booster packs', link: '/guide/booster-packs' },
          { text: 'Cards', link: '/guide/cards' },
          { text: 'Card Binder', link: '/guide/card-binder' },
          { text: 'Card Dealer & traders', link: '/guide/card-dealer' },
          { text: 'Pokémon rewards', link: '/guide/rewards' },
          { text: 'Commands', link: '/guide/commands' },
          { text: 'Configuration', link: '/guide/configuration' },
          { text: 'CobbleDollars', link: '/guide/cobbledollars' },
        ],
      },
      {
        text: 'Sets',
        items: [
          { text: 'All sets', link: '/sets/' },
          { text: 'Base Set', link: '/sets/base1' },
          { text: 'Jungle', link: '/sets/base2' },
        ],
      },
      {
        text: 'Datapacks & resource packs',
        items: [
          { text: 'Overview', link: '/datapacks/' },
          { text: 'Set files', link: '/datapacks/sets' },
          { text: 'Card files', link: '/datapacks/cards' },
          { text: 'Reward rules', link: '/datapacks/rewards' },
          { text: 'Textures & art', link: '/datapacks/textures' },
        ],
      },
      { text: 'FAQ', link: '/faq' },
    ],
    socialLinks: [{ icon: 'github', link: 'https://github.com/CoolerProYT/CobblemonTCG' }],
    search: { provider: 'local' },
    outline: { level: [2, 3] },
    footer: {
      message: 'Released under the CC0-1.0 License. Unofficial fan project, not affiliated with Nintendo, The Pokémon Company, Game Freak or Creatures Inc.',
    },
  },
})
