import {defineConfig} from 'vitepress'
import {withMermaid} from "vitepress-plugin-mermaid";
import timeline from "vitepress-markdown-timeline";
import {version} from "../../package.json"

// https://vitepress.dev/reference/site-config
export default withMermaid(
    defineConfig({
        base: process.env.VITE_BASE,
        lang: 'zh-CN',
        title: "YouQu | Linux自动化测试利器",
        description: "使用简单且功能强大的自动化测试框架",
        head: [
            ['meta', {name: 'referrer', content: 'no-referrer-when-downgrade'}],
            ['link', {rel: 'icon', href: `${process.env.VITE_BASE || '/'}favicon.ico`}],
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
            siteTitle: "YouQu",
            nav: [
                {text: '首页', link: '/index'},
                {text: '指南', link: '/指南/简介/YouQu是什么'},
                {text: '实践', link: '/实践/Linux桌面UI自动化测试/初始化项目'},
                {
                    text: '规划', items: [
                        {text: "框架设计", link: '/规划/框架设计/AT基础框架设计方案'},
                        {text: "Deepin Autotest", link: 'https://youqu.uniontech.com/deepin-autotest/'},
                    ]
                },
                {
                    text: `v${version}`, items: [
                        {text: "更新日志", link: '/RELEASE'},
                        {text: "参与贡献", link: '/CONTRIBUTING'},
                        {text: "兴趣小组", link: '/SIG'},
                    ]
                },
                {
                    text: '🔌 插件', items: [
                        {text: "日志系统 | funnylog", link: "https://linuxdeepin.github.io/funnylog/"},
                        {text: "重启方案 | letmego", link: "https://linuxdeepin.github.io/letmego/"},
                        {text: "文字识别 | pdocr-rpc", link: "https://linuxdeepin.github.io/pdocr-rpc/"},
                        {text: "图像识别 | image-center", link: "https://linuxdeepin.github.io/image-center/"},
                    ]
                },
            ],

            sidebar: {
                "/指南/": [
                    {
                        text: "简介",
                        items: [
                            {text: "YouQu是什么", link: "/指南/简介/YouQu是什么"},
                            {text: "快速开始", link: "/指南/简介/快速开始"},
                        ]
                    },
                    {
                        text: "环境",
                        collapsed: false,
                        items: [
                            {text: "环境部署", link: "/指南/环境/环境部署"},
                            {text: "全局配置", link: "/指南/环境/全局配置"},
                        ]
                    },
                    {
                        text: "元素定位",
                        collapsed: false,
                        items: [
                            {text: "图像识别", link: "/指南/元素定位/图像识别"},
                            {text: "属性定位", link: "/指南/元素定位/属性定位"},
                            {text: "OCR识别", link: "/指南/元素定位/OCR识别"},
                            {text: "相对坐标定位", link: "/指南/元素定位/相对坐标定位"},
                            {text: "去干扰识别", link: "/指南/元素定位/去干扰识别"},
                        ]
                    },
                    {
                        text: "框架必备",
                        collapsed: false,
                        items: [
                            {text: "断言", link: "/指南/框架必备/断言"},
                            {text: "键鼠操作", link: "/指南/框架必备/键鼠操作"},
                            {text: "执行管理器", link: "/指南/框架必备/执行管理器"},
                            {text: "测试报告", link: "/指南/框架必备/测试报告"},
                            {text: "Ruff代码检查", link: "/指南/框架必备/Ruff代码检查"},
                        ]
                    },
                    {
                        text: "特色功能",
                        collapsed: false,
                        items: [
                            {text: "标签化管理", link: "/指南/特色功能/标签化管理"},
                            {text: "标签自动同步", link: "/指南/特色功能/标签自动同步"},
                            {text: "全自动日志", link: "/指南/特色功能/全自动日志"},
                            {text: "远程交互式控制", link: "/指南/特色功能/远程交互式控制"},
                            {text: "失败录屏", link: "/指南/特色功能/失败录屏"},
                            {text: "WebUI", link: "/指南/特色功能/WebUI"},
                            {text: "Wayland适配", link: "/指南/特色功能/Wayland适配"},
                            {text: "重启类场景", link: "/指南/特色功能/重启类场景"},
                            {text: "数据回填", link: "/指南/特色功能/数据回填"},
                        ]
                    },
                ],
                "/实践/": [
                    {
                        text: "Linux桌面UI自动化测试",
                        collapsed: false,
                        items: [
                            {text: "初始化项目", link: "/实践/Linux桌面UI自动化测试/初始化项目"},
                            {text: "创建APP工程", link: "/实践/Linux桌面UI自动化测试/创建APP工程"},
                            {text: "创建一条完整的用例", link: "/实践/Linux桌面UI自动化测试/创建一条完整的用例"},
                            {text: "远程交互式控制", link: "/实践/Linux桌面UI自动化测试/远程交互式控制"},
                        ]
                    },
                    {
                        text: "WebUI自动化测试",
                        collapsed: false,
                        items: [
                            {text: "初始化项目", link: "/实践/WebUI自动化测试/初始化项目"},
                            {text: "创建APP工程", link: "/实践/WebUI自动化测试/创建APP工程"},
                            {text: "创建一条完整的用例", link: "/实践/WebUI自动化测试/创建一条完整的用例"},
                        ]
                    },
                    {
                        text: "DBus接口自动化测试",
                        collapsed: false,
                        items: [
                            {text: "初始化项目", link: "/实践/DBus接口自动化测试/初始化项目"},
                            {text: "创建APP工程", link: "/实践/DBus接口自动化测试/创建APP工程"},
                            {text: "创建一条完整的用例", link: "/实践/DBus接口自动化测试/创建一条完整的用例"},
                        ]
                    },
                    {
                        text: "命令行自动化测试",
                        collapsed: false,
                        items: [
                            {text: "初始化项目", link: "/实践/命令行自动化测试/初始化项目"},
                            {text: "创建APP工程", link: "/实践/命令行自动化测试/创建APP工程"},
                            {text: "创建一条完整的用例", link: "/实践/命令行自动化测试/创建一条完整的用例"},
                        ]
                    },
                    {
                        text: "HTTP接口自动化测试",
                        collapsed: false,
                        items: [
                            {text: "初始化项目", link: "/实践/HTTP接口自动化测试/初始化项目"},
                            {text: "创建APP工程", link: "/实践/HTTP接口自动化测试/创建APP工程"},
                            {text: "创建一条完整的用例", link: "/实践/HTTP接口自动化测试/创建一条完整的用例"},
                        ]
                    },
                ],
                "/规划/": [
                    {
                        text: "框架设计",
                        collapsed: false,
                        items: [
                            {text: "自动化测试架构设计规划", link: "/规划/框架设计/自动化测试架构设计v1.0"},
                            {text: "AT基础框架设计方案", link: "/规划/框架设计/AT基础框架设计方案"},
                            {text: "AT应用库设计方案", link: "/规划/框架设计/AT应用库设计方案"},
                        ]
                    },
                    {text: "未来规划", link: "/规划/未来规划"}
                ],
            },
            search: {
                provider: 'local'
            },
            ignoreDeadLinks: true,
            // =========================================================
            logo: {src: '/logo.png', width: 25, height: 30},
            socialLinks: [
                {icon: 'github', link: 'https://github.com/linuxdeepin/youqu'}
            ],
            footer: {
                copyright: `版权所有 © 2020-${new Date().getFullYear()} 统信软件`
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
