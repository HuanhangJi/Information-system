<template>
  <div>
    <div class="n-layout-page-header">
      <n-card :bordered="false" title="工作台">
        <n-grid cols="2 s:1 m:1 l:2 xl:2 2xl:2" responsive="screen">
          <n-gi>
            <div class="flex items-center">
              <div>
                <n-avatar circle :size="64" :src="schoolboy" />
              </div>
              <div>
                <p class="px-4 text-xl">{{greet}}{{username}}，开始您一天的工作吧！</p>
                <button @click="change">change</button>
                <p class="px-4 text-gray-400">今日阴转大雨，15℃ - 25℃，出门记得带伞哦。</p>
              </div>
            </div>
          </n-gi>
          <n-gi>
            <div class="flex justify-end w-full">
              <div class="flex flex-1 flex-col justify-center text-right workspace_clickable" @click="gotomission">
                <span class="text-secondary">项目数</span>
                <span class="text-2xl">{{ userinfo.mission_count }}</span>
              </div>
              <div class="flex flex-1 flex-col justify-center text-right workspace_clickable" @click="gotofilted_mission">
                <span class="text-secondary">待办任务</span>
                <span class="text-2xl">{{userinfo.undone_mission}}</span>
              </div>
              <div class="flex flex-1 flex-col justify-center text-right workspace_clickable" @click="gotomessage">
                <span class="text-secondary">消息</span>
                <span class="text-2xl">{{userinfo.message}}</span>
              </div>
            </div>
          </n-gi>
        </n-grid>
      </n-card>
    </div>
<!--    <n-grid class="mt-4" cols="2 s:1 m:1 l:2 xl:2 2xl:2" responsive="screen" :x-gap="12" :y-gap="9" :cols="2">-->
    <n-grid class="mt-4" cols="2" :x-gap="12" :y-gap="9" v-if="false">
      <n-gi>
        <n-card
          :segmented="{ content: 'hard' }"
          content-style="padding: 0;"
          :bordered="false"
          size="small"
          title="任务直达"
        >
          <div class="flex flex-wrap project-card">
            <template v-for="(item,index) in short_mission" :key="index">
            <n-card
              size="small"
              class="cursor-pointer  ms:w-1/2"
              hoverable
            >
              <div class="flex">
                <span>
                  <n-icon size="30">
                    <GithubOutlined />
                  </n-icon>
                </span>
                <span class="text-lg ml-4">{{ item.name }}</span>
              </div>
              <div class="flex mt-2 h-6 text-gray-400">
                {{ item.description }}
              </div>
              <div class="flex mt-2 h-6 text-gray-400"> {{item.poster}}，{{item.time}} </div>
            </n-card>
            </template>
          </div>
        </n-card>
      </n-gi>
    </n-grid>
    <n-grid class="mt-4" cols="2" :x-gap="12" :y-gap="9">
      <n-gi>
        <n-card
          :segmented="{ content: 'hard' }"
          content-style="padding: 0;"
          :bordered="false"
          size="small"
          title="任务直达"
        >
          <div class="flex flex-wrap project-card">
            <n-card
              size="small"
              class="cursor-pointer  ms:w-1/2"
              hoverable
            >
              <div class="flex">
                <span>
                  <n-icon size="30">
                    <GithubOutlined />
                  </n-icon>
                </span>
                <span class="text-lg ml-4">Github</span>
              </div>
              <div class="flex mt-2 h-6 text-gray-400">
                是一个面向开源及私有软件项目的托管平台。
              </div>
              <div class="flex mt-2 h-6 text-gray-400"> 开源君，2021-07-04 </div>
            </n-card>
            <n-card
              size="small"
              class="cursor-pointer  ms:w-1/2 "
              hoverable
            >
              <div class="flex">
                <span>
                  <n-icon size="30" color="#42b983">
                    <LogoVue />
                  </n-icon>
                </span>
                <span class="text-lg ml-4">Vue</span>
              </div>
              <div class="flex mt-2 h-6 text-gray-400"> 渐进式 JavaScript 框架 </div>
              <div class="flex mt-2 h-6 text-gray-400"> 学不动也要学，2021-07-04 </div>
            </n-card>
            <n-card
              size="small"
              class="cursor-pointer  ms:w-1/2 "
              hoverable
            >
              <div class="flex">
                <span>
                  <n-icon size="30" color="#e44c27">
                    <Html5Outlined />
                  </n-icon>
                </span>
                <span class="text-lg ml-4">Html5</span>
              </div>
              <div class="flex mt-2 h-6 text-gray-400"> HTML5是互联网的下一代标准。 </div>
              <div class="flex mt-2 h-6 text-gray-400"> 撸码也是一种艺术 2021-04-01 </div>
            </n-card>
            <n-card
              size="small"
              class="cursor-pointer ms:w-1/2 "
              hoverable
            >
              <div class="flex">
                <span>
                  <n-icon size="30" color="#dd0031">
                    <LogoAngular />
                  </n-icon>
                </span>
                <span class="text-lg ml-4">Angular</span>
              </div>
              <div class="flex mt-2 h-6 text-gray-400"> 现代 Web 开发平台，百万粉丝热捧。 </div>
              <div class="flex mt-2 h-6 text-gray-400"> 铁粉君 2021-07-04。 </div>
            </n-card>
            <n-card
              size="small"
              class="cursor-pointer ms:w-1/2 "
              hoverable
            >
              <div class="flex">
                <span>
                  <n-icon size="30" color="#61dafb">
                    <LogoReact />
                  </n-icon>
                </span>
                <span class="text-lg ml-4">React</span>
              </div>
              <div class="flex mt-2 h-6 text-gray-400"> 用于构建用户界面的 JavaScript 库。 </div>
              <div class="flex mt-2 h-6 text-gray-400"> 技术牛 2021-07-04。 </div>
            </n-card>
            <n-card
              size="small"
              class="cursor-pointer ms:w-1/2 "
              hoverable
            >
              <div class="flex">
                <span>
                  <n-icon size="30">
                    <LogoJavascript />
                  </n-icon>
                </span>
                <span class="text-lg ml-4">Js</span>
              </div>
              <div class="flex mt-2 h-6 text-gray-400"> 路是走出来的，而不是空想出来的。 </div>
              <div class="flex mt-2 h-6 text-gray-400"> 架构组 2021-07-04 </div>
            </n-card>
          </div>
        </n-card>
      </n-gi>
      <n-gi>
        <n-card
          :segmented="{ content: 'hard' }"
          content-style="padding-top: 0;padding-bottom: 0;"
          :bordered="false"
          size="small"
          title="动态"
          class="block float-right"
        >
          <template #header-extra><a href="javascript:;">更多</a></template>
          <n-list>
            <n-list-item v-for="(value,index) in motivation" :key="value" >
              <template #prefix>
                <n-avatar circle :size="60" :src="schoolboy" />
              </template>
              <n-thing :title="value" class="text-3xl">
              </n-thing>
                <div class="text-xs text-gray-500 h-16 relative">
                  <div class="absolute bottom-0">
                    {{times[index]}}
                  </div>
                </div>
            </n-list-item>
