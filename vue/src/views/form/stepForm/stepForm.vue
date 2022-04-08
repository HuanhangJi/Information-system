<template>
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
      <div v-if="type===2">
    <!--    <div class="n-layout-page-header">-->
    <!--      <n-card :bordered="false" title="分步表单">-->
    <!--        将一个冗长或用户不熟悉的表单任务分成多个步骤，指导用户完成。-->
    <!--      </n-card>-->
    <!--    </div>-->
        <n-card :bordered="false" class="proCard">
          <n-space vertical class="steps" justify="center">
            <n-steps :current="currentTab" :status="currentStatus">
              <n-step title="填写提现信息" description="确保填写正确" />
              <n-step title="确认提现信息" description="确认转账信息" />
              <n-step title="完成转账" description="恭喜您，转账成功" />
            </n-steps>
            <step1 v-if="currentTab === 1" @nextStep="nextStep" />
            <step2 v-if="currentTab === 2" @nextStep="nextStep" @prevStep="prevStep" />
            <step3 v-if="currentTab === 3" @prevStep="prevStep" @finish="finish" />
          </n-space>
        </n-card>
      </div>
      <div v-if="type===1">
        <n-card :bordered="false"
                class="proCard"
                title="我的钱包"
                :segmented="{
                  content: true,
                  footer: 'soft'
                }"
        >
          <template #header-extra>
            加油，打工仔
          </template>
          <div>账户余额</div>
          <div>
            <span class="text-3xl">{{account.count}}</span>
            <span>RMB</span>
          </div>
        </n-card>
      </div>
    </n-grid-item>
  </n-grid>
</template>

<script setup>
import { defineComponent, onMounted, ref } from "vue";
import axios from "axios";
  import step1 from './Step1.vue';
  import step2 from './Step2.vue';
  import step3 from './Step3.vue';
  // import Space from "../../../../dist/assets/vendor.5028d859";
  const typeTabList = [
    {
      name: '钱包信息',
      desc: '个人钱包信息',
      key: 1,
    },
    {
      name: '转账',
      desc: '转入您的个人账户',
      key: 2,
    },
    {
      name: '常见问题及解答',
      desc: '大多数问题都能得到解答,嗯,大多数.',
      key: 3,
    }

  ];
  let type=ref(1)
  let account={count:123}
  function switchType(e) {
    type.value = e.key;
    typeTitle.value = e.name;
  }

  const currentTab = ref(1);
  const currentStatus = ref('process');

  function nextStep() {
    if (currentTab.value < 3) {
      currentTab.value += 1;
    }
  }

  function prevStep() {
    if (currentTab.value > 1) {
      currentTab.value -= 1;
    }
  }

  function finish() {
    currentTab.value = 1;
  }
onMounted(()=>{
  console.log("start")
  axios({//格式a
    method:'get',
    url:'http://localhost:8000/edit/',

  }).then(function(resp){
    console.log(resp.data);
  }).catch(resp => {
    console.log('请求失败：'+resp.status+','+resp.statusText);
  });
  console.log("end")
})
</script>

<style lang="less" scoped>
  .steps {
    max-width: 750px;
    margin: 16px auto;
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
  .thing-cell {
    margin: 0 -16px 10px;
    padding: 5px 16px;
    &:hover {
      background: #f3f3f3;
      cursor: pointer;
    }
  }
</style>
