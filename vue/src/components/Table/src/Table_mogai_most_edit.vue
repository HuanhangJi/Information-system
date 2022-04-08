<template>
  <div class="table-toolbar">
    <!--顶部左侧区域-->
<!--    <div class="flex items-center table-toolbar-left">-->
<!--      <template v-if="title">-->
<!--        <div class="table-toolbar-left-title">-->
<!--          {{ title }}-->
<!--          <n-tooltip trigger="hover" v-if="titleTooltip">-->
<!--            <template #trigger>-->
<!--              <n-icon size="18" class="ml-1 text-gray-400 cursor-pointer">-->
<!--                <QuestionCircleOutlined />-->
<!--              </n-icon>-->
<!--            </template>-->
<!--            {{ titleTooltip }}-->
<!--          </n-tooltip>-->
<!--        </div>-->
<!--      </template>-->
<!--      <slot name="tableTitle"></slot>-->
<!--    </div>-->

    <div class="flex items-center table-toolbar-right">
      <!--顶部右侧区域-->
      <slot name="toolbar"></slot>

      <!--刷新-->
      <n-tooltip trigger="hover">
        <template #trigger>
          <div class="table-toolbar-right-icon" @click="reload">
            <n-icon size="18">
              <ReloadOutlined />
            </n-icon>
          </div>
        </template>
        <span>刷新</span>
      </n-tooltip>

      <!--密度-->
<!--      <n-tooltip trigger="hover">-->
<!--        <template #trigger>-->
<!--          <div class="table-toolbar-right-icon">-->
<!--            <n-dropdown-->
<!--              @select="densitySelect"-->
<!--              trigger="click"-->
<!--              :options="densityOptions"-->
<!--              v-model:value="tableSize"-->
<!--            >-->
<!--              <n-icon size="18">-->
<!--                <ColumnHeightOutlined />-->
<!--              </n-icon>-->
<!--            </n-dropdown>-->
<!--          </div>-->
<!--        </template>-->
<!--        <span>密度</span>-->
<!--      </n-tooltip>-->

      <!--表格设置单独抽离成组件-->
<!--      <ColumnSetting />-->
    </div>
  </div>
  <div class="s-table">
    <n-data-table
      ref="tableElRef"
      :columns="columns"
      :data="data"
      :pagination="pagination"
      @update:page="updatePage"
      @update:page-size="updatePageSize"
      :loading="isloading"
    >
<!--      <template #[item]="data" v-for="item in Object.keys($slots)" :key="item">-->
<!--        <slot :name="item" v-bind="data"></slot>-->
<!--      </template>-->
    </n-data-table>
  </div>
</template>

<script lang="ts">
import {
  ref,
  defineComponent,
  reactive,
  unref,
  toRaw,
  computed,
  toRefs,
  onMounted,
  nextTick,
  h,
  watch,
} from 'vue';
import { ReloadOutlined, ColumnHeightOutlined, QuestionCircleOutlined } from '@vicons/antd';
// import ColumnSetting from './components/settings/ColumnSetting.vue';
import { basicProps } from './props';
import { NButton } from 'naive-ui';
import axios from "axios";

const densityOptions = [
  {
    type: 'menu',
    label: '紧凑',
    key: 'small',
  },
  {
    type: 'menu',
    label: '默认',
    key: 'medium',
  },
  {
    type: 'menu',
    label: '宽松',
    key: 'large',
  },
];


type mission = {
  mission_id: number
  poster: string
  state: string
  start_time:string
  end_time:string
  level:number
  money:number
};
export default defineComponent({
  components: {
    ReloadOutlined,
    ColumnHeightOutlined,
    // ColumnSetting,
    QuestionCircleOutlined,
  },
  props: {
    ...basicProps,
  },
  emits: [
    'fetch-success',
    'fetch-error',
    'update:checked-row-keys',
    'edit-end',
    'edit-cancel',
    'edit-row-end',
    'edit-change',
  ],
    setup(props, { emit }) {
      let isloading=ref(false)

      function getPageColumns_mogai() {
        return [
          {title:"任务id",key:"mission_id"},
          {title:"发布者",key:"poster"},
          {title:"任务状态",key:"state"},
          {title:"开始时间",key:"start_time"},
          {title:"结束时间",key:"end_time"},
          {title:"等级",key:"level"},
          {title:"报酬",key:"money"},
          {title: 'Action',key: 'actions',
            render (row) {
              return h(NButton,
                {
                  strong: true,tertiary: true, size: 'small', onClick: () => row_del(row)
                },
                { default: () => 'Play' }
              )
            }
          }
        ]
      }
      function row_del(row:any){
        axios({//格式a
          method:'post',
          url:'http://localhost:8000/mission/',
          data:{"info":row}

        }).then(function(resp){
          console.log(resp.data);
        }).catch(resp => {
          if (resp.status=="200") {
            tabledata_mogai.value=resp.data.mission
          }
          else{
            console.log('请求失败：'+resp.status+','+resp.statusText);
          }
        });
        console.log(row)
      };
      function recover() {
        isloading.value=false
      }
      function reload(){
        isloading.value= true;
        console.log("开始")
        var startTime = new Date().getTime();
        // while (new Date().getTime() < startTime + 1000) {
        //   // console.log(new Date().getTime());
        // }//暂停一段时间 1000=1S。
        setTimeout(recover,1000)
        console.log("结束")
      }
      let tabledata_mogai=ref({})
      onMounted( () => {
        axios({//格式a
          method:'get',
          url:'http://localhost:8000/mission/',
        }).then(function(resp){
          console.log(resp.data);
        }).catch(resp => {
          if (resp.status=="200") {
            tabledata_mogai.value=resp.data.mission
          }
          else{
            console.log('请求失败：'+resp.status+','+resp.statusText);
          }
        });
      })
      //组装表格信息
      tabledata_mogai.value=Array.apply(null, { length: 46 }).map((_, index) => ({
        mission_id: index,
        poster: `Edward King ${index}`,
        state: "已开始",
        start_time: `London, Park Lane no. ${index}`,
        end_time:"123",
        level:1,
        money:111
      }));
      const paginationReactive = reactive({
        page: 2,
        pageSize: 5,
        showSizePicker: true,
        pageSizes: [3, 5, 7],
        onChange: (page) => {
          paginationReactive.page = page
        },
        onUpdatePageSize: (pageSize) => {
          paginationReactive.pageSize = pageSize
          paginationReactive.page = 1
        }
      })


      return {
        columns: toRaw(unref(getPageColumns_mogai())),
        data:tabledata_mogai,
        pagination:paginationReactive,
        isloading,
        reload,
      };
    },

  });
</script>
<style lang="less" scoped>
  .table-toolbar {
    display: flex;
    justify-content: space-between;
    padding: 0 0 16px 0;

    &-left {
      display: flex;
      align-items: center;
      justify-content: flex-start;
      flex: 1;

      &-title {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        font-size: 16px;
        font-weight: 600;
      }
    }

    &-right {
      display: flex;
      justify-content: flex-end;
      flex: 1;

      &-icon {
        margin-left: 12px;
        font-size: 16px;
        cursor: pointer;
        color: var(--text-color);

        :hover {
          color: #1890ff;
        }
      }
    }
  }

  .table-toolbar-inner-popover-title {
    padding: 2px 0;
  }
</style>
