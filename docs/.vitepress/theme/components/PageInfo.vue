<script setup>
import DefaultTheme from 'vitepress/theme'
import { useData } from 'vitepress'
import { ref } from 'vue'

const { Layout } = DefaultTheme
const defaultAuthor = 'mikigo'
const { frontmatter } = useData() //这里的frontmatter就是各个md文件中自己写在最上面的东西
</script>

<template>
    <div class="page_info">
        <span class="page_info_item" v-if="frontmatter.Author">
            🎨
            <span>作者：{{ frontmatter.Author }}</span>
        </span>
        <span class="page_info_item" v-if="frontmatter.date">
            🕐
            <span>发表于：{{ frontmatter.date ? frontmatter.date.substring(0, 10) : '' }}</span>
        </span>
        <span class="page_info_item">
            📔
            <span id="busuanzi_container_page_pv">
                阅读量：<span id="busuanzi_value_page_pv"></span>
            </span>
        </span>

    </div>
</template>

<style>
.page_info {
    margin-bottom: 48px;
}

.page_info .page_info_item {
    font-size: 16px;
    color: #7f7f7f;
    margin-right: 10px;
}
</style>