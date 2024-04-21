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
      link: /简介/YouQu是什么
    - theme: alt
      text: 快速开始
      link: /简介/快速开始
    - theme: alt
      text: GitHub
      link: "https://github.com/linuxdeepin/youqu"
  image:
      src: /logo.png
      alt: YouQu

features:
  - icon: 💻
    title: Linux 桌面 UI 自动化测试
    details: 提升Linux桌面应用品质，确保用户体验的一致性，选择我们的UI自动化测试服务。
  - icon: 🚌
    title: Linux DBus/Gsettings 接口自动化测试
    details: 专业自动化测试D-Bus和Gsettings接口，为Linux桌面应用的稳定性和可靠性保驾护航。
  - icon: 🚀
    title: 命令行自动化测试
    details: 高效命令行自动化测试，让Linux软件开发和维护更加轻松便捷。
  - icon: 🌏
    title: HTTP 接口自动化测试
    details: 保障HTTP接口的响应速度和数据传输安全，我们的自动化测试是您的明智之选。
  - icon: 🐵
    title: Web UI 自动化测试
    details: Web UI自动化测试，优化用户体验，提升Web应用的稳定性和可靠性。
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