import DefaultTheme from 'vitepress/theme';
import { h, onMounted, watch, nextTick } from "vue";
import giscusTalk from 'vitepress-plugin-comment-with-giscus';
import { useData, useRoute, inBrowser } from 'vitepress';
import mediumZoom from 'medium-zoom';
import vitepressBackToTop from 'vitepress-plugin-back-to-top';
import 'vitepress-plugin-back-to-top/dist/style.css';
import busuanzi from 'busuanzi.pure.js';

import './style/index.css';
import PageInfo from './components/PageInfo.vue';

export default {
  extends: DefaultTheme,

  Layout() {
    return h(DefaultTheme.Layout, null, {
        "doc-before": () => h(PageInfo) // 文章阅读统计
    });
  },

  enhanceApp({ app , router }) {
    if (inBrowser) {
      router.onAfterRouteChanged = () => {
        busuanzi.fetch()
      };
    }

    vitepressBackToTop({
      // default
      threshold:300
    })

  },

  setup() {
    // Get frontmatter and route
    const {frontmatter} = useData();
    const route = useRoute();
    const initZoom = () => {
    mediumZoom('.main img', { background: 'var(--vp-c-bg)' })
    };
    onMounted(() => {
        initZoom()
    });
    watch(
        () => route.path,
        () => nextTick(() => initZoom())
    );

    // giscus配置
    giscusTalk(
        {
          repo: 'funny-dream/youqu3', //仓库
          repoId: 'R_kgDOMBemKg', //仓库ID
          category: 'Announcements', // 讨论分类
          categoryId: 'DIC_kwDOMBemKs4CgATm', //讨论分类ID
          mapping: 'pathname',
          inputPosition: 'top',
          lang: 'zh-CN',
        },
        {
          frontmatter, route
        },
        //默认值为true，表示已启用，此参数可以忽略；
        //如果为false，则表示未启用
        //您可以使用“comment:true”序言在页面上单独启用它
        true
    )
  },
}