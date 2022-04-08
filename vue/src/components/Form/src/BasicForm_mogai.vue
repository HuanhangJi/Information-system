<template>
  <n-form
    ref="formref"
    inline
    :label-width="80"
    :model="formValue"
    :rules="rules"
    :size="size"
  >
    <n-form-item v-for="(value,index) in formlist" :key="index" :label="value.label">
        <n-input v-model:value="formValue[index]" :placeholder="'输入'+value.label" v-if="value.type==='input'" class="w-32" autosize/>
        <n-select v-model:value="formValue[index]" :options="value.options" :placeholder="'选择'+value.label" v-if="value.type==='select'" class="w-32"/>
        <n-date-picker v-model:value="formValue[index]" type="datetime" :placeholder="'选择'+value.label" v-if="value.type==='time'" />
        <n-input v-model:value="formValue[index][0]" placeholder="最小值" v-if="value.type==='interval'" class="w-24" autosize/>
        <span v-if="value.type==='interval'" style="white-space: pre">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;—&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <n-input v-model:value="formValue[index][1]" placeholder="最大值" v-if="value.type==='interval'" class="w-24" autosize/>
    </n-form-item>
    <n-form-item class="absolute right-2">
      <n-button attr-type="button" @click="log" class="mr-4 bg-blue-500 text-white">
        查询
      </n-button>
      <n-button attr-type="button" @click="resetform">
        重置
      </n-button>
    </n-form-item>
  </n-form>

</template>

<script lang="ts">
  import { defineComponent, reactive, ref, computed, unref, onMounted, watch } from 'vue';
  import { FormInst, useMessage } from 'naive-ui'
  export default defineComponent({
    name: 'BasicUpload',
    setup(props, { emit, attrs }) {
      let role=ref("pointer")
      let start_time=new Date()
      let end_time=new Date()
      let formValue=ref(["","","",start_time,end_time,[,],[,]])
      let formlist=ref([
        {type:"input",label:"任务id"},
        {type:"input",label:"发布者"},
        {type:"select",label:"任务状态",options:[{label:"已开始",value:"已开始"},{label:"已完成",value:"已完成"},{label:"已放弃",value:"已放弃"}]},
        {type:"time",label:"开始时间"},
        {type:"time",label:"结束时间"},
        {type:"interval",label:"等级"},
        {type:"interval",label:"报酬"}
      ])
      function getSchema(){
          if (role.value==="poster"){
            return [
            ]
          }
      }
      function resetform() {
        formValue.value=["","","",new Date(),new Date(),[,],[,]]
      }
      function log(){
        console.log(formValue)
      }

      return {
        formValue,
        getSchema,
        formlist,
        role,
        resetform,
        log
      };
    },
  });
</script>

<style lang="less" scoped>
  .isFull {
    width: 100%;
    justify-content: flex-start;
  }

  .unfold-icon {
    display: flex;
    align-items: center;
    height: 100%;
    margin-left: -3px;
  }
</style>
