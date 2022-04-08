<template>
  <div class="table-toolbar">
    <!--顶部左侧区域-->
    <div class="flex items-center table-toolbar-left">
      <template v-if="title">
        <div class="table-toolbar-left-title">
          {{ title }}
          <n-tooltip trigger="hover" v-if="titleTooltip">
            <template #trigger>
              <n-icon size="18" class="ml-1 text-gray-400 cursor-pointer">
                <QuestionCircleOutlined />
              </n-icon>
            </template>
            {{ titleTooltip }}
          </n-tooltip>
        </div>
      </template>
      <slot name="tableTitle"></slot>
    </div>

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
      <n-tooltip trigger="hover">
        <template #trigger>
          <div class="table-toolbar-right-icon">
            <n-dropdown
              @select="densitySelect"
              trigger="click"
              :options="densityOptions"
              v-model:value="tableSize"
            >
              <n-icon size="18">
                <ColumnHeightOutlined />
              </n-icon>
            </n-dropdown>
          </div>
        </template>
        <span>密度</span>
      </n-tooltip>

      <!--表格设置单独抽离成组件-->
      <ColumnSetting />
    </div>
  </div>
  <div class="s-table">
    <n-data-table
      ref="tableElRef"
      v-bind="getBindValues"
      :pagination="pagination"
      @update:page="updatePage"
      @update:page-size="updatePageSize"
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
  } from 'vue';
  import { ReloadOutlined, ColumnHeightOutlined, QuestionCircleOutlined } from '@vicons/antd';
  import { createTableContext } from './hooks/useTableContext';

  import ColumnSetting from './components/settings/ColumnSetting.vue';

  import { useLoading } from './hooks/useLoading';
  import { useColumns } from './hooks/useColumns';
  import { useDataSource } from './hooks/useDataSource';
  import { usePagination } from './hooks/usePagination';

  import { basicProps } from './props';

  import { BasicTableProps } from './types/table';

  import { getViewportOffset } from '@/utils/domUtils';
  import { useWindowSizeFn } from '@/hooks/event/useWindowSizeFn';
  import { isBoolean } from '@/utils/is';
  import { NButton } from 'naive-ui';

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

  export default defineComponent({
    components: {
      ReloadOutlined,
      ColumnHeightOutlined,
      ColumnSetting,
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
      const deviceHeight = ref(150);
      const tableElRef = ref<ComponentRef>(null);
      const wrapRef = ref<Nullable<HTMLDivElement>>(null);
      let paginationEl: HTMLElement | null;

      const tableData = ref<Recordable[]>([]);
      const innerPropsRef = ref<Partial<BasicTableProps>>();

      const getProps = computed(() => {
        return { ...props, ...unref(innerPropsRef) } as BasicTableProps;
      });

      const { getLoading, setLoading } = useLoading(getProps);

      const { getPaginationInfo, setPagination } = usePagination(getProps);

      const { getDataSourceRef, getDataSource, getRowKey, reload } = useDataSource(
        getProps,
        {
          getPaginationInfo,
          setPagination,
          tableData,
          setLoading,
        },
        emit
      );

      const { getPageColumns, setColumns, getColumns, getCacheColumns, setCacheColumnsField } =
        useColumns(getProps);

      const state = reactive({
        tableSize: unref(getProps as any).size || 'medium',
        isColumnSetting: false,
      });

      //页码切换
      function updatePage(page) {
        setPagination({ page: page });
        reload();
      }

      //分页数量切换
      function updatePageSize(size) {
        setPagination({ page: 1, pageSize: size });
        reload();
      }

      //密度切换
      function densitySelect(e) {
        state.tableSize = e;
      }

      //选中行
      function updateCheckedRowKeys(rowKeys) {
        emit('update:checked-row-keys', rowKeys);
      }

      //获取表格大小
      const getTableSize = computed(() => state.tableSize);
      type mission = {
        mission_id: number
        poster: string
        state: string
        start_time:string
        end_time:string
        level:number
        money:number
      }
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
        console.log(row)
      };
      //组装表格信息
      const tabledata_mogai:mission=ref([
        {mission_id:123,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:123,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:123,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:123,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:123,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:123,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:123,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:123,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:123,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:123,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:124,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:124,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:124,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:124,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:124,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:124,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:124,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:124,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},
        {mission_id:124,poster:"person1",state:"已完成",start_time:"12.30",end_time:"12.45",level:1,money:3.70},

      ])

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

      const getBindValues = computed(() => {
          const maxHeight = tabledata_mogai.value.length ? `${unref(deviceHeight)}px` : 'auto';
          return {
            loading: unref(getLoading),
            columns: toRaw(unref(getPageColumns_mogai())),
            data:tabledata_mogai.value,
            size: unref(getTableSize),
            remote:true,
            'max-height': maxHeight,
            pagination:paginationReactive
          }
        }
      );
      // const getBindValues = computed(() => {
      //   const tableData = unref(getDataSourceRef);
      //   const maxHeight = tableData.length ? `${unref(deviceHeight)}px` : 'auto';
      //   return {
      //     ...unref(getProps),
      //     loading: unref(getLoading),
      //     columns: toRaw(unref(getPageColumns)),
      //     rowKey: unref(getRowKey),
      //     data: tableData,
      //     size: unref(getTableSize),
      //     remote: true,
      //     'max-height': maxHeight,
      //   };
      // });


      //获取分页信息
      // const pagination = computed(() => toRaw(unref(getPaginationInfo)));
      // console.log(pagination)
      function setProps(props: Partial<BasicTableProps>) {
        innerPropsRef.value = { ...unref(innerPropsRef), ...props };
      }

      const tableAction = {
        reload,
        setColumns,
        setLoading,
        setProps,
        getColumns,
        getPageColumns,
        getCacheColumns,
        setCacheColumnsField,
        emit,
      };

      const getCanResize = computed(() => {
        const { canResize } = unref(getProps);
        return canResize;
      });

      async function computeTableHeight() {
        const table = unref(tableElRef);
        if (!table) return;
        if (!unref(getCanResize)) return;
        const tableEl: any = table?.$el;
        const headEl = tableEl.querySelector('.n-data-table-thead ');
        const { bottomIncludeBody } = getViewportOffset(headEl);
        const headerH = 64;
        let paginationH = 2;
        let marginH = 24;
        if (!isBoolean(paginationReactive)) {
          paginationEl = tableEl.querySelector('.n-data-table__pagination') as HTMLElement;
          if (paginationEl) {
            const offsetHeight = paginationEl.offsetHeight;
            paginationH += offsetHeight || 0;
          } else {
            paginationH += 28;
          }
        }
        let height =
          bottomIncludeBody - (headerH + paginationH + marginH + (props.resizeHeightOffset || 0));
        const maxHeight = props.maxHeight;
        height = maxHeight && maxHeight < height ? maxHeight : height;
        deviceHeight.value = height;
      }

      useWindowSizeFn(computeTableHeight, 280);

      onMounted(() => {
        nextTick(() => {
          computeTableHeight();
        });
      });

      createTableContext({ ...tableAction, wrapRef, getBindValues });

      return {
        ...toRefs(state),
        tableElRef,
        getBindValues,
        getDataSource,
        densityOptions,
        reload,
        densitySelect,
        updatePage,
        updatePageSize,
        // pagination,
        tableAction,
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
