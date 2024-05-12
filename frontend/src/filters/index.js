// set function parseTime,formatTime to filter
export { parseTime, formatTime } from '@/utils'

function pluralize(time, label) {
  if (time === 1) {
    return time + label
  }
  return time + label + 's'
}

export function timeAgo(time) {
  const between = Date.now() / 1000 - Number(time)
  if (between < 3600) {
    return pluralize(~~(between / 60), ' minute')
  } else if (between < 86400) {
    return pluralize(~~(between / 3600), ' hour')
  } else {
    return pluralize(~~(between / 86400), ' day')
  }
}

/* 数字 格式化*/
export function numberFormatter(num, digits) {
  const si = [
    { value: 1E18, symbol: 'E' },
    { value: 1E15, symbol: 'P' },
    { value: 1E12, symbol: 'T' },
    { value: 1E9, symbol: 'G' },
    { value: 1E6, symbol: 'M' },
    { value: 1E3, symbol: 'k' }
  ]
  for (let i = 0; i < si.length; i++) {
    if (num >= si[i].value) {
      return (num / si[i].value + 0.1).toFixed(digits).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, '$1') + si[i].symbol
    }
  }
  return num.toString()
}

export function toThousandFilter(num) {
  return (+num || 0).toString().replace(/^-?\d+/g, m => m.replace(/(?=(?!\b)(\d{3})+$)/g, ','))
}

// 格式化时间
export function parseDate(datestr) {
  if (datestr !== undefined) {
    const date = datestr.slice(0, 10)
    const time = datestr.slice(11, 19)
    return date + ' ' + time
  }
}

export function diffDate(date) {
  const d1 = new Date()
  const d2 = new Date(date)
  return Math.round(parseInt(d2 - d1) / 1000 / 60 / 60 / 24)
}

// 菜单
export function menuTypeFilter(val) {
  const Map = {
    1: '模塊',
    2: '菜單',
    3: '操作'
  }
  return Map[val]
}

// 按钮
export function operateTypeFilter(val) {
  const Map = {
    'none': '無',
    'add': '新增',
    'del': '刪除',
    'update': '編輯',
    'view': '查看'
  }
  return Map[val]
}

// 字段类型
export function FieldTypeFilter(val) {
  const Map = {
    1: '字符串',
    2: '整型',
    3: '浮點型',
    4: '布爾',
    5: '日期',
    6: '日期時間',
    7: '範圍日期',
    8: '文本域',
    9: '單選框',
    10: '下拉列表',
    11: '用戶名',
    12: '多選框',
    13: '多選下拉',
    14: '多選用戶名'
  }
  return Map[val]
}

// 状态类型
export function StateTypeFilter(val) {
  const Map = {
    0: '普通狀態',
    1: '初始狀態',
    2: '結束狀態'
  }
  return Map[val]
}

// 流转类型
export function TransitionTypeFilter(val) {
  const Map = {
    0: '常規流轉',
    1: '定時器流轉'
  }
  return Map[val]
}

// 属性类型
export function AttributeTypeFilter(val) {
  const Map = {
    0: '草稿',
    1: '待審',
    2: '駁回',
    3: '撤銷',
    4: '結束',
    5: '已關閉'
  }
  return Map[val]
}

// 流转名称
export function TransitionNameFilter(val) {
  const Map = {
    0: '保存',
    1: '轉交下一步',
    2: '駁回',
    3: '撤銷',
    4: '關閉'
  }
  return Map[val]
}

// 取第一个字母并大写
export function AvatarFilter(val) {
  return val.substr(0, 1).toUpperCase()
}
