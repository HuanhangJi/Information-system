<template>
  <n-grid cols="1" responsive="screen" class="-mt-5">
    <n-grid-item>
      <n-list>
        <n-list-item>
          <template #suffix>
            <n-button type="primary" text @click="edit_password=!edit_password">{{!edit_password? '修改':'返回'}}</n-button>
          </template>
          <n-thing title="账户密码">
            <template #description
              ><span class="text-gray-400" v-if="!edit_password" >绑定手机和邮箱，并设置密码，帐号更安全</span></template
            >
          </n-thing>
          <n-form v-if="edit_password" :rules="password_rules">
            <n-form-item label="旧密码" path="oldPassword">
              <n-input v-if="edit_password" v-model:value="old_password" placeholder="请输入旧密码" class="w-64" autosize type="password"/>
            </n-form-item>
            <n-form-item label="新密码" path="newPassword">
              <n-input v-if="edit_password" v-model:value="new_password" placeholder="请输入新密码" class="w-64" autosize type="password"/>
            </n-form-item>
            <n-form-item label="确认新密码" path="confirmPassword">
              <n-input v-if="edit_password" v-model:value="config_password" placeholder="请确认新密码" class="w-64" autosize type="password"/>
            </n-form-item>
          </n-form>
        </n-list-item>
        <n-list-item>
          <template #suffix>
            <n-button type="primary" text @click="edit_phone=!edit_phone">{{!edit_phone? '修改':'返回'}}</n-button>
          </template>
          <n-thing title="绑定手机">
            <template #description v-if="!edit_phone"
              ><span class="text-gray-400">已绑定手机号：+86189****4877</span></template
            >
          </n-thing>
          <n-form  v-if="edit_phone" :rules="phone_rules">
          <n-form-item label="换绑新手机号" v-if="edit_phone" path="newPhone">
            <n-input v-model:value="new_phone" placeholder="输入新手机号" class="w-64" autosize/>
          </n-form-item>
          </n-form>
        </n-list-item>
        <n-list-item>
          <template #suffix>
            <n-button type="primary" text>设置</n-button>
          </template>
          <n-thing title="密保问题">
            <template #description
              ><span class="text-gray-400"
                >未设置密保问题，密保问题可有效保护账户安全</span
              ></template
            >
          </n-thing>
        </n-list-item>
<!--        <n-list-item>-->
<!--          <template #suffix>-->
<!--            <n-button type="primary" text>修改</n-button>-->
<!--          </template>-->
<!--          <n-thing title="个性域名">-->
<!--            <template #description-->
<!--              ><span class="text-gray-400">已绑定域名：https://www.naiveui.com</span></template-->
<!--            >-->
<!--          </n-thing>-->
<!--        </n-list-item>-->
      </n-list>
    </n-grid-item>
  </n-grid>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
let edit_password=ref(false)
let edit_phone=ref(false)
let old_password=ref("")
let new_password=ref("")
let config_password=ref("")
let new_phone=ref("")
let password_rules={
  oldPassword: {
    required: true,
    message: '请输入旧密码',
    trigger: 'blur',
  },
  newPassword: {
    required: true,
    message: '请输入新密码',
    trigger: 'blur',
  },
  confirmPassword: {
    required: true,
    message: '请确认新密码',
    trigger: 'blur',
  },
}
let phone_rules={
  newPhone: {
    required: true,
    message: '请输入手机号',
    trigger: 'blur',
  },
}
</script>
