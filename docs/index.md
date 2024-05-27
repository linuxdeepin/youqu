---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: YouQu
  text: "使用简单且功能强大的自动化测试框架"
  tagline: 让 Linux 自动化测试变得简单
  actions:
    - theme: brand
      text: YouQu是什么？
      link: /指南/简介/YouQu是什么
    - theme: alt
      text: 快速开始
      link: /指南/简介/快速开始
    - theme: alt
      text: GitHub
      link: "https://github.com/linuxdeepin/youqu"
    - theme: alt
      text: Gitee
      link: "https://gitee.com/deepin-community/youqu"
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
  - icon: ️⏲️
    title: Linux 桌面应用性能自动化测试
    details: 让Linux桌面应用性能测试更简单、高效，选YouQu自动化测试基础框架。
  - icon: ️💥
    title: Fuzzy Desktop 桌面模糊测试
    details: 探索桌面应用的安全边界，YouQu自动化测试基础框架助您实现Fuzzy Desktop模糊测试无忧。

---

<style>
:root {
  --vp-home-hero-name-color: transparent;
  --vp-home-hero-name-background: -webkit-linear-gradient(120deg, #FF9933 30%, #41d1ff);

  --vp-home-hero-image-background-image: linear-gradient(-45deg, #FF9933 50%, #47caff 50%);
  --vp-home-hero-image-filter: blur(44px);
}

@media (min-width: 640px) {
  :root {
    --vp-home-hero-image-filter: blur(56px);
  }
}

@media (min-width: 960px) {
  :root {
    --vp-home-hero-image-filter: blur(68px);
  }
}
</style>

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
      Contributers
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
      感谢以下所有人的提供帮助及重要建议
    </template>
  </VPTeamPageTitle>
  <VPTeamMembers
    size="small"
    :members="helpers"
  />
</VPTeamPage>