<template>
  <div>
    <n-grid :x-gap="24">
      <n-grid-item span="6">
        <n-card :bordered="false" size="small" class="proCard">
          <n-thing
            class="thing-cell"
            v-for="item in typeTabList"
            :key="item.key"
            :class="{ 'thing-cell-on': type === item.key }"
            @click="switchType(item)"
          >
            <template #header>{{ item.name }}</template>
            <template #description>{{ item.desc }}</template>
          </n-thing>
        </n-card>
      </n-grid-item>
      <n-grid-item span="18">
<!--        下面这栏是头上的那个名字-->
<!--        <n-card :bordered="false" size="small" :title="typeTitle" class="proCard">-->
          <n-card
            :segmented="{ content: 'hard' }"
            content-style="padding-top: 0;padding-bottom: 0;"
            :bordered="false"
            size="small"
            title="动态"
            class="block float-right"
          >
<!--            <template #header-extra><a href="javascript:;">更多</a></template>-->
            <n-list>
              <n-list-item v-for="(value,index) in motivation" :key="value" >
                <template #prefix>
                  <n-avatar circle :size="60" :src="schoolboy" />
                </template>
                <div class="text-3xl font-bold">id</div>
                <div style="text-indent:2em">{{value}}</div>
                <div class="text-xs text-gray-500 h-16 relative">
                  <div class="absolute bottom-0">
                    {{times[index]}}
                  </div>
                </div>
              </n-list-item>
            </n-list>
          </n-card>
<!--        </n-card>-->
      </n-grid-item>
    </n-grid>
  </div>
</template>
<script lang="ts">
  import { defineComponent, reactive, toRefs } from 'vue';
  import BasicSetting from './BasicSetting.vue';
  import RevealSetting from './RevealSetting.vue';
  import EmailSetting from './EmailSetting.vue';

  const typeTabList = [
    {
      name: '基本设置',
      desc: '系统常规设置',
      key: 1,
    },
    {
      name: '显示设置',
      desc: '系统显示设置',
      key: 2,
    },
    {
      name: '邮件设置',
      desc: '系统邮件设置',
      key: 3,
    },
  ];
  export default defineComponent({
    setup() {
      const state = reactive({
        type: 1,
        typeTitle: '基本设置',
      });
      let motivation=["Ah Jung 刚才把工作台页面随便写了一些，凑合能看了！",
        "Ah Jung 在 开源组 创建了项目 naive-ui-admin？",
        "@It界风清扬，向naive-ui-admin提交了一个bug，抽时间看看吧！",
        "技术部那几位童鞋，再次警告，不要摸鱼，不要摸鱼，不要摸鱼啦！",
        "上班不摸鱼，和咸鱼有什么区别（这话真不是我说的哈）！"]
      let times=["2021-07-04 22:37:16","2021-07-04 09:37:16","2021-07-04 22:37:16","2021-07-04 09:37:16","2021-07-04 20:37:16"]
      function switchType(e) {
        state.type = e.key;
        state.typeTitle = e.name;
      }

      return {
        ...toRefs(state),
        switchType,
        typeTabList,
        motivation,
        times
      };
    },
  });
</script>
<style lang="less" scoped>
  .thing-cell {
    margin: 0 -16px 10px;
    padding: 5px 16px;

    &:hover {
      background: #f3f3f3;
      cursor: pointer;
    }
  }

  .thing-cell-on {
    background: #f0faff;
    color: #2d8cf0;

    ::v-deep(.n-thing-main .n-thing-header .n-thing-header__title) {
      color: #2d8cf0;
    }

    &:hover {
      background: #f0faff;
    }
  }
</style>
