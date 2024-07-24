---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: YouQu
  text: "使用简单且功能强大的自动化测试框架"
  tagline: 让 Linux 自动化测试变得简单
  actions:
    - theme: brand
      text: YouQu3 🔥
      link: "https://youqu.uniontech.com/v3/"
    - theme: brand
      text: PyLinuxAuto 🔥
      link: "https://youqu.uniontech.com/pylinuxauto/"
  image:
    src: /logo.png
    alt: YouQu

features:
  - icon: 💻
    title: Linux 桌面 UI 自动化测试
    details: 提升Linux桌面应用品质，确保用户体验的一致性，选择我们的UI自动化测试服务。
    link: /实践/Linux桌面UI自动化测试/初始化项目
    linkText: 查看
  - icon: 🌏
    title: Web UI 自动化测试
    details: Web UI自动化测试，优化用户体验，提升Web应用的稳定性和可靠性。
    link: /实践/WebUI自动化测试/初始化项目
    linkText: 查看
  - icon: 🚌
    title: Linux DBus 接口自动化测试
    details: 专业自动化测试D-Bus接口，为Linux桌面应用的稳定性和可靠性保驾护航。
    link: /实践/DBus接口自动化测试/初始化项目
    linkText: 查看
  - icon: 🚀
    title: 命令行自动化测试
    details: 高效命令行自动化测试，让Linux软件开发和维护更加轻松便捷。
    link: /实践/命令行自动化测试/初始化项目
    linkText: 查看
  - icon: ️🕷️
    title: HTTP 接口自动化测试
    details: 保障HTTP接口的响应速度和数据传输安全，我们的自动化测试是您的明智之选。
    link: /实践/HTTP接口自动化测试/初始化项目
    linkText: 查看

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
    title: 'Creator',
    org: 'YouQu',
    orgLink: 'https://github.com/linuxdeepin/youqu',
    links: [
      { icon: 'github', link: 'https://github.com/mikigo' },
      { icon: 'x', link: 'https://twitter.com/mikigo_' },
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
    avatar: 'https://www.github.com/CCrazyPeter.png',
    name: 'CCrazyPeter',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/CCrazyPeter' },
    ]
  },
  {
    avatar: 'https://www.github.com/003307.png',
    name: '003307',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/003307' },
    ]
  }, 
  {
    avatar: 'https://www.github.com/Marszzz1116.png',
    name: 'Marszzz1116',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/Marszzz1116' },
    ]
  },  
  {
    avatar: 'https://www.github.com/lu-xianseng.png',
    name: 'lu-xianseng',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/lu-xianseng' },
    ]
  },
  {
    avatar: 'https://www.github.com/KeyLee123.png',
    name: 'KeyLee123',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/KeyLee123' },
    ]
  },  
];

const helpers = [
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
]
</script>

<VPTeamPage>
  <VPTeamPageTitle>
    <template #title>
      Contributors
    </template>
    <template #lead>
      感谢以下所有人的贡献与参与
    </template>
  </VPTeamPageTitle>
  <VPTeamMembers
    size="small"
    :members="members"
  />
  <VPTeamPageTitle>
    <template #title>
      Helpers
    </template>
    <template #lead>
      感谢以下所有人提供的帮助及重要建议
    </template>
  </VPTeamPageTitle>
  <VPTeamMembers
    size="small"
    :members="helpers"
  />
</VPTeamPage>