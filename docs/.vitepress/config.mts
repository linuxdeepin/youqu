import {defineConfig} from 'vitepress'
import {withMermaid} from "vitepress-plugin-mermaid";
import timeline from "vitepress-markdown-timeline";

// https://vitepress.dev/reference/site-config
export default withMermaid(
    defineConfig({
        // base: '/docs/',
        lang: 'zh-CN',
        title: "YouQu | Linux自动化测试利器",
        description: "",
        head: [
            ['meta', {name: 'referrer', content: 'no-referrer-when-downgrade'}],
        ],
        vite: {
            publicDir: "assets",
        },
        markdown: {
            config: (md) => {
                md.use(timeline)
            }
        },

        themeConfig: {
            // https://vitepress.dev/reference/default-theme-config
            siteTitle: "官方中文文档",
            nav: [
                {text: '快速开始', link: '/快速开始'},
                {text: '功能介绍', link: '/框架功能介绍'},
            ],
            search: {
                provider: 'local'
            },
            ignoreDeadLinks: true,
            // =========================================================
            logo: {src: '/logo.png', width: 70, height: 24},
            socialLinks: [
                {icon: 'github', link: 'https://github.com/linuxdeepin/youqu'}
            ],
            footer: {
                copyright: `版权所有 © 2023-${new Date().getFullYear()} 统信软件`
            },
            //大纲显示2-3级标题
            outline: [2, 4],
            //大纲顶部标题
            outlineTitle: '当前页大纲',

            docFooter: {
                prev: '上一页',
                next: '下一页'
            },

            lastUpdated: {
                text: '最后更新于',
                formatOptions: {
                    dateStyle: 'short',
                    timeStyle: 'medium'
                }
            },

            langMenuLabel: '多语言',
            returnToTopLabel: '回到顶部',
            sidebarMenuLabel: '菜单',
            darkModeSwitchLabel: '主题',
            lightModeSwitchTitle: '切换到浅色模式',
            darkModeSwitchTitle: '切换到深色模式'
        },
    })
);