<!--            <n-list-item>-->
<!--              <template #prefix>-->
<!--                <n-avatar circle :size="40" :src="schoolboy" />-->
<!--              </template>-->
<!--              <n-thing title="页面切换其实也支持缓存，只是加了过度效果，看起来像是重新渲染了">-->
<!--                <template #description>-->
<!--                  <p class="text-gray-400">-->
<!--                    <n-input type="text" placeholder="不信，输点文字试试" />-->
<!--                  </p>-->
<!--                </template>-->
<!--              </n-thing>-->
<!--            </n-list-item>-->
          </n-list>
        </n-card>
      </n-gi>
<!--      <n-gi>-->
<!--        <n-card-->
<!--          :segmented="{ content: 'hard' }"-->
<!--          content-style="padding: 0;"-->
<!--          :bordered="false"-->
<!--          size="small"-->
<!--          title="快捷操作"-->
<!--        >-->
<!--          <div class="flex flex-wrap project-card">-->
<!--            <n-card size="small" class="cursor-pointer project-card-item" hoverable>-->
<!--              <div class="flex flex-col justify-center text-gray-500">-->
<!--                <span class="text-center">-->
<!--                  <n-icon size="30" color="#68c755">-->
<!--                    <DashboardOutlined />-->
<!--                  </n-icon>-->
<!--                </span>-->
<!--                <span class="text-lx text-center">主控台</span>-->
<!--              </div>-->
<!--            </n-card>-->
<!--            <n-card size="small" class="cursor-pointer project-card-item" hoverable>-->
<!--              <div class="flex flex-col justify-center text-gray-500">-->
<!--                <span class="text-center">-->
<!--                  <n-icon size="30" color="#fab251">-->
<!--                    <ProfileOutlined />-->
<!--                  </n-icon>-->
<!--                </span>-->
<!--                <span class="text-lx text-center">列表</span>-->
<!--              </div>-->
<!--            </n-card>-->
<!--            <n-card size="small" class="cursor-pointer project-card-item" hoverable>-->
<!--              <div class="flex flex-col justify-center text-gray-500">-->
<!--                <span class="text-center">-->
<!--                  <n-icon size="30" color="#1890ff">-->
<!--                    <FileProtectOutlined />-->
<!--                  </n-icon>-->
<!--                </span>-->
<!--                <span class="text-lx text-center">表单</span>-->
<!--              </div>-->
<!--            </n-card>-->
<!--            <n-card size="small" class="cursor-pointer project-card-item" hoverable>-->
<!--              <div class="flex flex-col justify-center text-gray-500">-->
<!--                <span class="text-center">-->
<!--                  <n-icon size="30" color="#f06b96">-->
<!--                    <ApartmentOutlined />-->
<!--                  </n-icon>-->
<!--                </span>-->
<!--                <span class="text-lx text-center">权限管理</span>-->
<!--              </div>-->
<!--            </n-card>-->
<!--            <n-card size="small" class="cursor-pointer project-card-item" hoverable>-->
<!--              <div class="flex flex-col justify-center text-gray-500">-->
<!--                <span class="text-center">-->
<!--                  <n-icon size="30" color="#7238d1">-->
<!--                    <SettingOutlined />-->
<!--                  </n-icon>-->
<!--                </span>-->
<!--                <span class="text-lx text-center">系统管理</span>-->
<!--              </div>-->
<!--            </n-card>-->
<!--            <n-card size="small" class="cursor-pointer project-card-item" hoverable>-->
<!--              <div class="flex flex-col justify-center text-gray-500">-->
<!--                <span class="text-center">-->
<!--                  <n-icon size="30" color="">-->
<!--                    <DashboardOutlined />-->
<!--                  </n-icon>-->
<!--                </span>-->
<!--                <span class="text-lx text-center">主控台</span>-->
<!--              </div>-->
<!--            </n-card>-->
<!--          </div>-->
<!--        </n-card>-->
<!--        <n-card :segmented="{ content: 'hard' }" :bordered="false" size="small" class="mt-4">-->
<!--          <img src="~@/assets/images/Business.svg" class="w-full" />-->
<!--        </n-card>-->
<!--      </n-gi>-->
    </n-grid>
  </div>
