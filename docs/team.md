---
layout: page
---
<script setup>
import {
  VPTeamPage,
  VPTeamPageTitle,
  VPTeamMembers
} from 'vitepress/theme'

const members = [
  {
    avatar: 'https://www.github.com/mikigo.png',
    name: 'mikigo',
    title: 'Maintainer',
    links: [
      { icon: 'github', link: 'https://github.com/mikigo' },
      // { icon: 'twitter', link: 'https://twitter.com/mikigo' }
    ]
  },
  {
    avatar: 'https://www.github.com/githublitao.png',
    name: 'githublitao',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/githublitao' },
    ]
  },
  {
    avatar: 'https://www.github.com/zhao-george.png',
    name: 'zhao-george',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/zhao-george' },
    ]
  },
  {
    avatar: 'https://www.github.com/saifeiLee.png',
    name: 'saifeiLee',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/saifeiLee' },
    ]
  },
  {
    avatar: 'https://www.github.com/DarkLii.png',
    name: 'DarkLii',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/DarkLii' },
    ]
  },
  {
    avatar: 'https://www.github.com/rb-union.png',
    name: 'rb-union',
    title: 'Helper',
    links: [
      { icon: 'github', link: 'https://github.com/rb-union' },
    ]
  },
  {
    avatar: 'https://www.github.com/Jimijun.png',
    name: 'Jimijun',
    title: 'Helper',
    links: [
      { icon: 'github', link: 'https://github.com/Jimijun' },
    ]
  },
  {
    avatar: 'https://www.github.com/king123666.png',
    name: 'king123666',
    title: 'Helper',
    links: [
      { icon: 'github', link: 'https://github.com/king123666' },
    ]
  },
  {
    avatar: 'https://www.github.com/momiji33.png',
    name: 'momiji33',
    title: 'Helper',
    links: [
      { icon: 'github', link: 'https://github.com/momiji33' },
    ]
  },
  {
    avatar: 'https://www.github.com/lu-xianseng.png',
    name: 'lu-xianseng',
    title: 'Helper',
    links: [
      { icon: 'github', link: 'https://github.com/lu-xianseng' },
    ]
  },
  
]
</script>

<VPTeamPage>
  <VPTeamPageTitle>
    <template #title>
      Our Team
    </template>
    <template #lead>
      The development of YouQu is guided by an international
      team, some of whom have chosen to be featured below.
    </template>
  </VPTeamPageTitle>
  <VPTeamMembers
    size="small"
    :members="members"
  />
</VPTeamPage>