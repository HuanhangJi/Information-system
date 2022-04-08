import { h } from 'vue';
import { NButton } from "naive-ui";



export const columns=[
  {title:"任务id",key:"mission_id",width:50},
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
function row_del(row:any){
  console.log(row)
};
//
// export const columns = [
//   {
//     title: 'mission_id',
//     key: 'id',
//     width: 100,
//   },
//   {
//     title: '名称',
//     key: 'name',
//     width: 100,
//   },
//   {
//     title: '头像',
//     key: 'avatar',
//     width: 100,
//     render(row) {
//       return h(NAvatar, {
//         size: 48,
//         src: row.avatar,
//       });
//     },
//   },
//   {
//     title: '地址',
//     key: 'address',
//     auth: ['basic_list'], // 同时根据权限控制是否显示
//     ifShow: (_column) => {
//       return true; // 根据业务控制是否显示
//     },
//     width: 150,
//   },
//   {
//     title: '开始日期',
//     key: 'beginTime',
//     width: 160,
//   },
//   {
//     title: '结束日期',
//     key: 'endTime',
//     width: 160,
//   },
//   {
//     title: '创建时间',
//     key: 'date',
//     width: 100,
//   },
// ];
