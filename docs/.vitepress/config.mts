import {defineConfig} from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    base: process.env.VITE_BASE,
    lang: 'zh-CN',
    title: "YouQu3 | Next-Gen Linux Autotest Framework",
    description: "让 Linux 自动化测试变得更简单",
    head: [
        // ['meta', {name: 'referrer', content: 'no-referrer-when-downgrade'}],
        ['link', {rel: 'icon', href: `${process.env.VITE_BASE || '/'}favicon.ico`}],
    ],
    vite: {
        publicDir: "assets",
    },

    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        siteTitle: "YouQu3",
        nav: [
                {text: '🏠 首页', link: '/index'},
            {text: '🧭 指南', link: '/指南/简介/YouQu3是什么'},
            {text: '🏃‍ 实践', link: '/实践/简介'},
            {text: '🎵 规划', link: '/规划/YouQu3架构设计规划'},
            {text: '🔌 插件', link: '/插件/插件列表'},
        ],

        sidebar: {
            "/指南/": [
                {
                    text: "简介",
                    items: [
                        {text: "YouQu3是什么", link: "/指南/简介/YouQu3是什么"},
                        {text: "快速开始", link: "/指南/简介/快速开始"},
                    ]
                },
                {
                    text: "环境管理",
                    items: [
                        {text: "虚拟环境", link: "/指南/环境管理/虚拟环境"},
                        {text: "原生环境", link: "/指南/环境管理/原生环境"},
                    ]
                },
                {
                    text: "驱动执行",
                    items: [
                        {text: "本地执行", link: "/指南/驱动执行/本地执行"},
                        {text: "远程执行", link: "/指南/驱动执行/远程执行"},
                        {text: "自定义执行", link: "/指南/驱动执行/自定义执行"},
                    ]
                },
                {
                    text: "与生俱来",
                    items: [
                        {text: "脚手架工具", link: "/指南/与生俱来/脚手架工具"},
                        {text: "全自动日志", link: "/指南/与生俱来/全自动日志"},
                        {text: "标签化管理", link: "/指南/与生俱来/标签化管理"},
                        {text: "远程交互控制", link: "/指南/与生俱来/远程交互控制"},
                        {text: "命令行交互", link: "/指南/与生俱来/命令行交互"},
                        {text: "DBus交互", link: "/指南/与生俱来/DBus交互"},
                        {text: "断言语句", link: "/指南/与生俱来/断言语句"},
                        {text: "动态等待", link: "/指南/与生俱来/动态等待"},
                        {text: "JSON报告", link: "/指南/与生俱来/JSON报告"},
                        {text: "前后钩子", link: "/指南/与生俱来/前后钩子"},
                    ]
                },
                {
                    text: "可选功能",
                    items: [
                        {text: "LinuxGUI", link: "/指南/可选功能/LinuxGUI"},
                        {text: "WebUI", link: "/指南/可选功能/WebUI"},
                        {text: "网络访问", link: "/指南/可选功能/网络访问"},
                        {text: "HTML报告", link: "/指南/可选功能/HTML报告"},
                        {text: "用例录屏", link: "/指南/可选功能/用例录屏"},
                    ]
                },

            ],
            "/实践/": [
                {
                    text: "从零开始构建自动化工程",
                    collapsed: false,
                    items: [
                        {text: "简介", link: "/实践/简介"},
                        {text: "工程创建", link: "/实践/工程创建"},
                        {text: "方法开发", link: "/实践/方法开发"},
                        {text: "用例开发", link: "/实践/用例开发"},
                        {text: "配置模块", link: "/实践/配置模块"},
                        {text: "依赖管理", link: "/实践/依赖管理"},
                    ]
                }
            ],
            "/规划/": [
                {
                    text: "设计规划",
                    collapsed: false,
                    items: [
                        {text: "YouQu3架构设计规划", link: "/规划/YouQu3架构设计规划"},
                        {text: "UOS自动化测试方法套件", link: "/规划/UOS自动化测试方法套件"},
                        {text: "UOS自动化测试用例", link: "/规划/UOS自动化测试用例"},
                    ]
                },
            ],
            "/插件/": [
                {text: "插件汇总", link: "/插件/插件列表"},
            ],
        },
        search: {
            provider: 'local'
        },
        ignoreDeadLinks: true,
        // =========================================================
        logo: {src: '/logo.png', width: 22, height: 30},
        socialLinks: [
            {icon: 'github', link: 'https://github.com/funny-dream/youqu3'}
        ],
        footer: {
            copyright: `版权所有 © 2024-${new Date().getFullYear()} 统信软件`
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
});
