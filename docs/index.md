---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: YouQu
  text: "使用简单且功能强大的自动化测试框架"
  tagline: 让 Linux 自动化测试变得简单
  actions:
    - theme: brand
      text: 快速开始
      link: /README
    - theme: alt
      text: 留言
      link: /comments.md
  image:
      src: /logo.png
      alt: YouQu

features:
  - icon: 📝
    title: Linux 桌面 UI 自动化测试
    details: 用热情的笔触描绘生活的点点滴滴，记录下我们共同成长的足迹。
  - icon: 💡
    title: Linux DBus/Gsettings 接口自动化测试
    details: 让知识的火花在分享中绽放，点燃我们追求卓越的热情。
  - icon: 🚀
    title: 命令行自动化测试
    details: 拥抱成长的旅程，让热情的阳光照耀我们不断前行的道路。
  - icon: 🚀
    title: HTTP 接口自动化测试
    details: 拥抱成长的旅程，让热情的阳光照耀我们不断前行的道路。
  - icon: 🚀
    title: Web UI 自动化测试
    details: 拥抱成长的旅程，让热情的阳光照耀我们不断前行的道路。
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