</template>

<script lang="ts" setup>
  import schoolboy from '@/assets/images/schoolboy.png';
  import {
    GithubOutlined,
    DashboardOutlined,
    ProfileOutlined,
    FileProtectOutlined,
    SettingOutlined,
    ApartmentOutlined,
    Html5Outlined,
  } from '@vicons/antd';
  import { LogoVue, LogoAngular, LogoReact, LogoJavascript } from '@vicons/ionicons5';
  import { useRouter } from "vue-router";
  import { computed, onMounted, ref } from "vue";
  import axios from "axios";
  const router=useRouter()

//动态内容
  let short_message=ref([])
  let motivation=["Ah Jung 刚才把工作台页面随便写了一些，凑合能看了！",
    "Ah Jung 在 开源组 创建了项目 naive-ui-admin？",
    "@It界风清扬，向naive-ui-admin提交了一个bug，抽时间看看吧！",
    "技术部那几位童鞋，再次警告，不要摸鱼，不要摸鱼，不要摸鱼啦！",
    "上班不摸鱼，和咸鱼有什么区别（这话真不是我说的哈）！"]
  let times=["2021-07-04 22:37:16","2021-07-04 09:37:16","2021-07-04 22:37:16","2021-07-04 09:37:16","2021-07-04 20:37:16"]

// 上方板块内容
  let userinfo=ref({"mission_count":1,"undone_mission":2,"message":35})
  let username=ref("before")
  function change(){
    username.value="after"
  }
  let hh = new Date().getHours();
  let greet = computed( () => {
    if (hh<=10 && hh>=6) return "早安，";
    else if (hh<=18 && hh>10) return "午安，";
    else return "晚上好！";
  });
  function gotomission() {
    router.push('/list/basiclist')
  }
  function gotomessage() {
    router.push('/setting/system')
  }

//任务部分
  let short_mission=ref([])

//页面加载
  onMounted(() => {
    //请求任务
    axios({//格式a
      method:'get',
      url:'http://localhost:8000/short_mission/',
    }).then(function(resp){
      console.log(resp.data);
    }).catch(resp => {
      if (resp.status=="200") {
        short_mission.value=resp.data.short_mission
      }
      else{
        console.log('请求失败：'+resp.status+','+resp.statusText);
      }
    });

    //请求动态
    axios({//格式a
      method:'get',
      url:'http://localhost:8000/short_message/',
    }).then(function(resp){
      console.log(resp.data);
    }).catch(resp => {
      if (resp.status=="200") {
        short_message.value=resp.data.short_message
      }
      else{
        console.log('请求失败：'+resp.status+','+resp.statusText);
      }
    });

    //请求用户信息
    axios({//格式a
      method:'get',
      url:'http://localhost:8000/user_info/',
    }).then(function(resp){
      console.log(resp.data);
    }).catch(resp => {
      if (resp.status=="200") {
        userinfo.value=resp.data.user_info
      }
      else{
        console.log('请求失败：'+resp.status+','+resp.statusText);
      }
    });
  })

</script>

<style lang="less" scoped>
.workspace_clickable:hover{
  color:orange;
}

  .project-card {
    margin-right: -6px;

    &-item {
      margin: -1px;
      width: 33.333333%;
    }
  }
</style>
